$(function() {
    $(".link-prev").linkpreview({
        previewContainer: "#preview-container"
    });
});

$(document).ready(function(){

   google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Month', 'Front-end', 'Back-end'],
          ['1',  2,      3],
          ['2',  5,      5],
          ['3',  7,       10],
          ['4',  3,      15],
          ['5',  18,      5],
          ['6',  10,      25],
          ['7',  3,      30],
          ['8',  10,      25],
          ['9',  5,      18],
          ['10',  9,      22],
          ['11',  7,      7],
          ['12',  3,      13],
        ]);

        var options = {
          title: '',
          hAxis: {title: 'Month',  titleTextStyle: {color: '#333'}},
          vAxis: {title: 'Commits',minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }

});

$(function() {
    $("a").linkpreview({
        previewContainer: "#preview-container"
    });
    $("input").linkpreview({
        previewContainer: "#preview-container2",
        refreshButton: "#refresh-button",
        previewContainerClass: "row-fluid",
        errorMessage: "Invalid URL",
        preProcess: function() {
            console.log("preProcess");
        },
        onSuccess: function() {
            console.log("onSuccess");
        },
        onError: function() {
            console.log("onError");
        },
        onComplete: function() {
            console.log("onComplete");
        }
    });
});