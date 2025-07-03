import datetime
from datetime import timedelta
from PIL import Image
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count
from django.contrib.auth.models import User
from almox.models import Produto, Categoria, Marca, Fornecedor, Unidade, Localizacao, Pedido, ItemPedido, ItemProduto, Movimentacao

def pedidos(request):
    pedidos_a_despachar = Pedido.objects.filter(status = 'AGU')
    pedidos_despachados = Pedido.objects.filter(Q(status = 'DEF') | Q(status = 'IND') | Q(status = 'ENT'), recebido = False)
        
    contexto = {
        'pedidos_a_despachar': pedidos_a_despachar,
        'pedidos_despachados': pedidos_despachados
    }
    
    return render(request, 'almox/pedidos.html', contexto)

def produtos(request):
    
    produtos = Produto.objects.filter(status = 'A').values('id', 'imagem', 'nome', 'descricao',quant = Count('itemproduto', filter=Q(itemproduto__situacao = 'EST') & Q(itemproduto__localizacao__principal = True)))

    contexto = {
        'produtos': produtos
    }
    return render(request, 'almox/produtos.html', contexto)

def cadastra_produto(request):
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    fornecedores = Fornecedor.objects.all()
    unidades = Unidade.objects.all()
    locais = Localizacao.objects.all()
    
    if request.POST.__contains__('status'):
        status_produto = 'A'
    else:
        status_produto = 'I'
       
    if request.method == 'POST':
        imagem_produto = request.FILES['imagem']     
        data = datetime.datetime.now()
        code_bar = f'{data.strftime("%Y")}{data.strftime("%m")}{data.strftime("%d")}{data.strftime("%H")}{data.strftime("%M")}{data.strftime("%S")}'
        Produto.objects.create(
            nome = request.POST['nome'],
            descricao = request.POST['descricao'],
            categoria = get_object_or_404(Categoria, pk = int(request.POST['categoria'])),
            marca = get_object_or_404(Marca, pk = int(request.POST['marca'])),
            quantidade_minima = request.POST['quantidade_minima'],
            unidade = get_object_or_404(Unidade, pk = int(request.POST['unidade'])),
            status = status_produto,
            imagem = imagem_produto,
            observacao = request.POST['observacao'],
            cod_bar = code_bar
        )
        return redirect('produtos')
    
    contexto= {
        'categorias': categorias,
        'marcas': marcas,
        'fornecedores': fornecedores,
        'unidades': unidades,
        'locais': locais,
    }
    return render(request, 'almox/cadastro.html', contexto)

def edita_produto(request, id):
    produto = Produto.objects.get(pk = id)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    fornecedores = Fornecedor.objects.all()
    unidades = Unidade.objects.all()
    locais = Localizacao.objects.all()
    mensagens = []
    
    if request.POST.__contains__('status'):
        status_produto = 'A'
    else:
        status_produto = 'I'
       
    if request.method == 'POST':
        imagem = request.POST.get('imagem', False)
        if imagem:   
            produto.imagem = imagem
        produto.nome = request.POST['nome']
        produto.descricao = request.POST['descricao']
        produto.categoria = get_object_or_404(Categoria, pk = int(request.POST['categoria']))
        produto.marca = get_object_or_404(Marca, pk = int(request.POST['marca']))
        produto.quantidade_minima = request.POST['quantidade_minima']
        produto.unidade = get_object_or_404(Unidade, pk = int(request.POST['unidade']))
        produto.status = status_produto
        produto.observacao = request.POST['observacao']
        produto.save()
        mensagens.append('Produto Editado com Sucesso!')
        
    
    contexto = {
        'mensagens': mensagens,
        'produto': produto,
        'categorias': categorias,
        'marcas': marcas,
        'fornecedores': fornecedores,
        'unidades': unidades,
        'locais': locais,
    }
    
    return render(request, 'almox/edita_produto.html', contexto)

