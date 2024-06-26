from django import forms
from django.contrib.auth import models
from django.core.files.storage import FileSystemStorage
from django.db.models.fields import TextField
from django.forms import BaseFormSet, fields, widgets
from django.forms import (formset_factory, modelformset_factory)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.forms.forms import Form

from configuracion.models import Restricciones

from .models import Tarea, Respuesta

from panel_carga.models import Documento


class TareaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user_list = []
        self.proyecto = kwargs.pop('proyecto', None)
        self.usuario = kwargs.pop('usuario', None)
        self.participantes = kwargs.pop('participantes', None)
        current_rol = self.usuario.perfil.rol_usuario
        #### recorre a todos los participantes e incluye en un listado solo el equipo de la empresa
        for user in self.participantes:
            try:
                rol = user.perfil.rol_usuario

                if current_rol >= 1 and current_rol <= 3:
                    if rol >= 1 and rol <= 3:
                        user_list.append(user.pk)

                if current_rol >= 4 and current_rol <= 6:
                    if rol >= 4 and rol <= 6:
                        user_list.append(user.pk)
            except Exception:
                pass
        # try:
        #     user_list.remove(self.usuario.pk)
        # except:
        #     pass
        qs = self.participantes.filter(pk__in=user_list)
        super(TareaForm, self).__init__(**kwargs)
        self.fields["documento"].disabled = True
        self.fields["encargado"] = forms.ModelChoiceField(queryset=qs)
        self.fields["restricciones"] = forms.ModelChoiceField(queryset=Restricciones.objects.filter(proyecto=self.proyecto))
        self.fields["restricciones"].required = False

    class Meta:
        model = Tarea
        exclude = ["estado","autor"]
        widgets = {
            'plazo': forms.DateInput(attrs={'type':'date'}),
            'comentarios': forms.Textarea(attrs={'style':'margin-top: 0px; margin-bottom: 0px; height: 63px;'}),
        }


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        exclude = ["tarea", "sent", "estado", "motivo"]