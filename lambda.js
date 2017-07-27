var AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
    var docClient = new AWS.DynamoDB.DocumentClient();
    tableName = "<TABLE>"
    body = JSON.parse(event.body)
    var success = body.success ? 1 : 0;
    var eventText = JSON.stringify(event, null, 2);
    var sns = new AWS.SNS();
    var params = {
        Message: "Requestid: "+body.request_id, 
        Subject: "Trigger Failed",
        TopicArn: "<SNSTOPIC>"
    };
    if (success === 0){
        sns.publish(params, context.done);
    }
    docClient.put({
        "TableName": tableName,
        "Item" : {
            "request_id": body.request_id,
            "request_uri": body.request_uri),
            "request_body": body.request_body,
            "success":success
        }
    }, function(err, data) {
        if (err) {
            console.log('great error: '+err);
            context.done('error','putting item into dynamodb failed: '+err);
            callback(null, {statusCode: 500,
                    headers: {},
                    body: JSON.stringify(err)});
        }
        else {
            console.log('great success: '+JSON.stringify(data, null, '  '));
            callback(null, {statusCode: 200,
                    headers: {},
                    body: JSON.stringify(event)});
        }
    });
};
