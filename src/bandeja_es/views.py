from email import message
import json
from multiprocessing import context
from os import error, path
import pathlib
import os.path
from django.contrib.auth.models import User

from django.core import serializers
from tools.objects import AdminViewMixin, SuperuserViewMixin, VisualizadorViewMixin
import zipfile
import time
import requests
from tablib import Dataset

from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import (reverse_lazy, reverse)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, FormView,View)
from django.db import IntegrityError
from notifications.emails import send_email
from panel_carga.views import ProyectoMixin
from .models import PaqueteAttachment, PrevPaqueteAttachment, Version, Paquete, BorradorPaquete, PrevVersion, PrevPaquete, PrevPaqueteDocumento, PaqueteDocumento
from .forms import CreatePaqueteForm, PaquetePreviewForm, PrevVersionForm
from .filters import PaqueteFilter, PaqueteDocumentoFilter, BorradorFilter
from panel_carga.models import Documento, Proyecto
from panel_carga.choices import TYPES_REVISION

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class InBoxView(ProyectoMixin, View):
    model = Paquete
    template_name = 'bandeja_es/baes.html'
    context_object_name = 'paquetes'

    def get_queryset(self):
        clientes = [1,2,3]        
        contratistas = [4,5,6]        
        user = self.request.user
        try:
            user_rol =  user.perfil.rol_usuario
            # if user.is_superuser:
            #     pkg = Paquete.objects.all().filter(proyecto=self.proyecto).order_by("-fecha_creacion")
            if user_rol:
                if user_rol >=1 and user_rol <= 3:
                        pkg = Paquete.objects.filter(destinatario__perfil__rol_usuario__in=clientes, proyecto=self.proyecto).order_by("-fecha_creacion")
                elif user_rol >= 4 and user_rol <= 6:
                    pkg = Paquete.objects.filter(destinatario__perfil__rol_usuario__in=contratistas, proyecto=self.proyecto).order_by("-fecha_creacion")
        except Exception as error:
            messages.add_message(self.request, messages.ERROR, "Usuario no cuenta con perfil. {0}".format(error))
            return redirect('Bandejaeys')

        # lista_paquetes_filtrados = PaqueteFilter(self.request.GET, queryset=pkg)
        return   pkg #lista_paquetes_filtrados.qs.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paquetes"] = self.get_queryset()
        return context
        
    def get (self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    #Descargar todos los paquetes
    def post(self, request, *args, **kwargs):
        #Obtengo los elementos checkboxes del HTML
        listado_checkboxes = self.request.POST.getlist('paquetes_pk')
        paquetes = Paquete.objects.filter(pk__in=listado_checkboxes)
        listado_versiones_url = []
        #Formato Archivo.zip
        zip_subdir = "Cartas-Enviados-{0}-{1}".format(self.proyecto.nombre, time.strftime('%d-%m-%y'))
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        for paquete in paquetes:
            versiones = paquete.version.all()
            try:
                coment1 = paquete.comentario1.url
                if coment1:
                    print(coment1)
                    com1 = requests.get(coment1, stream=True)
                    zf.writestr(str(paquete.comentario1), com1.content)
            except Exception:
                pass
            try:
                coment2 = paquete.comentario2.url
                if coment2:
                    print(coment2)
                    com2 = requests.get(coment2, stream=True)
                    zf.writestr(str(paquete.comentario2), com2.content)
            except Exception:
                pass
            for version in versiones:
                try:
                    static = version.archivo.url
                    if static:
                        listado_versiones_url.append(version)  
                except Exception:
                    pass
            for version in listado_versiones_url:
                r = requests.get(version.archivo.url, stream=True)
                zf.writestr(str(version.archivo), r.content)

        zf.close()
        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return response
class EnviadosView(ProyectoMixin, ListView):
    model = Paquete
    template_name = 'bandeja_es/baes_Enviado.html'
    context_object_name = 'paquetes'
    

    def get_queryset(self):
        clientes = [1,2,3]        
        contratistas = [4,5,6]        
        user = self.request.user
        user_rol =  user.perfil.rol_usuario
        # if user.is_superuser:
        #     pkg = Paquete.objects.all().filter(proyecto=self.proyecto).order_by("-fecha_creacion")
        
        try:
            if user_rol:
                if user_rol >= 1 and user_rol <= 3:
                        pkg = Paquete.objects.filter(owner__perfil__rol_usuario__in=clientes, proyecto=self.proyecto).order_by("-fecha_creacion")#.filter(proyecto=self.proyecto).order_by("-fecha_creacion")
                elif user_rol >= 4 and user_rol <= 6:
                        pkg = Paquete.objects.filter(owner__perfil__rol_usuario__in=contratistas, proyecto=self.proyecto).order_by("-fecha_creacion")#.filter(proyecto=self.proyecto).order_by("-fecha_creacion")
            
        except Exception as error:
            messages.add_message(self.request, messages.ERROR, "Usuario no cuenta con perfil. {0}".format(error))
            return redirect('Bandejaeys')

        #lista_paquetes_filtrados = PaqueteFilter(self.request.GET, queryset=pkg)
        return  pkg
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paquetes"] = self.get_queryset()
        return context
    
    #Descargar todos los paquetes
    def post(self, request, *args, **kwargs):
        #Obtengo los elementos checkboxes del HTML
        listado_checkboxes = self.request.POST.getlist('paquetes_pk')
        paquetes = Paquete.objects.filter(pk__in=listado_checkboxes)
        listado_versiones_url = []
        #Formato Archivo.zip
        zip_subdir = "Cartas-Enviados-{0}-{1}".format(self.proyecto.nombre, time.strftime('%d-%m-%y'))
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        for paquete in paquetes:
            versiones = paquete.version.all()
            try:
                coment1 = paquete.comentario1.url
                if coment1:
                    print(coment1)
                    com1 = requests.get(coment1, stream=True)
                    zf.writestr(str(paquete.comentario1), com1.content)
            except Exception:
                pass
            try:
                coment2 = paquete.comentario2.url
                if coment2:
                    print(coment2)
                    com2 = requests.get(coment2, stream=True)
                    zf.writestr(str(paquete.comentario2), com2.content)
            except Exception:
                pass
            for version in versiones:
                try:
                    static = version.archivo.url
                    if static:
                        listado_versiones_url.append(version)  
                except Exception:
                    pass
            for version in listado_versiones_url:
                r = requests.get(version.archivo.url, stream=True)
                zf.writestr(str(version.archivo), r.content)

        zf.close()
        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return response
        # return redirect('bandeja-enviados')
        
        # Sacado de https://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
        # zip_subdir = "Cartas-Enviados-{0}-{1}".format(self.proyecto.nombre, time.strftime('%d-%m-%y'))
        # zip_filename = "%s.zip" % zip_subdir
        # s = BytesIO()   
        # zf = zipfile.ZipFile(s, "w")
        
        # paquetes = self.get_queryset()
        
        # for paquete in paquetes:
        #     listado_versiones_url = []
        #     listados_comentario_1 = []
        #     listados_comentario_2 = []
        #     try:
        #         coment1 = paquete.comentario1.url
        #         if coment1:
        #             listados_comentario_1.append(paquete)
        #     except Exception:
        #         pass
            
        #     try:
        #         coment2 = paquete.comentario2.url
        #         if coment2:
        #             listados_comentario_2.append(paquete)
        #     except Exception:
        #         pass
                
        #     versiones = paquete.version.all()
            
        #     for version in versiones:
        #         try:
        #             static = version.archivo.url
        #             if static:
        #                 listado_versiones_url.append(version)
        #         except ValueError:
        #             pass
                    
        #     for version in listado_versiones_url:
        #         r = requests.get(version.archivo.url, stream=True)
        #         zf.writestr(str(version.archivo), r.content)
            
        #     for paquete_comentario1 in listados_comentario_1:
        #         com1 = requests.get(paquete_comentario1.comentario1.url, stream=True)
        #         zf.writestr(str(paquete_comentario1.comentario1), com1.content)
                
        #     for paquete_comentario2 in listados_comentario_2:
        #         com2 = requests.get(paquete_comentario2.comentario2.url, stream=True)
        #         zf.writestr(str(paquete_comentario2.comentario2), com2.content)
                
        # zf.close()
        # response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        # response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        # return response

class TransmitalDetail(ProyectoMixin, View):
    http_method_names = ['get','post']
    def get(self, request, *args, **kwargs):
        # Sacado de https://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
        listado_versiones_url = []
        paquete = Paquete.objects.get(pk=self.kwargs['paquete_pk'])
        #estoy obteniendo las versiones del paquete
        versiones = paquete.version.all()
        zip_subdir = "Documentos-{0}-{1}".format(paquete.codigo, time.strftime('%d-%m-%y'))
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()   
        zf = zipfile.ZipFile(s, "w")
        #Contador de FileFields Vacios
        contador_version = 0
        contador_comentario_1 = 0
        contador_comentario_2 = 0
        for version in versiones:
            print(version)
            try:
                static = version.archivo.url
                if static:
                    contador_version += 1
            except Exception:
                pass
        try:
            coment1 = paquete.comentario1.url
            if coment1:
                contador_comentario_1 += 1   
        except Exception:
            pass
        try:
            coment2 = paquete.comentario2.url
            if coment2:
                contador_comentario_2 += 1
        except Exception:
            pass
        #Compresion de documentos
        if contador_version == 1 or contador_comentario_1 == 1 or contador_comentario_2 == 1:
            for version in versiones:
                try:
                    static = version.archivo.url
                    if static:
                        listado_versiones_url.append(version)
                        for version in listado_versiones_url:
                            r = requests.get(version.archivo.url, stream=True)
                            zf.writestr(str(version.archivo), r.content)
                except ValueError:
                    pass
            try:
                coment1 = paquete.comentario1.url
                if coment1:
                    com1 = requests.get(coment1, stream=True)
                    zf.writestr(str(paquete.comentario1), com1.content)     
            except Exception:
                pass
            try:
                coment2 = paquete.comentario2.url
                if coment2:
                    com2 = requests.get(coment2, stream=True)
                    zf.writestr(str(paquete.comentario2), com2.content)
            except Exception:
                pass    
            zf.close()
            response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return response
        else:
           messages.add_message(request, messages.ERROR, message='No se puede obtener la descarga de un tramital sin Archivos.')
           return redirect('bandeja-enviados')

class PaqueteDetail(ProyectoMixin, DetailView):
    model = Paquete
    template_name = 'bandeja_es/paquete-detail.html'
    context_object_name = 'paquete'

    def get_context_data(self, **kwargs):
        listado_versiones_url = []
        context = super().get_context_data(**kwargs)
        paquete = Paquete.objects.get(pk=self.kwargs['pk'])
        versiones = paquete.version.all()
        for version in versiones:
            try:
                static = version.archivo
                listado_versiones_url.append(static)
            except ValueError:
                pass
        if listado_versiones_url:
            correcto = True
        else:
            correcto = False
        context['versiones'] = versiones
        context['correcto'] = correcto
        return context
    
    def post(self, request, *args, **kwargs):
        # Sacado de https://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
        listado_versiones_url = []
        paquete = Paquete.objects.get(pk=self.kwargs['pk'])
        versiones = paquete.version.all()
        for version in versiones:
            try:
                static = version.archivo.url
                if static:
                    listado_versiones_url.append(version)
            except ValueError:
                pass
        zip_subdir = "Documentos-{0}-{1}".format(paquete.codigo, time.strftime('%d-%m-%y'))
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()   
        zf = zipfile.ZipFile(s, "w")
        for version in listado_versiones_url:
            r = requests.get(version.archivo.url, stream=True)
            zf.writestr(str(version.archivo), r.content)
        zf.close()
        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return response

class PaqueteUpdate(ProyectoMixin, SuperuserViewMixin, UpdateView):
    model = Paquete
    template_name = 'bandeja_es/paquete-update.html'
    form_class = CreatePaqueteForm
    success_url = reverse_lazy('Bandejaeys')

    def form_valid(self, form) -> HttpResponse:
        paquete = self.get_object()
        fecha_modificar = form.cleaned_data["fecha_creacion"]
        versiones = paquete.version.all()

        for version in versiones:
            version.fecha = fecha_modificar
            version.save()

        return super().form_valid(form)

class PaqueteDelete(ProyectoMixin, SuperuserViewMixin, DeleteView):
    model = Paquete
    template_name = 'bandeja_es/paquete-delete.html'
    success_url = reverse_lazy('Bandejaeys')
    context_object_name = 'paquete'

    def form_valid(self, form) -> HttpResponse:
        paquete = self.get_object()
        versions = paquete.version.all()
        versions.delete()
        messages.add_message(self.request, messages.SUCCESS, "Paquete eliminado junto a sus versiones, correctamente")
        return redirect('Bandejaeys')

class BorradorList(ProyectoMixin, ListView):
    template_name = 'bandeja_es/borrador.html'
    context_object_name = 'borrador_paquete'

    def get_queryset(self):
        paquetes = PrevPaquete.objects.filter(prev_propietario=self.request.user, proyecto=self.proyecto).order_by('-prev_fecha_creacion')
        qs =  BorradorPaquete.objects.filter(prev_paquete__in=paquetes).order_by('-fecha_creacion')
        lista_borradores_filtrados = BorradorFilter(self.request.GET, queryset=qs)
        return  lista_borradores_filtrados.qs.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = BorradorFilter(self.request.GET, queryset=self.get_queryset())
        return context

def create_borrador(request, paquete_pk):
    prev_paquete = PrevPaquete.objects.get(pk=paquete_pk)
    prev_versiones = prev_paquete.prev_documento.all()
    if prev_versiones:
        try:
            borrador = BorradorPaquete(
                owner= request.user,
                prev_paquete= prev_paquete
            )
            borrador.save()
            messages.add_message(request, messages.INFO, 'Borrador Creado.')
            return HttpResponseRedirect(reverse_lazy('Borradores'))

        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'El Borrador ya existe actualmente.')
            return redirect('nueva-version', paquete_pk=paquete_pk)
    else:
        messages.add_message(request, messages.ERROR, 'Nada que guardar en Borrador')
        return redirect('nueva-version', paquete_pk=paquete_pk)

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
        proyecto = Proyecto.objects.get(pk=request.session.get('proyecto'))
        rol =paquete_prev.prev_propietario.perfil.rol_usuario
        clientes = [1,2,3]
        contratistas = [4,5,6]
        if rol in clientes:
            pkg = Paquete.objects.filter(proyecto=proyecto, owner__perfil__rol_usuario__in=clientes).count()
            codigo_trasmital = str(proyecto.codigo) + "-" + "C" +"-" +str((pkg + 1))
        elif rol in contratistas:
            pkg = Paquete.objects.filter(proyecto=proyecto, owner__perfil__rol_usuario__in=contratistas).count()
            codigo_trasmital = str(proyecto.codigo) + "-" + "T" +"-" +str((pkg + 1))

        paquete = Paquete(
            codigo = codigo_trasmital,
            asunto = paquete_prev.prev_asunto,
            descripcion = paquete_prev.prev_descripcion,
            destinatario = paquete_prev.prev_receptor,
            owner = paquete_prev.prev_propietario,
            proyecto= proyecto,
            comentario1=paquete_prev.prev_comentario1,
            comentario2=paquete_prev.prev_comentario2,

        )
        # files = paquete_prev.attachments.all()
        # for file in files:
        #     PaqueteAttachment.objects.create(
        #         file=file.file,
        #         paquete=paquete
        #     )
            
        paquete.save()
        paquete_prev.delete()

        vertions = PrevVersion.objects.filter(pk__in=versiones_pk_list)
        for vertion in vertions:
            vertion_f = Version(
                owner= vertion.prev_owner,
                documento_fk= vertion.prev_documento_fk,
                archivo= vertion.prev_archivo,
                revision= vertion.prev_revision,
                estado_cliente= vertion.prev_estado_cliente,
                estado_contratista= vertion.prev_estado_contratista,
            )
            vertion_f.save()
            paquete.version.add(vertion_f)
            vertion.delete()

        notification_list = []
        project_numCod = str(proyecto.codigo + " - " + proyecto.nombre)

        for user in proyecto.participantes.all():
            notification_list.append(user.email)

        send_email(
            html="bandeja_es/emails/Respuesta.html",
            context= {
                "paquete": paquete
            },
            subject="[{}] Se ha emitido un Transmittal".format(project_numCod),
            recipients=notification_list
        )

        messages.success(request, message="Transmittal envíado correctamente.")
        return redirect('Bandejaeys')


