//function to display predicted result for specific stock

function displayChart(stockName,response)
{

  var arrayA = response.body['oldDates'];
  var arrayB = response.body['dates'];
  var xData = arrayA.concat(arrayB);


  var arraydataA = response.body['oldData'];
  var arraydataB = response.body['data'];

  var yData = arraydataA.concat(arraydataB);
  var yaxisData = []
  yData.forEach(function(element) {
     yaxisData.push(element['score'])
  });



 xData.unshift('x');
 yaxisData.unshift(stockName);

var chart = c3.generate({
     // bindto: '#chart',
     data: {
         x: 'x',
         xFormat: '%Y-%m-%d',
         columns: [
             xData,
             yaxisData
        ]
    },
    axis: {
        x: {
             type: 'category',
             tick: {
                 format: '%Y-%m-%d'
             }
        }
    }


});

}

// function to compare two different stocks selected by user
function displaycompareChart(response,stockname1,stockname2){

  var yaxisData1 = []
  var yaxisData2 = []
  var arrayACompare = response['company1']['oldDates'];

  console.log(arrayACompare)



  var arrayBCompare = response['company1']['dates'];
  var xDataCompare = arrayACompare.concat(arrayBCompare);

  var arrayAyCompare = response['company1']['oldData'];

  var arrayByCompare = response['company1']['data'];
  var yDataCompare = arrayAyCompare.concat(arrayByCompare);

  yDataCompare.forEach(function(element) {
     yaxisData1.push(parseFloat(element['score']))
  });

  var arrayAy1Compare = response['company2']['oldData'];

  var arrayBy1Compare = response['company2']['data'];
  var y1DataCompare = arrayAy1Compare.concat(arrayBy1Compare);

  y1DataCompare.forEach(function(element) {
     yaxisData2.push(parseFloat(element['score']))
  });

  xDataCompare.unshift('xDataCompare')
  yaxisData1.unshift(stockname1);
  yaxisData2.unshift(stockname2);

  console.log(yaxisData1);
  var chart1 = c3.generate({
       data: {
           x: 'xDataCompare',
           xFormat: '%Y-%m-%d',
           columns: [
             xDataCompare,
             yaxisData1,
             yaxisData2

          ]
      },
      axis: {
          x: {
               type: 'category',
               tick: {
                   format: '%Y-%m-%d'
               }
          }
      }


  });

}
