import datetime
from django.shortcuts import render
from openpyxl import load_workbook
from orcamento.models import Categoria, Lancamento, Orcamento
from django.db.models.aggregates import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):

    return render(request, 'index.html')

@login_required
def testa_arquivo(request):
    arquivo_teste = request.FILES['arquivo']
    mes = request.POST['mes']

    wb = load_workbook(arquivo_teste)

    ws = wb.get_sheet_by_name(mes)

    for data in ws['N']:
        if data.value != 'Data de pagamento':
            print(data.value.strftime("%m"))
            lancamentos_a_excluir = Lancamento.objects.filter(data_pagamento__month = data.value.strftime("%m"))
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
            
    return render(request, 'index.html')

@login_required
def exibir_lancamentos(request):
    cat = Categoria.objects.first()
    mes_sel = datetime.datetime.now()
    context = exibir(cat.id, int(mes_sel.strftime("%m")))
    return render(request, 'exibe.html', context)

@login_required
def exibir_lancamentos2(request, var1, var2):
    item_indice = var1
    mes_sel = var2
    context = exibir(item_indice, mes_sel)
    
    return render(request, 'exibe.html', context)

@login_required
def orcamento(request, var1):
    if not var1:
        mes_buscado = 1
    else:
        mes_buscado = var1

    categorias = Categoria.objects.all().order_by('nome')
    orcamentos = Orcamento.objects.filter(data_orcamento__month = mes_buscado).values('categoria__nome').annotate(soma = Sum('valor_orc')).order_by('categoria__nome')
    
    for orcamento in orcamentos:
        orcamento['soma'] = float(orcamento['soma'])
        orcamento['soma'] = round(orcamento['soma'], 2)

    dados = {
        'categorias' : categorias,
        'orcamentos': orcamentos,
        'mes': var1
    }
    return render(request, 'orcamento.html', dados)

@login_required
def cadastra_orcamento(request):
    mes = request.POST['mes']
    mes = int(mes)
    if request.POST.get('recorrencia'):
        mes_final = 13
    else:
        mes_final = mes+1

    for m in range(mes, mes_final):

        data = f'2022-{m}-01'
        
        for cat, desc, valor in zip(request.POST.getlist('categoria'), request.POST.getlist('descricao'), request.POST.getlist('valor')):
            valor = valor.replace('.','')
            valor = valor.replace(',','.')
            valor = float(valor)
            valor = round(valor,2)
            orc = Orcamento.objects.filter(categoria = Categoria.objects.get(nome = cat), data_orcamento = data)
            if not orc:
                Orcamento.objects.create(categoria = Categoria.objects.get(nome = cat), data_orcamento = data, descricao = desc, valor_orc = valor)
            else:
                orc[0].categoria = Categoria.objects.get(nome = cat)
                orc[0].data_orcamento = data
                orc[0].descricao = desc
                orc[0].valor_orc = valor
                orc[0].save()


    return render(request, 'index.html')

def exibir(item_indice, mes_sel):
    lancamentos_exibir = Lancamento.objects.filter(categoria__id = item_indice, data_pagamento__month = mes_sel)                              
    orcamentos = Orcamento.objects.filter(categoria__id = item_indice, data_orcamento__month = mes_sel)
    lancamento_total_mensal = Lancamento.objects.filter(data_pagamento__year = 2022).values('data_pagamento__month').annotate(total=Sum('valor_pago')).order_by('data_pagamento__month')
    orcamento_total_mensal = Orcamento.objects.filter(data_orcamento__year = 2022).values('data_orcamento__month').annotate(total=Sum('valor_orc')).order_by('data_orcamento__month')
    categorias = Categoria.objects.all().order_by('nome')
    
    lista_orcamento = []
    
    for c in categorias:
        l = Lancamento.objects.filter(categoria_id = c.id, data_pagamento__month = mes_sel,
        ).values('categoria__nome').annotate(soma=Sum('valor_pago'))
        o = Orcamento.objects.filter(categoria_id = c.id, data_orcamento__month = mes_sel,
        ).values('categoria__nome').annotate(soma=Sum('valor_orc'))

        nome = c.nome
        if l:
            lanc_soma = round(float(l[0]['soma']),2)
        else:
            lanc_soma = 0

        if o:
            orc_valor = round(float(o[0]['soma']),2)
        else:
            orc_valor = 0
        
        if orc_valor == 0:
            uso = 's/ orçamento'
        else:
            uso = round((lanc_soma/orc_valor*100),2)
        saldo = round((orc_valor - lanc_soma),2)
        dados = {'nome':nome, 'saldo':saldo, 'uso_perc':uso, 'total':lanc_soma, 'indice':c.id, 'mes':mes_sel}

        lista_orcamento.append(dados)
        
    
    if len(orcamentos) > 0:
        orc = orcamentos[0]
    else:
        orc = {'valor_orc': 0 }


    graf_nome = categorias.filter(pk = item_indice).first().nome

    soma_lista = 0

    for item_lista in lista_orcamento:
        if lancamentos_exibir:
            if item_lista['nome'] == lancamentos_exibir[0].categoria.nome:
                soma_lista = round(item_lista['total'],2)


    context = {
        'lancamentos': lancamentos_exibir,
        'soma': soma_lista,
        'graf_nome': graf_nome,
        'orcamento' : orc,
        'lista_orcamento' : lista_orcamento,
        'lancamento_total_mensal' : lancamento_total_mensal,
        'orcamento_total_mensal': orcamento_total_mensal
        }
    
    return context
