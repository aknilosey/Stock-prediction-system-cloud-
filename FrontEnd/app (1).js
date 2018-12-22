
$(function() {

    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});





});

$('#chart1').hide();

$("#stock2button").click(function () {$("#Comparing").prop("disabled", false);});
$("#stock1button").click(function () {$("#stockname2").prop("disabled", false);});
$("#stock1button").click(function () {$("#stock2button").prop("disabled", false);});

//Initialize apigclient
var apigClient = apigClientFactory.newClient({
                   apiKey: "hvPZUqwPyY7ksfy6x2wU79Evf07xSADv2SM0304s"
      });


//function to get user authentication token
function getUserAuthentication()
{

  var url = window.location.href;
  var url_Split = url.split("/");
  var token_id_final = " "
  var access_token = " "

    if(url.indexOf('&') > -1)
    {
      token_split = url_Split[url_Split.length - 1].split("&");
      id_token = token_split[0].split("=");
      var token_id_final = id_token[1];
      access_token_split = token_split[1].split("=");
      var access_token = access_token_split[1];
    }

  return token_id_final

}

//function to search stock1 prediction
function searchStock1()
{
  $('.scrollnews').empty();
  $('.scrolltweets').empty();
  $('.scrollopinion').empty();
  var stock_name_1 = document.getElementById("stockname1").value;
  callApi(stock_name_1)

}

//function to search for stock2 prediction
function searchStock2()
{
  $('.scrollnews').empty();
  $('.scrolltweets').empty();
  $('.scrollopinion').empty();

  var stock_name_2 = document.getElementById("stockname2").value;
  callApi(stock_name_2)
}

//api call for sage invocation
function callApi(stockName)
{

  var response = " "
  var c3data = " "

  id_token = getUserAuthentication()
  console.log(id_token)
  var post_body = { stockname : stockName };
  var post_params = {};
  var post_additionalParams = {
    headers: {
      'jwt-token':id_token
    }
  };


  apigClient.fetchstockdetailsPost(post_params,post_body,post_additionalParams)
             .then(function(res){
               response = res.data
               display(response)
             }).catch( function(result){

         });

   apigClient.sageinvocationPost(post_params,post_body,post_additionalParams)
            .then(function(res){
              c3data = res.data
              displayChart(stockName,c3data)
            }).catch( function(result){

        });

}

//this function includes api call for comparing stocks
function compareStock()
{

  $('#chart1').show();
  var stockname1 = document.getElementById("stockname1").value;
  var stockname2 = document.getElementById("stockname2").value;

  var compare_stocks = stockname1 + "," + stockname2

  var response = " "
  var c3data = " "

  id_token = getUserAuthentication()

  var post_body = { stockname : compare_stocks };
  var post_params = {};
  var post_additionalParams = {
    headers: {
      'jwt-token':id_token
    }

  };

  apigClient.comparestocksPost(post_params,post_body,post_additionalParams)
           .then(function(res){
              c3data = res.data.body
              displaycompareChart(c3data,stockname1,stockname2)
           }).catch( function(result){

       });

}

//function to get the value of current stock
function getCurrentStock()
{
  id_token = getUserAuthentication()

  var user_message = document.getElementById("current_stock_query").value;
  var post_body = { message : user_message };
  var post_params = {};
  var post_additionalParams = {
    headers: {
      'jwt-token':id_token
    }

  };

  apigClient.getcurrentstockPost(post_params,post_body,post_additionalParams)
           .then(function(res){
             console.log(res.data)
             displayCurrentStock(res.data)
           }).catch( function(result){

       });

}

function displayCurrentStock(data)
{
  div = document.getElementById('current_stock_details')

  console.log(data)

  html = '<table class="table table-primary table-bordered" style="color:white">';
  html += '<thead><th>Company Name</th><th>' + data.body['name'] +'</th></thead>';
  html += '<tbody>';

  html += '<tr><th scope="row">Open</th><td>'+ data.body['stockVal']['1. open'] +'</td></tr>';
  html += '<tr><th scope="row">High</th><td>'+ data.body['stockVal']['2. high'] +'</td></tr>';
  html += '<tr><th scope="row">Low</th><td>'+ data.body['stockVal']['3. low'] +'</td></tr>';
  html += '<tr><th scope="row">Close</th><td>'+ data.body['stockVal']['4. close'] +'</td></tr>';
  html += '<tr><th scope="row">Volume</th><td>'+ data.body['stockVal']['5. volume'] +'</td></tr>';


   html += '</tbody>';
   html += '</table>';
   $('#current_stock_details').append(html);








}

// function to display news, tweets and sentiment for the searched stock
function display(response)
{
  console.log(response)
  var news_array = response['body']['news']['news_array']
  console.log(news_array)

  var news_marquee_div = document.getElementById('news_div')

  var news_marquee_title = document.getElementById('news_title')

  html = '<div class="scrollnews" id="new_panel">';
  html += '<div class="panel panel-primary">';
  html += '<div class="panel-heading">Top News</div>';
  var flag = 0;

  $.each(news_array, function(index, v){

      html += '<div class="panel panel-default">';
      html += '<div class="panel-heading"><i class="fa fa-file-text" style="font-size:25px;color:#337ab7;vertical-align: middle;"></i>&nbsp;'+v["title"]+'</div>';
       html += '<div class="panel-body">'+v["news"]+'<br>'+'<a href="'+v["url"]+'" target="_blank">Click here for the entire story</a>'+'</div>';

       html += '</div>';
   });
     html += '</div>';
    html += '</div>';
   html += '</div>';
   $('.scrollnews').append(html);


  var sentiment = response['body']['news']['sentiment']
  console.log(sentiment)


  var twitter_array = response['body']['twitter']
  console.log(twitter_array)


  html = '<div class="scrolltweets">';
  html += '<div class="panel panel-primary">';
  html += '<div class="panel-heading">See what is being tweeted</div>';
  var flag = 0;
  $.each(twitter_array, function(index, v){
    html += '<div class="panel panel-default">';
      html += '<div class="panel-body"><i class="fa fa-twitter-square" style="font-size:30px;color:#337ab7;vertical-align: middle;"></i>&nbsp;'+v["tweet"]+'</div>';
       html += '</div>';
   });
   html += '</div>';
  html += '</div>';

   html += '</div>';
   $('.scrolltweets').append(html);



   html = '<div class="scrollopinion">';
   html += '<div class="panel panel-primary">';
   html += '<div class="panel-heading">Opinion about the stock</div>';

     html += '<div class="panel panel-default">';
       html += '<div class="panel-heading" id ="changeSentiment">'+ sentiment +'</div>';
        html += '<div class="panel-body"><img class="img-responsive" id="changeimage" src="nuetral.png"></div>';
        html += '</div>';

    html += '</div>';
    html += '</div>';

    html += '</div>';
    $('.scrollopinion').append(html);


    console.log(sentiment)



if (sentiment=='POSITIVE')
  {
    $("#changeimage").attr('src', 'increase.png');
  }
else if(sentiment=='NEGATIVE')
    {
     $("#changeimage").attr('src', 'decreasing.png');
    }
else
  {
    $("#changeimage").attr('src', 'nuetral.png');
  }

}
