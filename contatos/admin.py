from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'email',
                    'telefone', 'data_criacao', 'categoria', 'mostrar')
    #list_filter = ('categoria', 'nome', 'sobrenome', 'email',)
    search_fields = ('nome', 'sobrenome', 'email', 'telefone')
    list_per_page = 10
    list_display_links = ('nome', 'sobrenome')
    list_editable = ('email', 'telefone', 'mostrar')
    list_select_related = ('categoria',)
    date_hierarchy = 'data_criacao'
    ordering = ('nome',)
    #filter_horizontal = ('categoria',)


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
