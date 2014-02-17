function timedRefresh(timeout) {
    setTimeout("location.reload(true);", timeout * 60000);
    // minutes
    drawGraph();
}

function drawGraph() {

    var lightData = new Array();
    var label = new Array();

    $.ajax({
        url: 'fetchData.php',
        dataType: 'json',
        success: function(data) {
            var i = 0;
            for (row in data) {
                //document.write(data[row].timestamp+" "+data[row].value+"<br>");
                lightData[i] = data[row].value;
                label[i] = data[row].timestamp;
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

                }
            var myLine = new Chart(document.getElementById("canvas").getContext("2d")).Line(lineChartData);

        }
    });

}
