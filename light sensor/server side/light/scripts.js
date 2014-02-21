function timedRefresh(timeout) {
    setTimeout("location.reload(true);", timeout * 60000);
    // minutes
    drawGraph(1);
    drawGraph(2);
    drawGraph(3);
    drawGraph(4);
}

function drawGraph(id) {

    var lightData = new Array();
    var label = new Array();

    $.ajax({
        url: 'fetchData.php',
        dataType: 'json',
        data: {'id':id},
        type: 'post',
        success: function(data) {
            var i = 0;
            for (row in data) {
                //document.write(data[row].time+" "+data[row].value+"<br>");
                lightData[i] = parseFloat(data[row].value);
                label[i] = data[row].time;
                i++;
            }
            var lineChartData = {
                labels: label,
                datasets: [{
                    fillColor: "rgba(151,187,205,0.5)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    data: lightData
                }, ]

                };
            var options ={
                            bezierCurve : false,
            };
            var myLine = new Chart(document.getElementById("canvas"+id.toString()).getContext("2d")).Line(lineChartData, options);

        }
    });

}
