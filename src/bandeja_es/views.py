from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.urls import (reverse_lazy, reverse)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, FormView)
from panel_carga.views import ProyectoMixin

from .models import Version, Paquete, BorradorVersion, BorradorPaquete, PrevVersion, PrevPaquete, BorradorDocumento, PaqueteDocumento
from .forms import PreviewVersionSet, VersionDocPreview, CreatePaqueteForm, VersionFormset, PaqueteBorradorForm, BorradorVersionFormset, PaquetePreviewForm, VersionDocBorrador
from .filters import PaqueteFilter, PaqueteDocumentoFilter, BorradorFilter, BorradorDocumentoFilter
from panel_carga.filters import DocFilter
from panel_carga.models import Documento
# Create your views here.

class InBoxView(ProyectoMixin, ListView):
    model = Paquete
    template_name = 'bandeja_es/baes.html'
    context_object_name = 'paquetes'
    paginate_by = 15

    def get_queryset(self):
        pkg =  Paquete.objects.filter(destinatario=self.request.user)
        lista_paquetes_filtrados = PaqueteFilter(self.request.GET, queryset=pkg)
        return  lista_paquetes_filtrados.qs.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pkg = Paquete.objects.filter(destinatario=self.request.user)
        context["filter"] = PaqueteFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class EnviadosView(ProyectoMixin, ListView):
    model = Paquete
    template_name = 'bandeja_es/baes_Enviado.html'
    context_object_name = 'paquetes'
    paginate_by = 10

    def get_queryset(self):
        pkg =  Paquete.objects.filter(owner=self.request.user)
        lista_paquetes_filtrados = PaqueteFilter(self.request.GET, queryset=pkg)
        return  lista_paquetes_filtrados.qs.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pkg = Paquete.objects.filter(owner=self.request.user)
        context["filter"] = PaqueteFilter(self.request.GET, queryset=self.get_queryset())
        return context
   
class PapeleraView(ProyectoMixin, ListView):
    model = Paquete
    # template_name = 
    context_object_name = 'paquetes'

class PaqueteDetail(ProyectoMixin, DetailView):
    model = Paquete
    template_name = 'bandeja_es/paquete-detail.html'
    context_object_name = 'paquete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paquete = Paquete.objects.get(pk=self.kwargs['pk'])
        versiones = PaqueteDocumento.objects.filter(paquete=paquete)
        context['versiones'] = versiones
        return context
class PaqueteUpdate(ProyectoMixin, UpdateView):
    model = Paquete
    template_name = 'bandeja_es/paquete-update.html'
    form_class = CreatePaqueteForm
    success_url = reverse_lazy('paquete-detalle')

class PaqueteDelete(ProyectoMixin, DeleteView):
    model = Paquete
    template_name = 'bandeja_es/paquete-delete.html'
    success_url = reverse_lazy('Bandejaeys')
    context_object_name = 'paquete'

class BorradorList(ProyectoMixin, ListView):
    template_name = 'bandeja_es/borrador.html'
    paginate_by = 15

    def get_queryset(self):
        qs =  BorradorPaquete.objects.filter(owner=self.request.user)
        lista_borradores_filtrados = BorradorFilter(self.request.GET, queryset=qs)
        return  lista_borradores_filtrados.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = BorradorPaquete.objects.filter(owner=self.request.user)
        context["filter"] = BorradorFilter(self.request.GET, queryset=self.get_queryset())
        borrador_paquete = BorradorPaquete.objects.all().filter(owner=self.request.user)
        context['borrador_paquete'] = borrador_paquete
        return context

