import django_filters
from django import forms
from panel_carga.models import Documento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from bandeja_es.models import Version

class DocFilter(django_filters.FilterSet):
    class Meta:
        model = Documento
        fields = ['Codigo_documento', 'fecha_Emision_B', 'Especialidad']
    
    def __init__(self, *args, **kwargs):
        super(DocFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()
    