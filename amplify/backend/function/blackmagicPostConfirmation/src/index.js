const AWS = require('aws-sdk');
const { v4: uuidv4 } = require('uuid');

const documentClient = new AWS.DynamoDB.DocumentClient();
const s3 = new AWS.S3();

async function createUser(email) {
  try {
    const userId = uuidv4();
    const usersTableParams = {
      TableName: process.env.USERS_TABLE_NAME,
      Item: {
        email,
        id: userId
      }
    };
    await documentClient.put(usersTableParams).promise();
    return userId;
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
    let items;
    do {
      items = await documentClient.scan(codesTableParams).promise();
      items.Items.forEach((item) => mp3sToDistribute.push(item));
      codesTableParams.ExclusiveStartKey = items.LastEvaluatedKey;
    } while (typeof items.LastEvaluatedKey !== 'undefined');

    return mp3sToDistribute;
  } catch (err) {
    return err;
  }
}

async function distributeExistingMp3sToUser(userId) {
  try {
    const mp3sToDistribute = [...(await listMp3sToDistribute())];
    for (let mp3 of mp3sToDistribute) {
      s3.copyObject(
        {
          CopySource: `${process.env.SOURCE_BUCKET}/${mp3}`,
          Bucket: process.env.DESTINATION_BUCKET,
          Key: `${userId}/${mp3}`
        },
        function (copyErr, copyData) {
          if (copyErr) {
            console.log(`Error: ${copyErr}`);
          } else {
            console.log(`Success: ${copyData}`)
          }
        }
      );
    }
  } catch (err) {
    return err;
  }
}

exports.handler = async (event, context, callback) => {
  try {
    if (event.request.userAttributes['cognito:user_status'] === 'CONFIRMED') {
      const userId = await createUser(event.request.userAttributes.email);
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
