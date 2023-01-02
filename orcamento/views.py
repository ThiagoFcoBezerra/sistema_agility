import datetime
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import load_workbook
from orcamento.models import Categoria, Lancamento, Orcamento, Faturamento, Autorizacao
from django.db.models.aggregates import Sum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

@login_required
def index(request):
    if request.method == 'POST':
        data_selecionada = request.POST['data']
        ano = data_selecionada[0:4]
        mes = data_selecionada[5:]
    else:
        data = datetime.datetime.now()
        ano = data.strftime("%Y")
        mes = data.strftime("%m")
        data_selecionada = f'{ano}-{mes}'
    
    lancamento_total_anual = Lancamento.objects.filter(data_pagamento__year = ano).values('data_pagamento__year').annotate(total=Sum('valor_pago'))
    orcamento_total_anual = Orcamento.objects.filter(data_orcamento__year = ano).values('data_orcamento__year').annotate(total=Sum('valor_orc'))
    lancamento_total_mensal = Lancamento.objects.filter(data_pagamento__month = mes, data_pagamento__year = ano).values('data_pagamento__month').annotate(total=Sum('valor_pago'))
    orcamento_total_mensal = Orcamento.objects.filter(data_orcamento__month = mes, data_orcamento__year = ano).values('data_orcamento__month').annotate(total=Sum('valor_orc'))
    categorias = Categoria.objects.all().order_by('nome')

    lista_dados_orc = []
    for categoria in categorias:
        lanc_mensal = Lancamento.objects.filter(categoria = categoria, data_pagamento__month = mes, data_pagamento__year = ano).values('categoria').annotate(total=Sum('valor_pago'))
        if len(lanc_mensal) == 0:
            lanc_mensal_valor = 0
        else:
            lanc_mensal_valor = round(lanc_mensal[0]['total'],2)

        orc_mensal = Orcamento.objects.filter(categoria = categoria, data_orcamento__month = mes, data_orcamento__year = ano).values('categoria').annotate(total=Sum('valor_orc'))
        if len(orc_mensal) == 0:
            orc_mensal_valor = 0
        else:
            orc_mensal_valor = round(orc_mensal[0]['total'],2)
        
        lanc_anual = Lancamento.objects.filter(categoria = categoria, data_pagamento__year = ano).values('categoria').annotate(total=Sum('valor_pago'))
        if len(lanc_anual) == 0:
            lanc_anual_valor = 0
        else:
            lanc_anual_valor = round(lanc_anual[0]['total'],2)

        orc_anual = Orcamento.objects.filter(categoria = categoria, data_orcamento__year = ano).values('categoria').annotate(total=Sum('valor_orc'))
        if len(orc_anual) == 0:
            orc_anual_valor = 0
        else:
            orc_anual_valor = round(orc_anual[0]['total'],2)
        dados_orc = {
                    'categoria_id': categoria.id,
                    'nome':categoria.nome,
                    'lanc_mensal_valor':lanc_mensal_valor,
                    'orc_mensal_valor':orc_mensal_valor,
                    'lanc_anual_valor':lanc_anual_valor,
                    'orc_anual_valor':orc_anual_valor
                    }
        lista_dados_orc.append(dados_orc)

    if len(lancamento_total_anual) == 0 or len(orcamento_total_anual) == 0:
        uso_anual = '0%'
    else:
        uso_anual = f"{round(lancamento_total_anual[0]['total'] / orcamento_total_anual[0]['total'] * 100,2)}%"
    
    if len(lancamento_total_mensal) == 0 or len(orcamento_total_mensal) == 0:
        uso_mensal = '0%'
    else:
        uso_mensal = f"{round(lancamento_total_mensal[0]['total'] / orcamento_total_mensal[0]['total'] * 100,2)}%"

    dados = {
        'lista_dados_orc':lista_dados_orc,
        'uso_anual': uso_anual,
        'uso_mensal': uso_mensal,
        'data' : data_selecionada,
        'mes':mes
    }
    return render(request, 'orcamento/index.html', dados)

@login_required
def testa_arquivo(request):

    lista_meses = {
                    "01":"Janeiro",
                    "02":"Fevereiro",
                    "03":"Março",
                    "04":"Abril",
                    "05":"Maio",
                    "06":"Junho",
                    "07":"Julho",
                    "08":"Agosto",
                    "09":"Setembro",
                    "10":"Outubro",
                    "11":"Novembro",
                    "12":"Dezembro",
                    }
    
    if request.method == 'POST':
        arquivo_teste = request.FILES['arquivo']
        mes = request.POST['mes']
       
        print(mes[5:7])

        wb = load_workbook(arquivo_teste)

        ws = wb.get_sheet_by_name(lista_meses[mes[5:7]])

        for data in ws['N']:
            if data.value != 'Data de pagamento':
                lancamentos_a_excluir = Lancamento.objects.filter(data_pagamento__month = data.value.strftime("%m"), data_pagamento__year = data.value.strftime("%Y"))
                for lancamento in lancamentos_a_excluir:
                    lancamento.delete()
                break
        
        for cell1, cell2, cell3, cell4 in zip(ws['C'], ws['D'], ws['G'], ws['N']):
            if type(cell3.value) == type(3.14) and cell1.value != None and cell2.value != None and cell4.value != None:
                
                cat = Categoria.objects.filter(nome = cell1.value)
                
                if not cat:
                    categoria = Categoria.objects.create(nome = cell1.value)
                else:
                    categoria = cat[0]
                
                valor_pago = round(cell3.value,2) 
                lanca = Lancamento.objects.create(categoria = categoria, descricao = cell2.value, valor_pago = valor_pago, data_pagamento = cell4.value)
                lanca.save()
            
    return render(request, 'orcamento/atualiza_lancamentos2.html')