def cadastra_pedido(request, id):
    dados_produto = Produto.objects.filter(pk = id).values('id', 'imagem', 'nome', 'descricao', 'unidade__sigla',quant = Count('itemproduto', filter=Q(itemproduto__situacao = 'EST') & Q(itemproduto__localizacao__principal = True)))
    usuario = get_object_or_404(User, pk = request.user.id)
    pedido_atual = Pedido.objects.get_or_create(usuario_pedido = usuario, status = 'ABE')
    itens = ItemPedido.objects.filter(pedido = pedido_atual[0])
    mensagens = []
    if request.method == 'POST':
        if int(request.POST['quantidade']) <= int(dados_produto[0]['quant']):
            
            for i in range(int(request.POST['quantidade'])):
                ItemPedido.objects.create(
                    pedido = pedido_atual[0], 
                    produto = get_object_or_404(Produto, pk = id))
        else:
            mensagens.append('quantidade não disponível!')
    
    contexto = {
        'itens': itens,
        'dados_produto':dados_produto,
        'pedido_atual': pedido_atual[0],
        'mensagens': mensagens
    }
    
    return render(request, 'almox/cadastra_pedido.html', contexto)

def fecha_pedido(request, id):
    pedido = get_object_or_404(Pedido, pk = id)
    pedido.status = 'AGU'
    pedido.save()
    
    return redirect('produtos')

def despacha_pedido(request, id):
    pedido = get_object_or_404(Pedido, pk = id)
    itens = ItemPedido.objects.filter(pedido = pedido)
    user = get_object_or_404(User, pk = request.user.id)
    alertas = []
    mensagens = []
    if request.method == 'POST':
        if user.has_perm('despachar'):
            despacho = request.POST['despacho']
            pedido.status = despacho
            pedido.data_despacho = datetime.datetime.now()
            pedido.usuario_despacho = User.objects.get(pk = request.user.id)
            pedido.save()
            mensagens.append('Pedido Despachado com sucesso!')
            return redirect('pedidos')
        else:
            alertas.append('Usuário sem acesso. Solicite ao administrador')
    contexto = {
        'alertas': alertas,
        'mensagens': mensagens,
        'pedido': pedido,
        'itens': itens,
        
    }
    return render(request, 'almox/despacha_pedido.html', contexto)

def entrega_pedido(request, id):
    alertas = []
    mensagens = []
    habilita = True
    pedido = get_object_or_404(Pedido, pk = id)
    itens_pedido = ItemPedido.objects.filter(pedido = pedido, entregue = False)
    local_destino = Localizacao.objects.filter(responsavel = pedido.usuario_pedido)
    lista = []

    if not pedido.status == 'DEF':
        habilita = False
        alertas.append('Pedido não está deferido')

            
    if request.method == 'POST':
        if request.user.has_perm('entregar'):
            destino = Localizacao.objects.get(pk= request.POST['local'])
            item_pedido = ItemPedido.objects.get(pk = request.POST['item'])
            item_produto = ItemProduto.objects.get(pk = request.POST['item_produto'])
            origem = get_object_or_404(Localizacao, pk = item_produto.localizacao_id)
            item_pedido.entregue = True
            item_pedido.save()
            item_produto.localizacao = destino
            item_produto.save()
            itens_pedido = ItemPedido.objects.filter(pedido = pedido, entregue = False)
            Movimentacao.objects.create(
                item_produto = item_produto,
                usuario = request.user,
                tipo_movimento = 'T',
                responsavel = pedido.usuario_pedido,
                local_origem = origem,
                local_destino = destino
                )
            mensagens.append('Item Entregue!')
        else:
            alertas.append('Usuário sem acesso. Solicite ao administrador.')
            
        
    for i in itens_pedido:
        item_prod = ItemProduto.objects.filter(situacao = 'EST', produto = i.produto, localizacao__responsavel = request.user, localizacao__principal = True)
        lista.append(item_prod)
    
    if not itens_pedido.exists():
        pedido.status = 'ENT'
        pedido.data_entrega = datetime.datetime.now()
        pedido.usuario_entrega = request.user
        pedido.save()
        
        mensagens.append('Todos os itens do pedido foram entregues!')
                    
    contexto = {
        'mensagens': mensagens,
        'local_destino': local_destino,
        'pedido':pedido,
        'itens_pedido':itens_pedido,
        'lista':lista,
        'alertas': alertas,
        'habilita': habilita
    }
    
    return render(request, 'almox/entrega_pedido.html', contexto)

