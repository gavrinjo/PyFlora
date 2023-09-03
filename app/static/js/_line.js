
const labels = [1,2,3,4];

function update_chart(chart){
    const data = chart.data;
    const dsColor = 'rgb(255, 99, 132)';
    const newDataset = {
        label: 'Dataset ' + (data.datasets.length + 1),
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: dsColor,
        data: [2,4,6,8],
    };
    chart.data.labels = labels;
    chart.data.datasets.push(newDataset);
    chart.update();
};

function data(){
    return data = {
        labels: labels,
        datasets: [{
            label: 'Dataset 1',
            data: [1,2,3,4],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgb(255, 99, 132)',
        }]
    };
};

const data2 = {
    labels: labels,
    datasets: [{
        label: 'Dataset 1',
        data: [1,2,3,4],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgb(255, 99, 132)',
        cubicInterpolationMode: 'monotone',
        tension: 0.4,
    }]
};

function config_chart(){
    return config = {
        type: 'line',
        data: {},
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Line Chart'
                }
            },
        },
    }
}

function radar_chart_cfg(){
    return config = {
        type: 'radar',
        data: {},
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Line Chart'
                }
            },
            scales: { // <-- Note change in options from scale to scales
                r: {
                    grid: {
                        circular: true
                    },
                    beginAtZero: true
                }
            }
        },
    }
}