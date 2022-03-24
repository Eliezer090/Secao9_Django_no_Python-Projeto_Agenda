from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):

    # para descrescente use '-nome'
    contatos = Contato.objects.order_by(
        'nome').filter(mostrar=True)
    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html', {'contatos': contatos})


def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    # por usarmos o get_object_or_404 podemos fazer validações como é feito abaixo
    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {'contato': contato})


def busca(request):
    termo = request.GET.get('termo').strip()
    if termo is None or termo == '':
        messages.add_message(request, messages.ERROR,
                             'Campo Pesquisa nao pode ficar vazio')
        return redirect('index')
    campos = Concat('nome', Value(' '), 'sobrenome', Value(' '))
    # o Q é uma classe que permite criar consultas complexas realizando OR na consulta
    contatos = Contato.objects.annotate(
        nome_completo=campos).filter(Q(nome_completo__icontains=termo) | Q(email__icontains=termo) | Q(telefone__icontains=termo), mostrar=True).order_by('nome')

    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {'contatos': contatos})
