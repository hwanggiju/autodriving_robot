var chart;
// 데이터 요청
function requestData() {
    $.ajax({
        // 웹페이지와 연결되는 url
        url: '/live-data',
        // 데이터가 들어오면 실행되는 함수
        success: function(point) {
            var series = chart.series[0],
                // 한 화면 그래프에 그려지는 데이터 최대 개수 20개 설정
                shift = series.data.length > 20; 
            // 다음 포인트 지정
            chart.series[0].addPoint(point, true, shift);
            // delay 1초
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}
// css 기반 그래프 x, y, 제목 등 기본 지정
$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'line',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live Motor data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Motor data',
            data: []
        }]
    });
});