from django.db import models

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=5)
    
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=75)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=85)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=75)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return self.nombre