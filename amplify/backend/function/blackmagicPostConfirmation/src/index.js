import { DynamoDBDocument } from '@aws-sdk/lib-dynamodb'
import { DynamoDB } from '@aws-sdk/client-dynamodb';
import { S3 } from '@aws-sdk/client-s3';
import { v4 as uuidv4 } from 'uuid';

const dynamoDbDocumentClient = DynamoDBDocument.from(new DynamoDB());
const s3 = new S3();

export const handler = async (event, context, callback) => {
  try {
    if (event.request.userAttributes['cognito:user_status'] === 'CONFIRMED') {
      const userId = await createUser(event.request.userAttributes.email);
      await createUserFolder(userId);
      await distributeExistingMp3sToUser(userId);
      // return to Cognito
    } else {
      // Nothing to do, the user's not confirmed
      callback(null, event);
    }
    return event;
  } catch (err) {
    console.log(err);
  }
};

async function createUser(email) {
  try {
    const userId = uuidv4();
    const usersTablePutParams = {
      TableName: process.env.USERS_TABLE_NAME,
      Item: {
        email,
        id: userId
      }
    };
    await dynamoDbDocumentClient.put(usersTablePutParams);
    return userId;
  } catch (err) {
    return err;
  }
}

async function createUserFolder(userId) {
  try {
    const createUserFolderParams = {
      Bucket: process.env.DESTINATION_BUCKET,
      Key: `${userId}/`
    };

    await s3.putObject(createUserFolderParams);
  } catch (err) {
    return err;
  }
}

async function distributeExistingMp3sToUser(userId) {
  try {
    const mp3sToDistribute = [...(await listMp3sToDistribute())];
    for (let mp3Name of mp3sToDistribute) {
      const mp3Params = {
        CopySource: `${process.env.SOURCE_BUCKET}/${mp3Name}.mp3`,
        Bucket: process.env.DESTINATION_BUCKET,
        Key: `${userId}/${mp3Name}.mp3`
      };
      await s3
        .copyObject(mp3Params, function (copyErr, copyData) {
          if (copyErr) {
            console.log(`Error: ${copyErr}`);
          } else {
            console.log(`Success: ${copyData}`);
          }
        });
    }
  } catch (err) {
    return err;
  }
}

async function listMp3sToDistribute() {
  try {
    const codesTableParams = {
      TableName: process.env.CODES_TABLE_NAME
    };
    const mp3sToDistribute = [];
    let dynamoDbScanResponse;
    do {
      dynamoDbScanResponse = await dynamoDbDocumentClient.scan(codesTableParams);
      dynamoDbScanResponse.Items.forEach((item) => mp3sToDistribute.push(item.code));
      codesTableParams.ExclusiveStartKey = dynamoDbScanResponse.LastEvaluatedKey;
    } while (typeof dynamoDbScanResponse.LastEvaluatedKey !== 'undefined');

    return mp3sToDistribute;
  } catch (err) {
    return err;
  }
}
