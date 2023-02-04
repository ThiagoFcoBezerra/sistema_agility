import datetime
from django.shortcuts import redirect, render
from django.db.models.aggregates import Sum, Avg, Count
from django.contrib.auth.decorators import login_required, permission_required
from game.models import Meta, Game, GameMensal, Area


# Create your views here.
@login_required
def dashboard (request):
   
    game = Game.objects.all().last()
    lista_mensal = GameMensal.objects.filter(game_ano = game)
    mensal = None
    areas = None
    metas = None
    if request.method == 'POST':
        chave = request.POST['data']
        mensal = GameMensal.objects.get(pk = chave)
    else:
        if game:
            mensal = GameMensal.objects.filter(game_ano = game).last()

    if mensal:
        areas = Area.objects.filter(game_mes = mensal)
        metas = Meta.objects.filter(meta_area__game_mes = mensal)

    dados = {
        'game': game,
        'lista_mensal':lista_mensal,
        'mensal': mensal,
        'areas': areas,
        'metas': metas
    }

    return render(request, 'game/game.html', dados)

@login_required
@permission_required('game.atualiza_metas', raise_exception=True)
def atualiza_game(request):
    game = Game.objects.all().last()
    mensal = GameMensal.objects.filter(game_ano = game).last()
    metas = []
    if mensal:
        metas = Meta.objects.filter(meta_area__game_mes = mensal)
    if request.method == 'POST':
        meta = metas.get(pk=request.POST['meta_id'])
        meta.data_atualizacao = datetime.datetime.now()
        meta.realizado_anterior = meta.realizado
        meta.realizado = request.POST['meta_valor']
        pontos = round((float(request.POST['meta_valor'])/float(meta.orcado) * float(meta.peso)),2)
        meta.pontos = str(pontos)
        meta.save()

    dados = {
        'metas':metas,
    }

    return render(request, 'game/atualiza_game.html', dados)

@login_required
def apura_game(request):
    game = Game.objects.all().last()
    mensal = GameMensal.objects.filter(game_ano = game).last()
    areas = Area.objects.filter(game_mes = mensal)
    metas = Meta.objects.filter(meta_area__game_mes = mensal)

    total_areas = metas.values('meta_area').annotate(total = Sum('pontos'))
    for total in total_areas:
        area = areas.get(pk = total['meta_area'])
        area.pontos = total['total'] * area.peso / 1000
        area.save()

    total_mensal = Area.objects.filter(game_mes = mensal).aggregate(Sum('pontos'))
    mensal.pontos = total_mensal['pontos__sum']
    mensal.save()

    total_game = GameMensal.objects.aggregate(Avg('pontos'))
    game.pontos = total_game['pontos__avg']
    game.save()

    return redirect('dashboard')