from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
@login_required
def cadastro(request):
    erros = []
    sucesso = []
    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        login = request.POST['login']
        email = request.POST['email']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        
        if User.objects.filter(username = login).exists():
            erros.append(f'Usuário {login} já existe!')
        else:
            if senha1 == senha2:
                user = User.objects.create_user(login, email, senha1)
                user.first_name = nome
                user.last_name = sobrenome
                user.save()
                sucesso.append(f'Usuário {nome} criado com sucesso!')
            else:
                erros.append('A senha e a confirmação devem ser iguais!')
    contexto = {
        'erros' : erros,
        'sucesso': sucesso 
    }
    return render(request, 'usuarios/cadastro.html', contexto)

def login(request):
    return render(request, 'usuarios/login.html')
    
def logout(request):
    pass

@login_required
def dashboard(request):
    pass

@login_required
def usuarios(request):
    if 'busca' in request.GET:
        busca = request.GET['busca']
        usuarios = User.objects.filter(Q(first_name__icontains = busca) | Q(last_name__icontains = busca) | Q(username__icontains = busca) )
    else:
        usuarios = User.objects.all().order_by('first_name')

    contexto = {
        'usuarios':usuarios,
    }
    
    return render(request, 'usuarios/usuarios.html', contexto)

@login_required
def exclui_usuario(request, id):
    user = User.objects.get(pk = id)

    user.delete()

    return redirect('usuarios')

@login_required
def edita_usuario(request, id):
    user = User.objects.get(pk = id)
    if request.method == 'POST':
        pass

    dados = {
        'usuario': user,
    }
    return render(request, 'usuarios/edita_usuario.html', dados)