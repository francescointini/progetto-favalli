from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from .component_parsing import parsing

class Component(models.Model):
    name = models.CharField(
        verbose_name='Nome',
        max_length=50,
    )
    file = models.FileField(
        upload_to='uploads',
        verbose_name='File'
    )
    created_at = models.DateField(
        verbose_name='Data di creazione', 
        auto_now_add=True
    )
    entity_name = models.CharField(
        blank=True,
        null=True,
        verbose_name='Nome entità',
        max_length=50
    )
    input_ports = models.TextField(
        blank=True,
        null=True,
        verbose_name='Porte di input'
    )
    output_ports = models.TextField(
        blank=True,
        null=True,
        verbose_name='Porte di output'
    )
    architecture_name = models.CharField(
        blank=True,
        null=True,
        verbose_name='Nome Architettura',
        max_length=50
    )

    def __str__(self):
        string = f"ID:{self.pk}, Nome:{self.name}, Nome entity:{self.entity_name}, Nome architettura:{self.architecture_name}"
        return string

@receiver(post_save, sender=Component, dispatch_uid='Component: post-save elaboration')
def elaboration(sender, **kwargs):
    obj = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        parsing(obj)

class Structural(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Nome'
    )
    component_list = models.TextField(
        verbose_name='Componenti'
    )
    created_at = models.DateField(
        verbose_name='Data di creazione', 
        auto_now_add=True
    )
    mappings = models.TextField(
        verbose_name='Mappature',
        blank=True,
        null=True
    )
    entity_name = models.CharField(
        verbose_name='Nome entità',
        max_length=50,
        blank=True,
        null=True
    )
    architecture_name = models.CharField(
        verbose_name='Nome architettura',
        max_length=50,
        blank=True,
        null=True,
    )