def recebe_pedido(request, id):
    pedido = Pedido.objects.get(pk = id, status = 'ENT')
    itens = ItemPedido.objects.filter(pedido = pedido, entregue = True)
    alertas = []
    mensagens = []
    
    if request.GET.get('acao', '') == 'receber':
        if request.user == pedido.usuario_pedido:
            pedido.recebido = True
            pedido.save()
            return redirect('pedidos')
        else:
            alertas.append('Pedido não pertence ao usuário.')

    contexto = {
        'alertas': alertas,
        'mensagens': mensagens,
        'pedido': pedido,
        'itens': itens
    }
    
    return render(request, 'almox/recebe_pedido.html', contexto)

def entrada_item_produto(request, id):
    produto = get_object_or_404(Produto, pk = int(id))
    locais = Localizacao.objects.all()
    fornecedores = Fornecedor.objects.all()
    mensagens = []
    dados_form = {}
    
    
    if request.method == 'POST':
        data_aquisicao = datetime.date(int(request.POST['data_aquisicao'][0:4]),int(request.POST['data_aquisicao'][5:7]),int(request.POST['data_aquisicao'][8:]))
        tempo_garantia = timedelta(days = +int(request.POST['garantia']))
        data_garantia = data_aquisicao + tempo_garantia
        
        item = ItemProduto.objects.create(
        produto = produto,
        data_aquisicao = data_aquisicao,
        data_entrada = datetime.datetime.now(),
        data_situacao = datetime.datetime.now(),
        data_garantia = data_garantia,
        numero_serie = request.POST['num_serie'],
        situacao = 'EST',
        localizacao = get_object_or_404(Localizacao, pk = int(request.POST['local'])),
        fornecedor = get_object_or_404(Fornecedor, pk = request.POST['fornecedor']),
        custo = request.POST['custo']
        )
        Movimentacao.objects.create(
                item_produto = item,
                data = datetime.datetime.now(),
                usuario = request.user,
                tipo_movimento = 'E',
                responsavel = request.user.username,
                local_origem = item.localizacao, 
                local_destino = item.localizacao
                )
        
        
        mensagem = 'Item incluído com sucesso!'
        mensagens.append(mensagem)
        
        if 'fixa' in request.POST:
            dados_form.update({'data_aquisicao': request.POST['data_aquisicao']})
            dados_form.update({'garantia': request.POST['garantia']})
            dados_form.update({'local': request.POST['local']})
            dados_form.update({'fornecedor': request.POST['fornecedor']})
            dados_form.update({'custo': request.POST['custo']})
            dados_form.update({'fixa': 'fixa'})
        
    
    contexto = {
        'dados_form': dados_form,
        'produto': produto,
        'locais': locais,
        'fornecedores': fornecedores,
        'mensagens': mensagens
    }
    
    return render (request, 'almox/cadastro_item.html', contexto)

def move_itens(request, id):
    item = ItemProduto.objects.get(pk = id)
    mensagens = []
    alertas = []
    sucesso = False
    usuario_movimenta = request.user
    
    
    if request.method == 'POST':
        if request.user == item.localizacao.responsavel:
            responsavel_destino = request.POST['responsavel']
            
            destino = Localizacao.objects.get_or_create(local = responsavel_destino, responsavel = usuario_movimenta, producao = True)
            
            Movimentacao.objects.create(
                item_produto = item,
                data = datetime.datetime.now(),
                usuario = usuario_movimenta,
                tipo_movimento = 'A',
                responsavel = responsavel_destino,
                local_origem = item.localizacao, 
                local_destino = destino[0],
                )
            
            item.situacao = 'PRO'
            item.localizacao = destino[0]
            item.data_situacao = datetime.datetime.now()
            item.save()
            mensagens.append('Item alterado com sucesso.')
            sucesso = True           
        else:
            alertas.append('Usuário não é o responsável.')
    contexto = {
        'alertas': alertas,
        'mensagens': mensagens,
        'item': item,
        'sucesso': sucesso
    } 
    
    return render(request, 'almox/move_itens.html', contexto)

