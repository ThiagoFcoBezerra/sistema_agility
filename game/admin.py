from django.contrib import admin

from game.models import Game, GameMensal, Area, Meta

admin.site.register(Game)
admin.site.register(GameMensal)
admin.site.register(Area)
admin.site.register(Meta)