def create_borrador(request, borrador_pk=None):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            borrador_paraquete = PaquetePreviewForm(request.POST or None)
            borrador_version_set = PreviewVersionSet(request.POST or None, request.FILES or None)
            borrador_fk = 0

            #   Borrador para el Form #
            #    del Paquete que contendrá las versiones #
            asunto_b =  borrador_paraquete['prev_asunto'].value()
            destinatario_b = borrador_paraquete['prev_receptor'].value()
            descripcion_b = borrador_paraquete['descripcion'].value()
            #################################################################
            #        Si existe borrador, lo actualiza, si no lo crea        #  
            try:
                versiones_pk = []
                borrador = BorradorPaquete.objects.get(pk=borrador_pk)
                borrador_versiones = BorradorDocumento.objects.get(borrador=borrador)
                for x in borrador_versiones:
                    versiones.append(x.version.pk)
                    return versiones_pk

                if destinatario_b:
                    destinatario_b = int(destinatario_b)
                    desti = User.objects.get(pk=destinatario_b)
                    borrador.asunto = asunto_b
                    borrador.descripcion = descripcion_b
                    borrador.destinatario = desti
                    borrador.save()
                else:
                    borrador = BorradorPaquete.objects.get(pk=borrador_pk)
                    borrador.asunto = asunto_b
                    borrador.descripcion = descripcion_b
                    borrador.save()
                
                for form, version_pk in zip(borrador_version_set, versiones_pk):
                    documento_b = form['prev_documento_fk'].value()
                    revision_b = form['prev_revision'].value() 
                    archivo_b = form['prev_archivo'].value()
                    comentario_b = form['prev_comentario'].value()
                    cliente_estado_b = form['prev_estado_cliente'].value()
                    contratista_estado_b = form['prev_estado_contratista'].value()

                    if cliente_estado_b and contratista_estado_b:            #
                        cliente_estado_b = int(cliente_estado_b)            #  If que comprueba que estados del
                        contratista_estado_b = int(contratista_estado_b)    #   cliente y contratista existan
                    else:                                                   #
                        cliente_estado_b = 0                                #
                        contratista_estado_b = 0
                    
                    version = BorradorVersion.objects.get(pk=version_pk)
                    
                    if documento_b:
                        documento_b = int(documento_b)
                        document = Documento.objects.get(pk=documento_b)
                        version.documento_fk = document
                        version.revision = revision_b
                        version.archivo = archivo_b
                        version.comentario = comentario_b
                        version.estado_cliente = cliente_estado_b
                        version.estado_contratista = contratista_estado_b
                    else:
                        documento_b = 0
                        version.revision = revision_b
                        version.archivo = archivo_b
                        version.comentario = comentario_b
                        version.estado_cliente = cliente_estado_b
                        version.estado_contratista = contratista_estado_b

                    version.save()

                    return JsonResponse({'msg': 'Update'})

            except BorradorPaquete.DoesNotExist:
            #################################################################

                # Valida y transforma valores vacíos a su correspondiente tipo #
                if destinatario_b:
                    destinatario_b = int(destinatario_b)
                    desti = User.objects.get(pk=destinatario_b)
                    borrador = BorradorPaquete(
                        asunto= asunto_b,
                        descripcion= descripcion_b,
                        destinatario= desti,
                        owner= request.user
                    )
                else:
                    borrador = BorradorPaquete(
                        asunto= asunto_b,
                        descripcion= descripcion_b,
                        owner= request.user
                    )
                borrador.save()
                #   Borrador para           #
                #   el Formset de Versiones #
                borrador_fk = borrador.pk
                paquete_borrador = BorradorPaquete.objects.get(pk=borrador_fk)
                for form in borrador_version_set:
                    documento_b = form['prev_documento_fk'].value()
                    revision_b = form['prev_revision'].value() 
                    archivo_b = form['prev_archivo'].value()
                    comentario_b = form['prev_comentario'].value()
                    cliente_estado_b = form['prev_estado_cliente'].value()
                    contratista_estado_b = form['prev_estado_contratista'].value()
                #############################################################
                    if cliente_estado_b and contratista_estado_b:            #
                        cliente_estado_b = int(cliente_estado_b)            #  If que comprueba que estados del
                        contratista_estado_b = int(contratista_estado_b)    #   cliente y contratista existan
                    else:                                                   #
                        cliente_estado_b = 0                                #
                        contratista_estado_b = 0                            #
                #############################################################
                    if documento_b: #if que comprueba un valor no vacío para //documento_b// #
                        documento_b = int(documento_b)
                        document = Documento.objects.get(pk=documento_b)
                        version = BorradorVersion(
                            owner= request.user,
                            documento_fk= document,
                            revision= revision_b,
                            archivo= archivo_b,
                            comentario= comentario_b,
                            estado_cliente= cliente_estado_b,
                            estado_contratista= contratista_estado_b,
                        )
                    else:
                        documento_b = 0
                        version = BorradorVersion(
                            owner= request.user,
                            revision= revision_b,
                            archivo= archivo_b,
                            comentario= comentario_b,
                            estado_cliente= cliente_estado_b,
                            estado_contratista= contratista_estado_b,
                        )

                    version.save()
                    paquete_borrador.version.add(version)
                return JsonResponse({'msg': 'Success'})

def editar_borrador(request, package):
    context = {}
    if request.method == 'POST':
        form_paquete = PaqueteBorradorForm(request.POST or None)
        formset_versiones = VersionDocBorrador(request.POST or None, request.FILES or None)
        if form_paquete.is_valid() and formset_versiones.is_valid():
            form_paquete.save()
            for form in formset_versiones:
                form.save()
    else:
        vrs_borrador = BorradorDocumento.objects.filter(borrador=pkg_borrador)
        form_paquete = PaqueteBorradorForm(instance=pkg_borrador)
        formset_versiones = VersionDocBorrador()
        context['form_paquete'] = form_paquete
        context['formset_versiones'] = formset_versiones
    return render(request, 'bandeja_es/crear-borrador.html', context)

