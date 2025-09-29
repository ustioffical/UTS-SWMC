AppGraphModel = function () {

    let me = this;
    me.appConstructor = function () {

    };

    me.DisplayStackBarGraph_ComparisonWithValue = function (div_id, SeriesData, Hierarchy) {
        Highcharts.chart(div_id, {

            chart: {
                type: 'column'
            },

            title: {
                text: ''
            },

            legend: {
                align: 'center',
                verticalAlign: 'bottom',
                layout: 'horizontal'
            },

            xAxis: {
                categories: Hierarchy,
                labels: {
                    x: -10
                }
            },

            yAxis: {
                allowDecimals: false,
                title: {
                    text: 'Containers'
                }
            },

            credits: {
                enabled: false
            },

            series: SeriesData,

        });
    }

}