def recupera_itens(request, id):
    item = ItemProduto.objects.get(pk = id)
    mensagens = []
    alertas = []
    sucesso = False
    usuario_movimenta = request.user
    locais = Localizacao.objects.filter(responsavel = usuario_movimenta, producao = False)
    
    
    if request.method == 'POST':
        
        destino = get_object_or_404(Localizacao, pk = request.POST['local'])
        
        Movimentacao.objects.create(
            item_produto = item,
            data = datetime.datetime.now(),
            usuario = usuario_movimenta,
            tipo_movimento = 'A',
            responsavel = usuario_movimenta.username,
            local_origem = item.localizacao, 
            local_destino = destino,
            )
        
        item.situacao = 'EST'
        item.localizacao = destino
        item.data_situacao = datetime.datetime.now()
        item.save()
        mensagens.append('Item alterado com sucesso.')
        sucesso = True           
    
    contexto = {
        'locais' : locais,
        'alertas': alertas,
        'mensagens': mensagens,
        'item': item,
        'sucesso': sucesso
    } 
    
    return render(request, 'almox/recupera_itens.html', contexto)

def lista_itens(request, id):
    lista = ItemProduto.objects.filter(produto_id = id)
    
    if request.GET.__contains__('busca'):
        lista = ItemProduto.objects.filter(numero_serie__icontains = request.GET['busca'])
    
    contexto = {
    'lista': lista    
    }
    return render(request, 'almox/lista_itens.html', contexto )

def cadastra_categoria(request):
    
    if request.method == 'POST':
        Categoria.objects.create(nome = request.POST['nome'])
        
        return redirect('cadastro')
    
    return render(request, 'almox/cadastra_categoria.html')

def cadastra_marca(request):
    if request.method == 'POST':
        Marca.objects.create(nome = request.POST['nome'])
        return redirect('cadastro')
    return render(request, 'almox/cadastra_marca.html')

def cadastra_unidade(request):
    if request.method == 'POST':
        Unidade.objects.create(nome = request.POST['nome'], sigla = request.POST['sigla'])
        return redirect('cadastro')
    return render(request, 'almox/cadastra_unidade.html')

def cadastra_local(request):
    usuarios = User.objects.filter()
    mensagens = []
    
    if 'busca' in request.GET:
        usuarios = usuarios.filter(username__icontains = request.GET['busca'])
    
    if 'id_usuario' in request.GET:
        usuarios.get(pk = request.GET['id_usuario'])
        
    if request.method == 'POST':
        usuario = get_object_or_404(User, pk = request.POST['responsavel'])
        teste_principal = False
        if 'principal' in request.POST:
            teste_principal = True
            
        Localizacao.objects.create(responsavel = usuario, local = request.POST['local'], principal = teste_principal)
        mensagens.append('Local cadastrado com sucesso!')    
    
    contexto = {
        'usuarios': usuarios,
        'mensagens': mensagens,
    }
    return render(request, 'almox/cadastra_local.html', contexto)

def detalha_local(request, id):
    local = Localizacao.objects.get(pk = id)
    itens_produtos = ItemProduto.objects.filter(localizacao = local).exclude(situacao = 'PRO')
    
    contexto = {
        'local': local,
        'itens_produtos': itens_produtos
    }
    
    return render(request, 'almox/detalha_local.html', contexto)

def lista_locais(request):
    locais = Localizacao.objects.all().exclude(producao = True)
    
    
    contexto = {
        'locais': locais
    }
    
    return render(request, 'almox/lista_locais.html', contexto)

def cadastra_fornecedor(request):
    mensagens = []
    
    if request.method == 'POST':
        Fornecedor.objects.create(nome = request.POST['nome'])
        mensagens.append('Fornecedor cadastrado com sucesso!')
        
        
    contexto = {
        'mensagens':mensagens,
    }
    
    return render(request, 'almox/cadastra_fornecedor.html', contexto)

def lista_movimento(request, id):
    movimentos = Movimentacao.objects.filter(item_produto_id = id).order_by('-data')
    
    
    contexto = {
        'movimentos': movimentos,
        'id': id
    }
    
    return render(request, 'almox/lista_movimento.html', contexto)
