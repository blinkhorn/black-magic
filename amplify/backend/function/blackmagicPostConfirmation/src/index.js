const AWS = require('aws-sdk');
const { v4: uuidv4 } = require('uuid');

const docClient = new AWS.DynamoDB.DocumentClient();


async function createItem(email) {
  try {
    const params = {
      TableName: process.env.TABLE_NAME,
      Item: {
        email,
        id: uuidv4()
      }
    };
    await docClient.put(params).promise();
  } catch (err) {
    return err;
  }
}

exports.handler = async (event, context, callback) => {
  try {
    if (event.request.userAttributes['cognito:user_status'] === 'CONFIRMED') {
      await createItem(event.request.userAttributes.email);
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
