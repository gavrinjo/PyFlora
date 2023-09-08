
function addDataSet(chart, label, color,  data, labels) {
    const newDataset = {
        label: label,
        data: data, // Data on Y axis
        borderWidth: 1,
        backgroundColor: color,
        borderColor: color,
        cubicInterpolationMode: 'monotone',
        tension: 0.4,
        spanGaps: true,
    };
    chart.data.labels = labels;
    chart.data.datasets.push(newDataset);
    chart.update();
}

function addData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    myChart.update();
}
function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}
function removeFirstData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
}
const MAX_DATA_COUNT = 10

const ctx = document.getElementById('line').getContext('2d');
const labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
const color = 'red'
const label = 'Label'
const data3 = [12, 19, 3, 5, 2, 3]
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Chart.js Line Chart'
        }
    }
};
const dataset = [{
    label: label,
    data: data3, // Data on Y axis
    borderWidth: 1,
    cubicInterpolationMode: 'monotone',
    tension: 0.4,
    spanGaps: true,
}];
const config = {
    type: 'line',
    data: {
        labels: [], // data on X axis
        datasets: [],
    },
    options: options
};