@login_required
def orcamento(request):
    
    data_atual = datetime.datetime.now()
    
    if request.method == 'POST':
        data_buscada = request.POST['mes_buscado']
        mes_buscado = data_buscada[5:7]
        ano_buscado = data_buscada[0:4]
    else:
        mes_buscado = data_atual.strftime('%m')
        ano_buscado = data_atual.strftime('%Y')

    data_buscada = f'{ano_buscado}-{mes_buscado}'
    categorias = Categoria.objects.all().order_by('nome')
    orc = Orcamento.objects.filter(data_orcamento__month = mes_buscado, data_orcamento__year = ano_buscado)

    for cat in categorias:
        orcamento_existe = orc.filter(categoria = cat)
        if not orcamento_existe:
            Orcamento.objects.create(categoria = cat, valor_orc = 0, data_orcamento = f'{ano_buscado}-{mes_buscado}-01')

    orcamentos = Orcamento.objects.filter(data_orcamento__month = mes_buscado, data_orcamento__year = ano_buscado).values('categoria__nome').annotate(soma = Sum('valor_orc')).order_by('categoria__nome')
    
    for orcamento in orcamentos:
        orcamento['soma'] = float(orcamento['soma'])
        orcamento['soma'] = round(orcamento['soma'], 2)

    dados = {
        'orcamentos': orcamentos,
        'data': data_buscada
    }
    return render(request, 'orcamento/orcamento2.html', dados)
    
@login_required
@permission_required('orcamento.change_orcamento', raise_exception=True)
def cadastra_orcamento(request):
    data = request.POST['data']
    mes = int(data[5:7])
    ano = int(data[0:4])
    if request.POST.get('recorrencia'):
        mes_final = 13
    else:
        mes_final = mes+1

    for m in range(mes, mes_final):
        m = str(m)
        if len(m) < 2:
            m = '0'+m

        data = f'{ano}-{m}-01'
        
        for cat, desc, valor in zip(request.POST.getlist('categoria'), request.POST.getlist('descricao'), request.POST.getlist('valor')):
            valor = valor.replace('.','')
            valor = valor.replace(',','.')
            valor = float(valor)
            valor = round(valor,2)
            
            orc = Orcamento.objects.filter(categoria = Categoria.objects.get(nome = cat), data_orcamento = data)
            if not orc:
                Orcamento.objects.create(categoria = Categoria.objects.get(nome = cat), data_orcamento = data, descricao = desc, valor_orc = valor)
            else:
                #orc[0].categoria = Categoria.objects.get(nome = cat)
                #orc[0].data_orcamento = data
                orc[0].descricao = desc
                orc[0].valor_orc = valor
                orc[0].save()


    return redirect('index')

@login_required
def detalhes(request, id, m):

    if request.method == 'POST':
        data_selecionada = request.POST['data']
        ano = data_selecionada[0:4]
        mes = data_selecionada[5:]
        cat_id = id
    else:
        data = datetime.datetime.now()
        ano = data.strftime("%Y")
        cat_id = id
        mes = m
        if m < 10:
            mes = f'0{m}'
        data_selecionada = f'{ano}-{mes}'

    categorias = Categoria.objects.all().order_by('nome')
    categoria = categorias.get(pk = cat_id)
    lancamentos_a_exibir = Lancamento.objects.filter(categoria__id = id, data_pagamento__month = mes, data_pagamento__year = ano)
    lancamento_total_mensal = Lancamento.objects.filter(categoria__id = id, data_pagamento__year = ano).values('data_pagamento__month').annotate(total=Sum('valor_pago')).order_by('data_pagamento__month')
    orcamento_total_mensal = Orcamento.objects.filter(categoria__id = id, data_orcamento__year = ano).values('data_orcamento__month').annotate(total=Sum('valor_orc')).order_by('data_orcamento__month')

    dados = {
        'mes': mes,
        'categorias':categorias,
        'data_selecionada':data_selecionada,
        'categoria': categoria,
        'id':cat_id,
        'lancamentos_a_exibir':lancamentos_a_exibir,
        'lancamento_total_mensal':lancamento_total_mensal,
        'orcamento_total_mensal':orcamento_total_mensal,
    }
    return render(request, 'orcamento/detalhes.html', dados)

@login_required
def cadastra_faturamento(request):
    if request.method == 'POST':
        data = request.POST['data']
        valor = request.POST['valor']

        Faturamento.objects.create(faturamento_data = data, faturamento_valor = valor)
    
    return redirect('resultado')