class BorradorDelete(ProyectoMixin, DeleteView):
    model = BorradorPaquete
    success_url = reverse_lazy('Bandejaeys')
    pass

def create_paquete(request, paquete_pk, versiones_pk):
    context = {}
    if request.method == 'GET':

    #########################################################
    #             Transformación de str                     #
    #                a Lista de Pk's                        #
        lista_nueva = versiones_pk.lstrip("[").rstrip("]")
        new_list = lista_nueva.replace(',', "")
        versiones_pk_1 = list(new_list.split())
        versiones_pk_list = list(map(int, versiones_pk_1))
    #                                                       #
    #                                                       #
    #########################################################

        paquete_prev = PrevPaquete.objects.get(pk=paquete_pk)
        paquete = Paquete(
            asunto = paquete_prev.prev_asunto,
            descripcion = paquete_prev.prev_descripcion,
            destinatario = paquete_prev.prev_receptor,
            owner = paquete_prev.prev_propietario,
        )
        paquete.save()
        for v in versiones_pk_list:
            vertion = PrevVersion.objects.get(pk=v)
            vertion_f = Version(
                owner= vertion.prev_owner,
                documento_fk= vertion.prev_documento_fk,
                revision= vertion.prev_revision,
                estado_cliente= vertion.prev_estado_cliente,
                estado_contratista= vertion.prev_estado_contratista,
            )
            vertion_f.save()
            paquete.version.add(vertion_f)


        return HttpResponseRedirect(reverse_lazy('Bandejaeys'))

def create_preview(request, borrador_pk):
    context = {}
    context2 = {}
    if borrador_pk == None:
        borrador_pk = 0
        pkg_borrador = BorradorPaquete.objects.get(pk=borrador_pk)
        versiones = BorradorDocumento.objects.filter(borrador=pkg_borrador)
    else:
        pkg_borrador = BorradorPaquete.objects.get(pk=borrador_pk)
        versiones = BorradorDocumento.objects.filter(borrador=pkg_borrador)

    PreviewVersionFormset = formset_factory(VersionDocPreview, extra= 1)
    if request.method == 'POST':
        version_list = []
        version_list_pk = []
        form_paraquete = PaquetePreviewForm(request.POST or None)
        formset_version = PreviewVersionFormset(request.POST or None, request.FILES or None, initial=[{'prev_documento_fk': x.version.documento_fk, 'prev_revision': x.version.revision, 'prev_estado_cliente': x.version.estado_cliente, 'prev_estado_contratista': x.version.estado_contratista, 'prev_archivo': x.version.archivo, 'prev_comentario': x.version.comentario} for x in versiones])
        if form_paraquete.is_valid() and formset_version.is_valid():
            package_pk = 0
            obj = form_paraquete.save(commit=False)
            obj.prev_propietario = request.user
            obj.save()
            package_pk = obj.pk
            for form in formset_version:
                package = PrevPaquete.objects.get(pk=package_pk)
                version = form.save(commit=False)
                version.prev_owner = request.user
                version.save()
                version_pk = version.pk
                version_qs = PrevVersion.objects.get(pk=version_pk)
                package.prev_documento.add(version_qs)
                version_list.append(version)
                version_list_pk.append(version_pk)
        context2['paquete'] = package
        context2['paquete_pk'] = package_pk
        context2['versiones'] = version_list
        context2['versiones_pk'] = version_list_pk

        return render(request, 'bandeja_es/create-paquete.html', context2)

    else:
        try:
            form_paraquete = PaquetePreviewForm(initial={
                'descripcion': pkg_borrador.descripcion,
                'prev_receptor': pkg_borrador.destinatario,
                'prev_asunto': pkg_borrador.asunto,
            })
            PreviewVersionFormset = formset_factory(VersionDocPreview, extra= (len(versiones))-3)
            formset_version = PreviewVersionFormset(initial=[{'prev_documento_fk': x.version.documento_fk, 'prev_revision': x.version.revision, 'prev_estado_cliente': x.version.estado_cliente, 'prev_estado_contratista': x.version.estado_contratista, 'prev_archivo': x.version.archivo, 'prev_comentario': x.version.comentario} for x in versiones])
            context['formset'] = formset_version
            context['form_paraquete'] = form_paraquete

        except:
            data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
            PreviewVersionFormset = formset_factory(VersionDocPreview, extra=1)
            form_paraquete = PaquetePreviewForm()
            formset_version = PreviewVersionFormset(data)
            context['formset'] = formset_version
            context['form_paraquete'] = form_paraquete
        context['borr_pk'] = borrador_pk

    return render(request, 'bandeja_es/create-paquete2.html', context)
    
