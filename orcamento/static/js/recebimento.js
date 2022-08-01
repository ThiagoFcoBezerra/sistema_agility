graficos();
corrigeDados();

function graficos(){

    const listaFatDiario = document.querySelectorAll('.fat-dia');
    const listaFatMensal = document.querySelectorAll('.fat-mes');
    const listaPagMensal = document.querySelectorAll('.pag-mes');

    const fatDiarioDados = capturaDados(listaFatDiario);
    const fatMensalDados = capturaDados(listaFatMensal);
    const pagMensalDados = capturaDados(listaPagMensal);
    const resultadoMensal = [];

    for (let i = 0; i < fatMensalDados['valores'].length; i++) {
        if (i < pagMensalDados['valores'].length){
            let resultado = fatMensalDados['valores'][i] - pagMensalDados['valores'][i];
            resultadoMensal.push(resultado);
        }
    }
    
    const ctx1 = document.getElementById('faturamento-diario').getContext('2d');
    const ChartDiario = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: fatDiarioDados['labels'],
            datasets: [{
                label: 'Faturamento por dia',
                data: fatDiarioDados['valores'],
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
        data: {
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            datasets: [{
                type: 'line',
                label: 'Receitas',
                data: fatMensalDados['valores'],
                backgroundColor: [
                    'rgba(50, 100, 255, 0.2)',
                ],
                borderColor: [
                    'rgba(50, 100, 255, 1)',
                ],
                borderWidth: 1
            },
            {
                type: 'line',
                label: 'Desembolsos',
                data: pagMensalDados['valores'],
                backgroundColor: [
                    'rgba(255, 50, 100, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 50, 100, 1)',
                ],
                borderWidth: 1
            },
            {
                type: 'bar',
                label: 'Resultado',
                data: resultadoMensal,
                backgroundColor: [
                    'rgba(50, 250, 100, 0.2)',
                ],
                borderColor: [
                    'rgba(50, 250, 100, 1)',
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
}

function habilitaEdicao(botao){
    const teste = botao.parentNode.parentNode.parentNode;
    const entradas = teste.querySelectorAll('input');
    const botaos = teste.querySelectorAll('button');
    entradas[1].attributes.removeNamedItem("readonly");
    entradas[0].attributes.removeNamedItem("readonly");
    botao.innerText = 'Salvar'
    const valorBotao1 = botao.attributes.getNamedItem("onclick");
    valorBotao1.value = 'enviaFormulario(this)';
    botaos[1].innerText = 'Cancelar'
    const valorBotao2 = botaos[1].attributes.getNamedItem("onclick");
    valorBotao2.value = 'cancela()'
    console.log(teste);
}

function enviaFormulario(botao){
    const form = botao.parentNode.parentNode.parentNode.parentNode;
    form.submit();
}

function excluir(dado){
    let confirmacao = confirm("Deseja realmente excluir o item?");
    let url = dado.attributes.value.nodeValue;

    if (confirmacao){
         location.assign(url);
     }
}

function cancela(){
    location.reload();
}

function corrigeDados(){
    datas = document.querySelectorAll('.fat-data');
    valores = document.querySelectorAll('.fat-valor');
    meses = {
        'Janeiro':'01',
        'Fevereiro':'02',
        'Março':'03',
        'Abril':'04',
        'Maio':'05',
        'Junho':'06',
        'Julho':'07',
        'Agosto':'08',
        'Setembro':'09',
        'Outubro':'10',
        'Novembro':'11',
        'Dezembro':'12'
    };

    for (let i = 0; i < datas.length; i++) {
        const dado = datas[i].attributes.value.nodeValue;
        let dadosLista = dado.split(" ");
        let dia = dadosLista[0];
        if (parseInt(dia) < 10){
            dia = '0'+ dia;
        }
        let mes = meses[dadosLista[2]];
        let ano = dadosLista[4];
        datas[i].attributes.value.nodeValue = ano+'-'+mes+'-'+dia;
    }

    for (let i = 0; i < valores.length; i++) {
        let dado = valores[i].attributes.value.nodeValue;
        dado = dado.replace(',','.');
        valores[i].attributes.value.nodeValue = dado;
    }
}

function capturaDados(listaDados){
    const labels = [];
    const valores = [];

    for (let i = 0; i < listaDados.length; i++) {
        let d = listaDados[i].children[0].innerText;
        labels.push(d);
        let v = listaDados[i].children[1].innerText;
        v = v.replace(',','.');
        v = parseFloat(v).toFixed(2);
        valores.push(v);
    }

    return {'labels': labels,'valores': valores}
}