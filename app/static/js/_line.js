
const labels = [1,2,3,4];

function update_chart(chart, data, label){
    const dsColor = 'rgb(255, 99, 132)';
    const newDataset = {
        label: label,
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: dsColor,
        data: data,
        cubicInterpolationMode: 'monotone',
        tension: 0.4,
    };
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
        spanGaps: true,
    }]
};

function config_chart(labels){
    return config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: []
        },
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

