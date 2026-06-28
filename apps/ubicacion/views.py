from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Pais, Departamento, Provincia, Ciudad


@login_required
def pais_list(request):
    paises = Pais.objects.all().order_by('nombre')
    return render(request, 'ubicacion/pais_list.html', {'paises': paises})


@login_required
def departamento_list(request):
    departamentos = Departamento.objects.select_related('pais').all().order_by('nombre')
    return render(request, 'ubicacion/departamento_list.html', {'departamentos': departamentos})


@login_required
def provincia_list(request):
    provincias = Provincia.objects.select_related('departamento').all().order_by('nombre')
    return render(request, 'ubicacion/provincia_list.html', {'provincias': provincias})


@login_required
def ciudad_list(request):
    ciudades = Ciudad.objects.select_related('provincia').all().order_by('nombre')
    return render(request, 'ubicacion/ciudad_list.html', {'ciudades': ciudades})


def get_departamentos(request):
    pais_id = request.GET.get('pais_id')
    departamentos = Departamento.objects.filter(pais_id=pais_id).order_by('nombre')
    return JsonResponse(list(departamentos.values('id', 'nombre')), safe=False)


def get_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.filter(departamento_id=departamento_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)


def get_ciudades(request):
    provincia_id = request.GET.get('provincia_id')
    ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
    return JsonResponse(list(ciudades.values('id', 'nombre')), safe=False)