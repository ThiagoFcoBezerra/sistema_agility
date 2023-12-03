  document.getElementById("form-entrada").addEventListener("input", mostraGrafico);
    const entradasRotulos = document.querySelectorAll("#categoria");
    const rotulos = [];
    for (let i = 0; i < entradasRotulos.length; i++){
        rotulos.push(entradasRotulos[i].value);
    }

clicado();
mostraGrafico();
function mostraGrafico(){

    
  const teste = document.querySelectorAll(".entrada");
  var soma = 0.0;
  var numero = 0.0;
  const valores = [];
  for (let i = 0; i < teste.length; i++){
    if (teste[i].value){
      numero = teste[i].value;
      numero = numero.replace(".", "");
      numero = numero.replace(",", ".");
      numero = parseFloat(numero);
    } else {
      numero = 0;
    }
    if (valores[i]){
      valores[i] = numero;
    } else {
      valores.push(numero);
    }
    soma = soma + numero;
  } 
  document.getElementById("resultado").textContent = soma.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
  const divGraf = document.getElementById("grafico");
  divGraf.removeChild(divGraf.children[1]);
  const novoGraf = document.createElement("canvas");
  novoGraf.id = "myChart";
  divGraf.appendChild(novoGraf);
  grafico(valores, rotulos);
}


function grafico(valores, rotulos){
  

  const data = {
    labels: rotulos,
    datasets: [{
      label: 'My First dataset',
      backgroundColor: ['rgb(255, 0, 0)',
                        'rgb(0, 255, 0)',
                        'rgb(0, 0, 255)',
                        'rgb(255, 150, 0)',
                        'rgb(0, 255, 150)',
                        'rgb(150, 0, 255)',
                        'rgb(255, 100, 0)',
                        'rgb(100, 255, 0)',
                        'rgb(0, 100, 255)',
                        'rgb(255, 150, 100)',
                        'rgb(100, 255, 150)',
                        'rgb(150, 100, 255)',
                        'rgb(200, 0, 0)',
                        'rgb(0, 200, 0)',
                        'rgb(0, 0, 200)',
                        'rgb(200, 150, 0)',
                        'rgb(0, 200, 150)',
                        'rgb(150, 0, 200)',
                        'rgb(200, 100, 0)',
                        'rgb(100, 200, 0)',
                        'rgb(0, 100, 200)',
                        'rgb(200, 150, 100)',
                        'rgb(100, 200, 150)',
                        'rgb(150, 100, 200)'
                       ],
      //borderColor: 'rgb(255, 99, 132)',
      data: valores
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
    options: {}
  };
  
  const myChart = new Chart(
    document.getElementById('myChart'),
    config
  );
}

function converte(valor){
  var v = valor.value.replace(/\D/g,'');
	v = (v/100).toFixed(2) + '';
	v = v.replace(".", ",");
	v = v.replace(/(\d)(\d{3})(\d{3}),/g, "$1.$2.$3,");
	v = v.replace(/(\d)(\d{3}),/g, "$1.$2,");
	valor.value = v;
}

function clicado(){
  const mesSelecionado = document.querySelector("#mes")
  const menuMes = document.querySelectorAll(".link")
  for(let i = 0; i <= menuMes.length; i++){
    if(mesSelecionado.value == i){
      menuMes[i-1].classList.add("clicado");
    }
  }
    
}
