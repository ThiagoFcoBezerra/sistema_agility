from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


# Create your views here.
@login_required
@permission_required(['auth.add_usuario', 'auth.change_usuario', 'auth.delete_usuario'])
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
@permission_required('auth.delete_usuario')
def exclui_usuario(request, id):
    user = User.objects.get(pk = id)

    user.delete()

    return redirect('usuarios')

@login_required
@permission_required('auth.change_usuario')
def edita_usuario(request, id):
    sucesso = []
    usuario = User.objects.get(pk = id)
    permissoes = Permission.objects.all()
    grupos = Group.objects.all()

    if request.method == 'POST':
        permissoes_selecionadas = request.POST.getlist('user_permissions')
        for perm in permissoes_selecionadas:
            usuario.user_permissions.add(perm)

        grupos_selecionados = request.POST.getlist('grupos')
        for grupo in grupos_selecionados:
            usuario.groups.add(grupo)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        chaves = request.POST.keys()
        for c in chaves:
            if c == 'is_staff':
                usuario.is_staff = True
                break
            else:
                usuario.is_staff = False

        for c in chaves:
            if c == 'is_active':
                usuario.is_active = True
                break
            else:
                usuario.is_active = False
        
            
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email

        usuario.save()
        sucesso.append('Usuário editado com sucesso.')

        
        

    dados = {
        'grupos': grupos,
        'usuario': usuario,
        'permissoes' : permissoes,
    }
    return render(request, 'usuarios/edita_usuario.html', dados)

@login_required
def cria_grupo(request):
    permissoes = Permission.objects.all()
    sucesso = []
    erros = []

    if request.method == 'POST':
        nome = request.POST['nome']

        grupo_existe = Group.objects.filter(name = nome)
        if grupo_existe:
            erros.append(f'O Grupo {nome} já existe')
        else:
            permissoes_selecionadas = request.POST.getlist('permissions')
            grupo = Group.objects.create(name = nome)
            for perm in permissoes_selecionadas:
                print(perm)
                grupo.permissions.add(perm)
            sucesso.append('Grupo criado com sucesso.')

    context = {
        'erros': erros,
        'sucesso': sucesso,
        'permissoes': permissoes,
    }
    return render(request, 'usuarios/form_grupo.html', context)