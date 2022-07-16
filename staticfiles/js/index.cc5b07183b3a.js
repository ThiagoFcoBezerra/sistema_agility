
const usoMensal = document.getElementById('uso-mensal').innerText;
const barraMensal = document.getElementById('barra-mensal');
barraMensal.innerText = usoMensal;
barraMensal.style.width = usoMensal;

const usoAnual = document.getElementById('uso-anual').innerText;
const barraAnual = document.getElementById('barra-anual');
barraAnual.innerText = usoAnual;
barraAnual.style.width = usoAnual;

const cartoes = document.querySelectorAll('.cartao');

for (let i = 0; i < cartoes.length; i++) {
    const dados = cartoes[i].querySelectorAll('.cartao-dados');
    const saida = cartoes[i].querySelectorAll('h6');
    const graficos = cartoes[i].querySelectorAll('circle');
    const textos = cartoes[i].querySelectorAll('span');

    let orc = parseFloat(dados[0].innerText.replace(',','.'));
    let rel = parseFloat(dados[1].innerText.replace(',','.'));
    let saldo = orc - rel;

    saida[1].innerText = saldo.toFixed(2);

    let multi = rel / orc;

    if (rel == 0) {
        multi = 0;			
    }

    if (orc == 0) {
        multi = 99.9999;
    }
    multi = multi * 100;

    textos[0].innerText = multi.toFixed(2);

    if (multi > 100) {
        multi = 100;
    }

    graficos[1].style.strokeDashoffset = 189 - 189 * multi / 100;

}