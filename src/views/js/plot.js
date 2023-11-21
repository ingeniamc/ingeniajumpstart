var series;
const AXIS_MAXIMUM = 20;

function updatePlot(timestamp, velocity, xAxis) {
    if (timestamp > AXIS_MAXIMUM) {
        xAxis.max = timestamp;
        xAxis.min = timestamp - AXIS_MAXIMUM;
    }
    series.append(timestamp, velocity);
}

function initPlot(chart, xAxis, yAxis) {
    series = chart.createSeries(ChartView.SeriesTypeSpline, "spline", xAxis, yAxis);
    series.pointsVisible = true;
}

function resetPlot(chart, xAxis) {
    xAxis.min = 0;
    xAxis.max = AXIS_MAXIMUM;
    chart.removeAllSeries();
}