from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato
# Create your views here.


def login(request):
    if auth.get_user(request).is_authenticated:
        return redirect('dashboard')
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    if user is not None:
        auth.login(request, user)
        return redirect('dashboard')
    else:
        messages.add_message(request, messages.ERROR,
                             'Usuario ou senha invalidos')
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    sobrenome = request.POST.get('sobrenome')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR,
                             'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if nome == '' or email == '' or senha == '' or senha2 == '' or sobrenome == '':
        messages.add_message(request, messages.ERROR,
                             'Preencha todos os campos')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Senhas nao conferem')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.add_message(request, messages.ERROR,
                             'Senha deve ter no minimo 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.add_message(request, messages.ERROR,
                             'Usuario deve ter no minimo 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR,
                             'Usuario ja existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR,
                             'Email ja existe')
        return render(request, 'accounts/cadastro.html')

    try:
        user = User.objects.create_user(
            username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Cadastro realizado com sucesso')
        return redirect('login')
    except:
        messages.add_message(request, messages.ERROR,
                             'Erro ao cadastrar usuario')
        return render(request, 'accounts/cadastro.html')


@login_required(login_url='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR,
                             'Formulario invalido')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')
    if len(descricao) < 5:
        messages.add_message(request, messages.ERROR,
                             'Descricao deve ter no minimo 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    try:
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Contato cadastrado com sucesso')
        return redirect('dashboard')
    except:
        messages.add_message(request, messages.ERROR,
                             'Erro ao enviar formulario')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