# URL PARA SELECT2
def documentos_ajax(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        terms = request.GET.get('term')
        documentos = Documento.objects.filter(proyecto=request.session.get('proyecto'), Codigo_documento__icontains=terms)
        response_content = list(documentos.values()) 
    # return JsonResponse(response_content,safe=False)
    return JsonResponse(response_content, safe=False)

# def version_prev(request, paquete_pk):
#     context = {}

#     if request.method == 'GET':
#         form = VersionDocPreview()
#         context['form'] = form
#         context['paquete'] = paquete_pk
#         lista_versiones_pk = []
#         package = PrevPaquete.objects.get(pk=paquete_pk)
#         pkg_versiones = PrevPaqueteDocumento.objects.filter(prev_paquete=package)
#         for version in pkg_versiones:
#             pk = version.prev_version.pk
#             lista_versiones_pk.append(pk)
#         versiones = PrevVersion.objects.filter(pk__in=lista_versiones_pk)
#         response_content = list(versiones.values())
#     return render(request, 'bandeja_es/tabla-versiones-form.html', context)


    #### AJAX Request ####

def vue_version(request, paquete_pk):
    #### GET request para   ####        
    ####  Obtener las versiones ####        
    if request.method == 'GET':
        versiones = Documento.objects.filter(proyecto=request.session.get('proyecto', None))
        list_serviones = serializers.serialize('json', versiones, fields=('Codigo_documento', 'Descripcion', 'Especialidad'))
        print(list_serviones)
        # lista_versiones_pk = []
        # package = PrevPaquete.objects.get(pk=paquete_pk)
        # pkg_versiones = PrevPaqueteDocumento.objects.filter(prev_paquete=package)
        # for version in pkg_versiones:
        #     pk = version.prev_version.pk
        #     lista_versiones_pk.append(pk)
        # versiones = PrevVersion.objects.filter(pk__in=lista_versiones_pk)
        # response_content = list(versiones.values())
        
    return JsonResponse(list_serviones, safe=False)

@csrf_exempt
def vue_file_import(request):
    response_dict = []
    if request.user.is_authenticated:
        if request.method == 'POST':
            excel = request.FILES.get("file")
            if excel:
                dataset = Dataset()
                try:
                    imported_data = dataset.load(excel.read(), format='xlsx')
                except Exception as excep:
                    imported_data = None
                    error = excep
                    return JsonResponse({"message": "Hubo un error al procesar el archivo"}, status=500)

                if imported_data:
                    return JsonResponse({ 
                        "message": "se recibió el archivo",
                        "data": imported_data.dict
                        }, status=200)
                        
                else:
                    return JsonResponse({"message": "error con el archivo"}, status=500)

            else:

                return JsonResponse({
                    "message": "error con el archivo"
                },
                    status=500

                )

@csrf_exempt
def check_version(request):
    row_version = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST:
                owner = User.objects.get(pk=request.user.pk)
                rol = owner.perfil.rol_usuario
                paquete_pk = request.POST.get('paquete', None)
                doc_code = request.POST.get('prev_documento_fk', None)
                file = request.FILES.getlist('file', None)
                try:
                    doc = Documento.objects.get(Codigo_documento=doc_code)
                except Documento.DoesNotExist:
                    return JsonResponse({"message": 'No existe Documento con ese Código.'}, status=500)
                    
                row_version["prev_documento_fk"] = doc
                row_version["prev_revision"] = request.POST.get('prev_revision', None)
                # row_version["prev_archivo"]= file

                if rol >= 1 or rol <= 3:
                    row_version["prev_estado_cliente"] = request.POST.get('prev_estado_cliente', None)
                    row_version["adjuntar"] = request.POST.get('adjuntar', False)
                    row_version["prev_estado_contratista"] = None

                elif rol >= 4 or rol <= 6 :
                    row_version["prev_estado_contratista"] = request.POST.get('prev_estado_contratista', None)
                    row_version["prev_estado_cliente"] = None

                print(row_version)
                # form = PrevVersionForm(user=request.user, data=request.POST, files=request.FILES )
                form = PrevVersionForm(user=request.user, data=row_version, files=request.FILES )

                if form.is_valid():
                    prev_version = form.save(commit=False)
                    prev_version.prev_owner = owner
                    prev_version.save()
                    paquete = PrevPaquete.objects.get(pk=paquete_pk)
                    paquete.prev_documento.add(prev_version)
                    return JsonResponse({
                        "message": "Validado Correctamente"
                        }, status=200)
                else:
                    print(form.non_field_errors())
                    return JsonResponse({
                        "message": "version Invalidad",
                        "errors": form.non_field_errors(),
                    }, status=500)
            else:

                return JsonResponse({"message": "No se ha enviado correctamente la información necesaria"}, status=500)
                

# @csrf_exempt
# def upload_versiones_validated(request):
#     if request.user.is_authenticated:
        


class PrevPaqueteView(ProyectoMixin, VisualizadorViewMixin, FormView):
    template_name = 'bandeja_es/crear-pkg-modal.html'
    form_class = PaquetePreviewForm
    success_url = reverse_lazy('Bandejaeys')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        usuario = self.request.user
        rol = usuario.perfil.rol_usuario
        if rol >= 1 and rol <= 3:
            participantes = self.proyecto.participantes.filter(perfil__rol_usuario__in=[4,5,6], is_superuser=False, is_active=True).exclude(pk=usuario.pk)
        elif rol >= 4 and rol <= 6:
            participantes = self.proyecto.participantes.filter(perfil__rol_usuario__in=[1,2,3], is_superuser=False, is_active=True).exclude(pk=usuario.pk)
        else:
            participantes = []


        kwargs["participantes"] = participantes
        return kwargs

    def form_valid(self, form, **kwargs):
        paquete = form.save(commit=False)
        paquete.prev_propietario = self.request.user
        paquete.proyecto = self.proyecto
        paquete.save()
        # files = self.request.FILES.getlist('prev_comentario')
        # for file in files:
        #     PrevPaqueteAttachment.objects.create(
        #         prev_paquete = paquete,
        #         file= file
        #     )
        paquete_pk = paquete.pk
        if paquete.tipo == 1:
            return redirect('nueva-version', paquete_pk=paquete_pk)
        elif paquete.tipo == 2:
            paquete_prev = paquete
            proyecto = self.proyecto
            rol =paquete_prev.prev_propietario.perfil.rol_usuario
            clientes = [1,2,3]
            contratistas = [4,5,6]
            if rol in clientes:
                pkg = Paquete.objects.filter(proyecto=proyecto, owner__perfil__rol_usuario__in=clientes).count()
                codigo_trasmital = str(proyecto.codigo) + "-" + "C" +"-" +str((pkg + 1))
            elif rol in contratistas:
                pkg = Paquete.objects.filter(proyecto=proyecto, owner__perfil__rol_usuario__in=contratistas).count()
                codigo_trasmital = str(proyecto.codigo) + "-" + "T" +"-" +str((pkg + 1))

            paquete = Paquete(
                codigo = codigo_trasmital,
                asunto = paquete_prev.prev_asunto,
                descripcion = paquete_prev.prev_descripcion,
                destinatario = paquete_prev.prev_receptor,
                owner = paquete_prev.prev_propietario,
                proyecto= proyecto,
                comentario1=paquete_prev.prev_comentario1,
                comentario2=paquete_prev.prev_comentario2,
                tipo=paquete_prev.tipo
            )

            paquete.save()
            # for file in files:
            #     PaqueteAttachment.objects.create(
            #         paquete = paquete,
            #         file= file
            #     )
            paquete_prev.delete()

            messages.add_message(self.request, messages.SUCCESS, "Transmittal informativo enviado correctamente")
            return super().form_valid(form)

class TablaPopupView(ProyectoMixin, VisualizadorViewMixin, ListView):
    model = PrevVersion
    template_name = 'bandeja_es/tabla-versiones-form.html'

    def get_context_data(self, **kwargs):
        versiones = []
        context = super().get_context_data(**kwargs)
        paquete = PrevPaquete.objects.get( pk=self.kwargs['paquete_pk'] )
        vertions = PrevPaqueteDocumento.objects.filter(prev_paquete=paquete).order_by('-prev_fecha_creacion')
        for version in vertions:
            versiones.append(version.prev_version)
        context['versiones'] = versiones
        context["paquete_pk"] = self.kwargs['paquete_pk']
        return context
    
    def post(self, request, *args, **kwargs):
        context={}
        versiones_pk = []
        paquete = PrevPaquete.objects.get( pk=self.kwargs['paquete_pk'] )
        context['paquete'] = paquete
        vertions = paquete.prev_documento.all()
        if vertions:
            context['versiones'] = vertions
            for vertion in vertions:
                versiones_pk.append(vertion.pk)
            context['versiones_pk'] = versiones_pk
            return render(request, 'bandeja_es/create-paquete.html', context)
        else:
            messages.add_message(request, messages.ERROR, message='No se puede obtener la vista previa de un tramital sin revisiones.')
            return redirect('nueva-version', paquete_pk=paquete.pk)

class PrevVersionView(ProyectoMixin, VisualizadorViewMixin, FormView):
    model = PrevVersion
    template_name = 'bandeja_es/popup-archivo.html'
    form_class = PrevVersionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        paquete = PrevPaquete.objects.get(pk= self.kwargs['paquete_pk'])
        kwargs["paquete_pk"] = paquete
        kwargs["user"] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paquete = PrevPaquete.objects.get(pk= self.kwargs['paquete_pk'])
        choices = TYPES_REVISION[2:]
        context["paquete_pk"] = paquete
        context["choices"] = choices
        
        return context
    
    def form_valid(self, form, **kwargs):
        version = form.save(commit=False)
        version.prev_owner = self.request.user
        rev_a = form.cleaned_data["revision_a"]
        if rev_a:
            version.prev_revision = 1
        version.save()
        paquete = PrevPaquete.objects.get(pk=self.kwargs['paquete_pk'])
        paquete.prev_documento.add(version)
        return HttpResponse('<script type="text/javascript"> window.opener.location.reload(); window.close(); </script>')

class UpdatePrevVersion(ProyectoMixin, VisualizadorViewMixin, UpdateView):
    model = PrevVersion
    template_name = 'bandeja_es/popup-archivo.html'
    form_class = PrevVersionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        paquete = PrevPaquete.objects.get(pk= self.kwargs['paquete_pk'])
        user = self.request.user
        kwargs["paquete_pk"] = paquete
        kwargs["user"] = user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paquete = PrevPaquete.objects.get(pk= self.kwargs['paquete_pk'])
        context["paquete_pk"] = paquete
        return context
    
    def form_valid(self, form, **kwargs):
        version = form.save(commit=False)
        version.prev_owner = self.request.user
        version.save()
        paquete = PrevPaquete.objects.get(pk=self.kwargs['paquete_pk'])
        paquete.prev_documento.add(version)
        return HttpResponse('<script type="text/javascript"> window.opener.location.reload(); window.close(); </script>')

def delete_prev_version(request, id_version, paquete_pk):
    if request.method == 'GET':
        prev_version = PrevVersion.objects.get(pk=id_version)
        prev_version.delete()
        messages.add_message(request, messages.INFO, message='Revisión eliminada')
    return redirect('nueva-version', paquete_pk=paquete_pk)


