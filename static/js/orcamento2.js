defineCor();
teste();
function teste(){

	const barras = document.querySelectorAll('.progress-bar');
	const entradas = document.querySelectorAll('.entrada-valor');
	const resultado = document.getElementById('resultado');

	let total = 0;

	for(let i = 0; i < entradas.length; i++){
		let valorEntrada = 0
	
		if (entradas[i].value.length == 0){
			valorEntrada = 0;
		} else {
			valorEntrada = parseFloat(entradas[i].value.replace(",","."));	
		}
		total = total + valorEntrada;
	}
	resultado.innerText = total.toLocaleString("pt-BR", {style:"currency", currency:"BRL"});

	for(let i = 0; i < entradas.length; i++){
		let valor = 0
		if (entradas[i].value.length > 0){
			valor = parseFloat(entradas[i].value.replace(",","."));	
		}

		valor = valor * 100 / total;
		barras[i].style.width = valor + '%';
		barras[i].innerText = valor.toFixed(2) + '%';
	}

}
function defineCor(){

	const marcadores = document.querySelectorAll('.marca');
	const barras = document.querySelectorAll('.progress-bar');

	for (let i = 0; i < marcadores.length; i++) {

    let cor = generateColor();

		marcadores[i].style.background = cor;
	  barras[i].style.background = cor;

	}
}

function generateColor() {

  const letters = '0123456789ABCDEF';
  let color = '#';
  
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  
  return color;
  
}
