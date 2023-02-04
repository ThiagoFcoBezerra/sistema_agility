from django.shortcuts import render, redirect
from cliente.models import Contato, Motivo, Relato
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def contatos(request):
    
    if 'data' in request.GET and request.GET['data']:
        if request.GET['filtro'] == 'dia':
            contatos = Contato.objects.filter(data=request.GET['data']).order_by('-data')
        if request.GET['filtro'] == 'mes':
            contatos = Contato.objects.filter(data__month=request.GET['data'][5:7]).order_by('-data')
        if request.GET['filtro'] == 'ano':
            contatos = Contato.objects.filter(data__year=request.GET['data'][0:4]).order_by('-data')
    else:
        contatos = Contato.objects.all().order_by('-data')

    if 'motivo' in request.GET and request.GET['motivo']:
        contatos = contatos.filter(motivo__id = request.GET['motivo'])
    
    if 'resultado' in request.GET and request.GET['resultado']:
        contatos = contatos.filter(resultado = request.GET['resultado'])

    if 'concluido' in request.GET and request.GET['concluido']:
        contatos = contatos.filter(concluido = request.GET['concluido'])
    
    motivos = Motivo.objects.all()
    total_contatos = contatos.count()

    contexto = {
        'contatos': contatos,
        'motivos':motivos,
        'total_contatos':total_contatos,
    }

    return render(request, 'cliente/contatos.html', contexto)

@login_required
def cria_contato(request):
    if request.method == 'POST':
        Contato.objects.create(
            cliente = request.POST['cliente'],
            motivo = Motivo.objects.get(pk = request.POST['motivo']),
        )
    return redirect('contatos')
    
@login_required
def cria_motivo(request):
    if 'descricao' in request.GET:
        Motivo.objects.create(descricao = request.GET['descricao'])
        return redirect('cria_contato')
    return render(request, 'cliente/cria_motivo.html')

@login_required
def cria_relato(request, id):
    contato_recebido = Contato.objects.get(pk = id)
    relatos = Relato.objects.filter(contato_id = id).order_by('data')
    if request.method =='POST':
        Relato.objects.create(
            usuario = User.objects.get(pk = request.user.id),
            contato = contato_recebido,
            relato = request.POST['relato']
        )
        if request.POST['data_agendamento'] != '':
            contato_recebido.data_agendamento = request.POST['data_agendamento']
        if 'concluido' in request.POST:
            contato_recebido.concluido = True
        if 'resultado' in request.POST:
            contato_recebido.resultado = request.POST['resultado']

        contato_recebido.save()
    contexto = {
        'relatos':relatos,
        'contato': contato_recebido,
    }

    return render(request, 'cliente/cria_relato.html', contexto)