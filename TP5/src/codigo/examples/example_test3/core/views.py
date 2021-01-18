from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.db.models import ProtectedError, Q

from django.views.generic import ListView, FormView
from .models import Propriedade, Reserva, Pagamento
from .forms import *
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
import datetime
import time
from django.contrib import messages


# Classe de controle que exibe as propriedades
# De um usuário na tela
class MinhasPropriedades(ListView,ClassB,ClassC):
    model = Propriedade
    template_name = 'core/minhaspropriedades.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Minhas propriedades'
        return context

    def get_queryset(self):
        return Propriedade.objects.filter(proprietario=self.request.user)


def prop_detalhe_view(request, pk):
    propriedade = get_object_or_404(Propriedade, id=pk)
    reservas = Reserva.objects.all().filter(propriedade=propriedade)
    dados = []
    for reserva in reservas:
        hospede = reserva.hospede
        data_ini = reserva.dini.strftime('%Y-%m-%d')
        data_fim = reserva.dfim.strftime('%Y-%m-%d')
        dados.append((hospede, data_ini, data_fim))

    return render(request, 'core/propriedade.html', context={'prop': propriedade, 'user': request.user, 'dados': dados})

# Uma função de controle
# Que trata a exibição da tela inicial do sistema
def index_view(request):
    form = BuscaPropForm(request.POST or None)
    if (form.is_valid()):
        ini = form.cleaned_data['data_ini'].strftime('%Y-%m-%d')
        fim = form.cleaned_data['data_fim'].strftime('%Y-%m-%d')
        cidade = form.cleaned_data['cidade']
        return HttpResponseRedirect('/propriedades/'+ cidade +'/' + ini + '/' + fim)
    return render(request,'core/index.html', {'form': form})



# Classe para o model Reserva, com campos que descrevem
# Uma reserva em um sistema de reservas
class Reserva(Propriedade):

    # informacoes basicas da reserva
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hospede = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.PROTECT, blank=True)
    dados_pagamento = models.ForeignKey('Pagamento', on_delete=models.PROTECT, blank=True)

    # as possiveis escolhas para o campo qtd_pessoas
    QTD_PESSOAS_CHOICES = (
        ('1', '1 pessoa'),
        ('2', '2 pessoas'),
        ('3', '3 pessoas'),
    )

    qtd_pessoas = models.CharField('Quantidade de pessoas da reserva', max_length=1, choices=QTD_PESSOAS_CHOICES, default=1)

    # campos do tipo data, que determinam o inicio e o fim da reserva
    dini = models.DateField('Inicio da reserva', default=datetime.datetime.now)
    dfim = models.DateField('Fim da reserva', default=get_data)

    def __str__(self):
        return self.propriedade.nome
