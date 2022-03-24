from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    telefone = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nome
