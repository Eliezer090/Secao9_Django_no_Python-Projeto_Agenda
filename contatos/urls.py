from django import urls
from . import views

urlpatterns = [
    urls.path('', views.index, name='index'),
    urls.path('<int:contato_id>/', views.ver_contato, name='ver_contato'),
    urls.path('busca/', views.busca, name='busca'),
]
