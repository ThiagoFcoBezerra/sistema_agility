const ctx1 = document.getElementById('faturamento-diario').getContext('2d');
const ChartDiario = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['01/06', '02/06', '03/06', '04/06', '05/06', '07/06'],
        datasets: [{
            label: 'Faturamento por dia',
            data: [1556, 2356, 2897, 2896, 1245, 1872],
            backgroundColor: [
                'rgba(50, 255, 100, 0.2)',
            ],
            borderColor: [
                'rgba(50, 255, 100, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx2 = document.getElementById('faturamento-anual').getContext('2d');
const ChartAnual = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        datasets: [{
            label: 'Realizado',
            data: [1556, 2356, 2897, 2896, 1245, 1872],
            backgroundColor: [
                'rgba(50, 100, 255, 0.2)',
            ],
            borderColor: [
                'rgba(50, 100, 255, 1)',
            ],
            borderWidth: 1
        },
        {
            label: 'Orçado',
            data: [2568, 1458, 2478, 1998, 1496, 2141],
            backgroundColor: [
                'rgba(255, 50, 100, 0.2)',
            ],
            borderColor: [
                'rgba(255, 50, 100, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});