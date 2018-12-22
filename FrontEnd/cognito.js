let apigClient;

AWS.config.region = 'us-east-1';

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    // IdentityPoolId: 'IDENTITY_POOL_ID',//us-east-1:cb582d62-f692-4c62-ac28-7cc8efc9ee2c
    IdentityPoolId:'us-east-1:b411f013-c667-4600-8c91-2c768794c2cb',
    Logins: {
            }
});

AWS.config.credentials.get(function(){

    // Credentials will be available when this function is called.
    var accessKeyId = AWS.config.credentials.accessKeyId;
    var secretAccessKey = AWS.config.credentials.secretAccessKey;
    var sessionToken = AWS.config.credentials.sessionToken;
    var identityId = AWS.config.credentials.identityId;
    console.log(identityId);

});

var AWSconfig = {
    "accessKey":"",
    "secretKey":"",
    "S3Bucket":"",
    "region":"us-east-1",
    "sessionToken":"",
    "client_id" :"5l4t998gnc709pjvppfbdvgp62",
    "user_pool_id" : "us-east-1_QKIkGEZDA",
    "cognito_domain_url":"https://stockprediction.auth.us-east-1.amazoncognito.com",
    "redirect_uri" : "https://s3.amazonaws.com/stockprediction/mainpage.html",
    "identity_pool_id":"us-east-1:cb582d62-f692-4c62-ac28-7cc8efc9ee2c"
};


var getParameterByName = function(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

var exchangeAuthCodeForCredentials = function({auth_code = getParameterByName("code"),
                                                client_id = AWSconfig.client_id,
                                                identity_pool_id = AWSconfig.identity_pool_id,
                                                aws_region =AWSconfig.region,
                                                user_pool_id = AWSconfig.user_pool_id,
                                                cognito_domain_url= AWSconfig.cognito_domain_url,
                                                redirect_uri = AWSconfig.redirect_uri}) {
    return new Promise((resolve, reject) => {
        var settings = {
            url: `${cognito_domain_url}/oauth2/token`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {
                grant_type: 'authorization_code',
                client_id: client_id,
                redirect_uri: redirect_uri,
                code: auth_code
            }
        };
        $.ajax(settings).done(function (response) {
            console.log('OAuth2 Token Call Responded');
            console.log(response);
            if (response.id_token) {
                AWS.config.region = aws_region;
                AWS.config.credentials = new AWS.CognitoIdentityCredentials({
                    IdentityPoolId : identity_pool_id,
                    Logins : {
                        [`cognito-idp.${aws_region}.amazonaws.com/${user_pool_id}`]: response.id_token
                    }
                });

                console.log({IdentityPoolId : identity_pool_id,
                    Logins : {
                        [`cognito-idp.${aws_region}.amazonaws.com/${user_pool_id}`]: response.id_token
                    }
                });

                AWS.config.credentials.refresh(function (error) {
                    console.log("Error",error);
                    if (error) {
                        reject(error);
                    } else {
                        console.log('Successfully Logged In');
                        resolve(AWS.config.credentials);
                    }
                });
            } else {
                reject(response);
            }

            var params = {
          AccessToken: response.access_token /* required */
          };
          console.log('params');
          var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider();
          cognitoidentityserviceprovider.getUser(params, function (err, data) {
          if (err) console.log(err, err.stack); // an error occurred
          else     console.log(data);
         userid_email= data.UserAttributes[2].Value.toString();          // successful response
          console.log("acess token wala data");
          // console.log(userid_email);
          });

        });
    });
};

console.log("Calling for auth credentials exchange");

exchangeAuthCodeForCredentials({auth_code: code,
                                client_id: AWSconfig.client_id,
                                identity_pool_id: AWSconfig.identity_pool_id,
                                aws_region: AWSconfig.region,
                                user_pool_id: AWSconfig.user_pool_id,
                                cognito_domain_url: AWSconfig.cognito_domain_url,
                                redirect_uri: AWSconfig.redirect_uri})
  .then(function(response) {

    console.log("Inside Then Function",response);
    // console.log(response.accessKeyId);
    // let access_key=response.accessKeyId;
     apigClient = apigClientFactory.newClient({
        accessKey: response.accessKeyId,
        secretKey: response.secretAccessKey,
        sessionToken: response.sessionToken,
        region: "us-east-1"
    });



  })
  .catch(function(error) {
      console.log("Got error ... ");
      console.log("error = "+this.error);
      console.log("response = "+this.response);
  });
