dados = atualizaTabela();
grafico(dados[0], dados[1]);

function atualizaData(){
const data = document.getElementById('data');
let d = new Date();

data.value = d.toLocaleString();
}


function grafico(orcado, realizado) {
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            datasets: [{
                label: 'Orçado',
                data: orcado,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            },{
                label: 'Realizado',
                data: realizado,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
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

function atualizaTabela() {
    tabela = document.querySelector('table').children[1].children;
    orcado = document.querySelectorAll('.orcado');
    realizado = document.querySelectorAll('.real');
    lista_orcado = [];
    lista_realizado = [];
    
    for (let i = 0; i < orcado.length; i++) {
        let mes = parseInt(orcado[i].children[0].innerText);
        let valor = parseFloat(orcado[i].children[1].innerText)
        tabela[mes-1].children[1].innerText = valor.toLocaleString('pt-BR', {style:"currency", currency:"BRL"});
    }

    for (let i = 0; i < realizado.length; i++) {
        let mes = parseInt(realizado[i].children[0].innerText);
        let valor = parseFloat(realizado[i].children[1].innerText);
        tabela[mes-1].children[2].innerText = valor.toLocaleString('pt-BR', {style:"currency", currency:"BRL"});        
    }

    for (let i = 0; i < 12; i++) {
        let orc = tabela[i].children[1].innerText;
        orc = orc.replace('R$','');
        orc = orc.replace('.','');
        orc = orc.replace(',','.');
        orc = parseFloat(orc);

        let real = tabela[i].children[2].innerText;
        real = real.replace('R$','');
        real = real.replace('.','');
        real = real.replace(',','.');
        real = parseFloat(real);

        let saldo = orc - real;
        if (!(isNaN(saldo))){
            tabela[i].children[3].innerText = saldo.toLocaleString('pt-BR', {style:"currency", currency:"BRL"}); 
        }
    }
    
    ultimaPosicao = parseInt(realizado[realizado.length-1].children[0].innerText);
    for (let i = 0; i < ultimaPosicao; i++) {
        let valor = tabela[i].children[2].innerText;
        valor = valor.replace('R$','');
        valor = valor.replace('.','');
        valor = valor.replace(',','.');
        valor = parseFloat(valor);
        lista_realizado.push(valor);
        
    }

    ultimaPosicao = parseInt(orcado[orcado.length-1].children[0].innerText);
    for (let i = 0; i < ultimaPosicao; i++) {
        let valor = tabela[i].children[1].innerText;
        valor = valor.replace('R$','');
        valor = valor.replace('.','');
        valor = valor.replace(',','.');
        valor = parseFloat(valor);
        lista_orcado.push(valor);
        
    }
    return [lista_orcado, lista_realizado]; 
}

