
pegaData();

const cartoes = document.querySelectorAll('.cartao')
let orcamentoTotalMensal = 0
let orcamentoTotalAnual = 0
let lancamentoTotalMensal = 0
let lancamentoTotalAnual = 0

for (let i = 0; i < cartoes.length; i++) {
    const dados = cartoes[i].querySelectorAll('.cartao-dados');
    const autorizados = cartoes[i].querySelector('.autorizado');
    const mostraUso = cartoes[i].querySelector('span');
    orcamentoTotalMensal = somaValores(dados, orcamentoTotalMensal, 0)
    lancamentoTotalMensal = somaValores(dados, lancamentoTotalMensal, 1)
    orcamentoTotalAnual =somaValores(dados, orcamentoTotalAnual, 2)
    lancamentoTotalAnual =somaValores(dados, lancamentoTotalAnual, 3)
    
    cartoes[i].querySelector('.saldo').innerText = calculaSaldo(dados)
    const graf = cartoes[i].querySelectorAll('circle')
    let uso = calculaUso(dados)

    mostraUso.innerText = uso.toFixed(2);
    if (uso >= 100) {
        uso = 100;
    }
    graf[2].style.strokeDashoffset = 189 - 189 * uso /100
    
    let usoComAutorizado = calculaUsoComAutorizado(dados, autorizados)
    if (usoComAutorizado >= 100) {
        usoComAutorizado = 100;                
    }
    graf[1].style.strokeDashoffset = 189 - 189 * usoComAutorizado /100
}

const barraMensal = document.querySelector('#barra-mensal');
let valorUsoMensal = lancamentoTotalMensal / orcamentoTotalMensal * 100;
if (valorUsoMensal > 100) {
    valorBarraMensal = 100
} else {
    valorBarraMensal = valorUsoMensal;
}
barraMensal.style.width = `${valorBarraMensal}%`
barraMensal.innerText = valorUsoMensal.toFixed(2)

const barraAnual = document.querySelector('#barra-anual');
let valorUsoAnual = lancamentoTotalAnual / orcamentoTotalAnual * 100;
if (valorUsoAnual > 100) {
    valorBarraAnual = 100
} else {
    valorBarraAnual = valorUsoAnual;
}
barraAnual.style.width = `${valorBarraAnual}%`
barraAnual.innerText = valorUsoAnual.toFixed(2)

function somaValores(dados, soma, indice) {
    let valor = '0,00'
    if(dados[indice].innerText != ''){
        valor = dados[indice].innerText;
    } else {
        dados[indice].innerText = '0,00'
    }


    valor = valor.replace(',','.');
    soma = soma + parseFloat(valor);
    return soma
    
}

function calculaSaldo(dados) {
    let saldo = 0;
    if (dados[0].innerText != '' && dados[1].innerText != '') {
        valor1 = dados[0].innerText;
        valor1 = valor1.replace(',','.');
        valor2 = dados[1].innerText;
        valor2 = valor2.replace(',','.');

        saldo = parseFloat(valor1) - parseFloat(valor2)
        
    } else {
        saldo = 0;
    }

    return saldo = saldo.toLocaleString("pt-BR", {style:"currency", currency:"BRL"});


}
function calculaUso(dados) {
    let uso = 0;
    if (dados[0].innerText != '' && dados[1].innerText != '') {
        valor1 = dados[0].innerText;
        valor1 = valor1.replace(',','.');
        valor2 = dados[1].innerText;
        valor2 = valor2.replace(',','.');

        uso = parseFloat(valor2) / parseFloat(valor1) * 100
        
    } else {
        uso = 0;
    }

    return uso;


}

function calculaUsoComAutorizado(dados, autorizado) {
    let uso = 0;
    if (dados[0].innerText != '' && dados[1].innerText != '' && autorizado.innerText != '') {
        valor1 = dados[0].innerText;
        valor1 = valor1.replace(',','.');
        valor2 = dados[1].innerText;
        valor2 = valor2.replace(',','.');
        valor3 = autorizado.innerText;
        valor3 = valor3.replace(',','.');

        uso = (parseFloat(valor2) + parseFloat(valor3)) / parseFloat(valor1) * 100
        
    } else {
        uso = 0;
    }

    return uso;


}

function pegaData(){
    let dataDados = document.getElementById('data');
    let mostraMes = document.getElementById('mes');
    let mostraAno = document.getElementById('ano');
    let meses = ['Janeiro',
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
            ]
    let ano = dataDados.value.slice(0,4);
    let valorMes = parseInt(dataDados.value.slice(5,));


    mostraMes.innerText = `Mes: ${meses[valorMes - 1]}`;
    mostraAno.innerText = `Ano: ${ano}`; 
}