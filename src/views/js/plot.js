const AXIS_MAXIMUM = 20;

function updatePlot(chart, timestamp, velocity) {
    const series = chart.series(0);
    const xAxis = chart.axisX(series);
    if (timestamp > AXIS_MAXIMUM) {
        xAxis.max = timestamp;
        xAxis.min = timestamp - AXIS_MAXIMUM;
    }
    series.append(timestamp, velocity);
}

function initSeries(chart, xAxis, yAxis, label) {
    const series = chart.createSeries(ChartView.SeriesTypeSpline, label, xAxis, yAxis);
    series.pointsVisible = true;
}

function resetPlot(chart) {
    const series = chart.series(0);
    const xAxis = chart.axisX(series);
    xAxis.min = 0;
    xAxis.max = AXIS_MAXIMUM;
    chart.removeAllSeries();
}

function setMaxVelocity(chart, velocity) {
    const series = chart.series(0);
    const yAxis = chart.axisY(series);
    yAxis.min = (velocity * -1) - 2.5;
    yAxis.max = velocity + 2.5;
}