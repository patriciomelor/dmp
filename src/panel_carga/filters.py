import django_filters
from django import forms
from .models import Documento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DocFilter(django_filters.FilterSet): 
    fecha_Emision_0 = django_filters.DateFilter(
        label='Fecha Emision 0', 
        lookup_expr='icontains',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'style':'float:left;'

        }), input_formats=['%Y-%m-%d'])

    fecha_Emision_B = django_filters.DateFilter(
        lookup_expr='icontains',
        label='Fecha Emision B', 
        widget=forms.DateInput(attrs={
            'type': 'date','class':'float-left;'

        }), input_formats=['%Y-%m-%d']
    )
    Especialidad = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Especialidad', 
        widget=forms.TextInput(
            attrs={
                'name':'#ordenName',
                'id':'ordenName',
                'autocomplete':'on',
                'class':'float-left;'
                }
            )
        )
    Descripcion = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Descripción', 
        widget=forms.TextInput(
            attrs={
                'name':'#ordenName2',
                'id':'ordenName2',
                'autocomplete':'on',
                'class':'float-left;'
                }
            )
        )
    Codigo_documento = django_filters.CharFilter(
        label='Codigo Documento', 
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'name':'#ordenName3',
                'id':'ordenName3',
                'autocomplete':'on',
                'class':'float-left;'
                }
            )
        )
    Tipo_Documento = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Tipo Documento', 

        widget=forms.TextInput(
            attrs={
                'name':'#ordenName4',
                'id':'ordenName4',
                'autocomplete':'on',
                'class':'float-left;'
                }
            )
        )
    Numero_documento_interno = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Numero Interno', 
        widget=forms.TextInput(
            attrs={
                'name':'#ordenName5',
                'id':'ordenName5',
                'autocomplete':'on',
                'class':'float-left;'
                }
            )
        )
    class Meta:
        model=Documento
        fields = ['Especialidad', 'Descripcion', 'Codigo_documento','Tipo_Documento','Numero_documento_interno','fecha_Emision_B','fecha_Emision_0']

   