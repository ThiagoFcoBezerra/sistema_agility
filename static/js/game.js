graficoDosIndicadores();
atualizaBarra();

function graficoDosIndicadores(){
const indicadores = document.querySelectorAll('.banner-indicador');
for (let i = 0; i < indicadores.length; i++) {
    const orc = parseFloat(indicadores[i].childNodes[7].childNodes[1].children[0].innerText);
    const real = parseFloat(indicadores[i].childNodes[7].childNodes[3].children[0].innerText);
    const text = indicadores[i].childNodes[3].childNodes[3].childNodes[1].childNodes[1]
    const graf = indicadores[i].childNodes[3].childNodes[3].childNodes[1].childNodes[3].childNodes[3]
    let res = real / orc * 100

    text.innerText = res.toFixed(0).toString() + '%';


    if (res > 100) {
        res = 100;
    }

    graf.style.strokeDashoffset = 157 - 157 * res / 100;
    
}
}

function atualizaBarra(){
    const barra = document.querySelector('.progress-bar');
    const objetivo = document.querySelector('#obj-mensal') 
    const pontos = document.querySelector('#pts-mensal')
    
    let progresso = parseFloat(pontos.innerText) / parseFloat(objetivo.innerText) * 100;

    barra.innerText = `${(progresso.toFixed(2))}%`

    if(progresso > 100){
        progresso = 100;
    }
    barra.style.width = `${progresso}%`
    
}