@login_required
def resultado(request):
    if request.method == 'POST':
        data_selecionada = request.POST['data_sel']
        ano = data_selecionada[0:4]
        mes = data_selecionada[5:]
    else:
        data = datetime.datetime.now()
        ano = data.strftime("%Y")
        mes = data.strftime("%m")
    data_selecionada = f'{ano}-{mes}'

    faturamentos = Faturamento.objects.filter(faturamento_data__month = mes, faturamento_data__year = ano).order_by('faturamento_data')
    fat_dia = Faturamento.objects.filter(faturamento_data__month = mes, faturamento_data__year = ano).values('faturamento_data__day').annotate(total=Sum('faturamento_valor')).order_by('faturamento_data__day')
    fat_mes = Faturamento.objects.filter(faturamento_data__year = ano).values('faturamento_data__month').annotate(total=Sum('faturamento_valor')).order_by('faturamento_data__month')
    pag_dia = Lancamento.objects.filter(data_pagamento__month = mes, data_pagamento__year = ano).values('data_pagamento__day').annotate(total=Sum('valor_pago')).order_by('data_pagamento__day')
    pag_mes = Lancamento.objects.filter(data_pagamento__year = ano).values('data_pagamento__month').annotate(total=Sum('valor_pago')).order_by('data_pagamento__month')

    dados = {
        'faturamentos':faturamentos,
        'fat_dia':fat_dia,
        'fat_mes':fat_mes,
        'pag_dia':pag_dia,
        'pag_mes':pag_mes,
        'data_selecionada':data_selecionada,
    }

    return render(request, 'orcamento/resultado.html', dados)

@login_required
def exclui_faturamento(request, id):
    faturamento = Faturamento.objects.get(pk = id)
    faturamento.delete()

    return redirect('resultado')

@login_required
def atualiza_faturamento(request, id):
    if request.method == 'POST':
        data = request.POST['data']
        valor = request.POST['valor']

        faturamento = Faturamento.objects.get(pk=id)
        faturamento.faturamento_data = data
        faturamento.faturamento_valor = valor

        faturamento.save() 
    return redirect('resultado')

@login_required
@permission_required('orcamento.add_autorizacao')
def cria_autorizacao(request):
    if request.method == 'POST':
        categoria_id = request.POST['id']
        justificativa = request.POST['justificativa']
        valor = request.POST['valor']
        user = user = get_object_or_404(User,pk=request.user.id)
        Autorizacao.objects.create(
            categoria = Categoria.objects.get(pk = categoria_id),
            justificativa = justificativa,
            valor_autorizacao = valor,
            solicitante = user)

    return redirect('lista_autorizacao')

@login_required
def carrega_autorizacao(request, id):
    autorizacao = Autorizacao.objects.get(pk = id)
    categorias = Categoria.objects.all().order_by('nome')

    context = {
        'autorizacao': autorizacao,
        'categorias': categorias
    }

    return render(request, 'form_autorizacao.html', context)

@login_required
@permission_required('orcamento.change_autorizacao')
def edita_autorizacao(request):
    if request.method == 'POST':
        autorizacao = Autorizacao.objects.get(pk = request.POST['id'])
        autorizacao.categoria = get_object_or_404(Categoria, pk = request.POST['categoria'])
        autorizacao.justificativa = request.POST['justificativa']
        autorizacao.valor_autorizacao = request.POST['valor']
        autorizacao.solicitante = get_object_or_404(User,pk=request.user.id)
        autorizacao.save()

    return redirect('lista_autorizacao')

@login_required
@permission_required('orcamento.delete_autorizacao')
def exclui_autorizacao(request, id):

    autorizacao = Autorizacao.objects.get(pk=id)
    autorizacao.delete()

    return redirect('lista_autorizacao')

@login_required
@permission_required('orcamento.pode_despachar', raise_exception=True)
def despacha_autorizacao(request):

    if request.method == 'POST':

        autorizacao = Autorizacao.objects.get(pk=request.POST['id'])
        autorizacao.autorizacao_status = request.POST['status']
        autorizacao.despacho = request.POST['despacho']
        autorizacao.despachante = get_object_or_404(User, pk=request.user.id)
        autorizacao.save()
        return redirect('lista_autorizacao')

@login_required
def lista_autorizacao(request):
    autorizacoes = Autorizacao.objects.all().order_by('-data_criacao')
    aguardando = autorizacoes.filter(autorizacao_status = 'AGU')
    despachadas = autorizacoes.exclude(autorizacao_status = 'AGU')

    context = {
        'aguardando': aguardando,
        'despachadas': despachadas,
    }
    return render (request, 'orcamento/lista_autorizacoes.html', context)

@login_required
@permission_required('orcamento.view_autorizacao')
def detalha_autorizacao(request, id):
    autorizacao = Autorizacao.objects.get(pk = id)

    context = {
        'autorizacao': autorizacao,
    }

    return render(request, 'orcamento/autorizacao_detalhes.html', context)