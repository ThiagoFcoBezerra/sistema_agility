
    grandeGrafico();
    function grandeGrafico(){
    const valor = document.getElementById('valor-orc');
    const soma = document.getElementById('soma');
    const nomeGrafico = document.getElementById('nome-grafico');
    var xValues = ['Orçado','Realizado'];
    var yValues = [parseFloat(valor.textContent), parseFloat(soma.textContent), 0];
    var barColors = ["green","red"];

    new Chart("grafico", {
    type: "bar",
    data: {
    labels: xValues,
    datasets: [{
        backgroundColor: barColors,
        data: yValues
    }]
    },
    options: {
    legend: {display: false},
    title: {
        display: true,
        text: nomeGrafico.textContent
    },
    scales: {
        y: {
        beginAtZero: true,
        }
    }
    }
    });
    }

miniGraficos();
function miniGraficos(){
const graficos = document.querySelectorAll(".mini-grafico")

for(let i = 0; i < graficos.length; i++){
    let valor = parseFloat(graficos[i].firstElementChild.textContent);
    valor = valor / 100;
    graficos[i].style.background = `linear-gradient(90deg, rgb(85, 80, 155) calc(${valor} * 100%), transparent 0%)`;
}
}
        
