
grandeGrafico();
miniGraficos();
graficoAnual();

function getTotal(elementos){
    const listaTotal = [];
    const valores = document.querySelectorAll(elementos);
    for (let i = 0; i < valores.length; i++) {
        let valor = parseFloat(valores[i].textContent.replace(',','.'));
        valor = parseFloat(valor.toFixed(2));
        listaTotal.push(valor);     
    }
    return listaTotal;
}
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

function miniGraficos(){
const graficos = document.querySelectorAll(".mini-grafico")

for(let i = 0; i < graficos.length; i++){
    let valor = parseFloat(graficos[i].firstElementChild.textContent);
    valor = valor / 100;
    graficos[i].style.background = `linear-gradient(90deg, rgb(85, 80, 155) calc(${valor} * 100%), transparent 0%)`;
}
}
function graficoAnual(){
    const labels = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
      ];
    
      const data = {
        labels: labels,
        datasets: [{
          label: 'Orçado',
          fill: false,
          borderColor: 'rgb(0,255,255)',
          data: getTotal('.total-orc'),
          tension: 0.1
        },{
          label: 'Realizado',
          fill: false,
          borderColor: 'rgb(255,99,71)',
          data: getTotal('.total-lanc'),
          tension: 0.1
        }]
      };
    
      const config = {
        type: 'line',
        data: data,
        options: {}
      };
      const grafico = new Chart(
        document.getElementById('myChart'),
        config
      );   
}