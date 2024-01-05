import {
  DynamoDBDocument,
  QueryCommand,
  PutCommand
} from '@aws-sdk/lib-dynamodb';
import { DynamoDB } from '@aws-sdk/client-dynamodb';
import { S3 } from '@aws-sdk/client-s3';
import { v4 as uuidv4 } from 'uuid';

const dynamoDbDocumentClient = DynamoDBDocument.from(new DynamoDB());
const s3 = new S3();

export const handler = async (event, context, callback) => {
  try {
    if (event.request.userAttributes['cognito:user_status'] === 'CONFIRMED') {
      const emailQueryCommandResponse = await queryDatabaseForUser(
        event.request.userAttributes.email
      );
      if (
        emailQueryCommandResponse.Items &&
        emailQueryCommandResponse.Items.length
      ) {
        throw new Error(
          `The email address [ ${event.request.userAttributes.email} ] already exists in the system, please use a different email address.`
        );
      } else {
        const userId = await createUser(event.request.userAttributes.email);
        await createUserFolder(userId);
      }
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

async function queryDatabaseForUser(email) {
  try {
    const emailQueryCommand = new QueryCommand({
      TableName: process.env.USERS_TABLE_NAME,
      KeyConditionExpression: 'email = :email',
      ExpressionAttributeValues: {
        ':email': email
      }
    });
    return await dynamoDbDocumentClient.send(emailQueryCommand);
  } catch (err) {
    return err;
  }
}

async function createUser(email) {
  try {
    const userId = uuidv4();
    const createNewUserCommand = new PutCommand({
      TableName: process.env.USERS_TABLE_NAME,
      Item: {
        email,
        id: userId
      }
    });
    await dynamoDbDocumentClient.send(createNewUserCommand);
    return userId;
  } catch (err) {
    return err;
  }
}

async function createUserFolder(userId) {
  try {
    const createUserFolderParams = {
      Bucket: process.env.USER_MP3_BUCKET,
      Key: `${userId}/`
    };

    await s3.putObject(createUserFolderParams);
  } catch (err) {
    return err;
  }
}
