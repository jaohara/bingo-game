from django.contrib import admin

from .models import GameSet, Square, GameInstance, GameCard, GameEvent

# Register your models here.
admin.site.register(GameSet)
admin.site.register(Square)
admin.site.register(GameInstance) 
admin.site.register(GameCard)
admin.site.register(GameEvent)