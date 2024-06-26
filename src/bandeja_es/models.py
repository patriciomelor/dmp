from django.db import models
from django.contrib.auth.models import User
from panel_carga.choices import (ESTADO_CONTRATISTA, ESTADOS_CLIENTE, TYPES_REVISION)
from django.conf import settings
from panel_carga.models import Documento, Proyecto
from django.forms import model_to_dict
from django.utils import timezone
#################################################
                # VERSION Y PAQUETE
#################################################

class Version(models.Model):
    fecha = models.DateTimeField(verbose_name="Fecha Versión", default=timezone.now, editable=True)
    documento_fk = models.ForeignKey(Documento, on_delete=models.CASCADE) #relacion por defecto one to many en django
    archivo = models.FileField(upload_to="proyecto/documentos/", blank=True, null=True)
    revision = models.IntegerField(verbose_name="Revisión", choices=TYPES_REVISION, blank=True)
    #revision = models.CharField(verbose_name="Revisión", max_length=1, default="B")
    estado_cliente = models.IntegerField(choices=ESTADOS_CLIENTE, default=1, blank=True, null=True) #Necesario para tomar los estados del primer grafico
    estado_contratista = models.IntegerField(choices=ESTADO_CONTRATISTA, default=1, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creador")
    valido = models.BooleanField(verbose_name="Válido", default=1) #1=VALIDO  0=ANULADO

    def __str__(self):
        if self.estado_cliente is not None:
            return str(self.documento_fk.Codigo_documento)+"-"+str(self.get_revision_display()+"- "+str(self.get_estado_cliente_display()))
        elif self.estado_contratista is not None:
            return str(self.documento_fk.Codigo_documento)+"-"+str(self.get_revision_display()+"- "+str(self.get_estado_contratista_display()))

class Paquete(models.Model):
    TYPE_PQUETE = (
        ('', "------"),
        (1, "Información Técnica"),
        (2, "Informativo"),
    )
    codigo = models.CharField(max_length=100, verbose_name='Codigo del Paquete', unique=True)
    comentario1 = models.FileField(upload_to="proyecto/comentarios/", blank=True, null=True)
    comentario2 = models.FileField(upload_to="proyecto/comentarios/", blank=True, null=True)
    version = models.ManyToManyField(Version, through='PaqueteDocumento') #Relacion muchos a muchos, se redirecciona a la tabla auxiliar que se indica acá de otra manera no se podrian agregar varias veces los documentos, si bien se podria agregar 2 o mas veces el mismo documento, desconozco si se puede para varios proyectos el mismo documento.
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creacion", default=timezone.now, editable=True)
    fecha_respuesta = models.DateTimeField(verbose_name="Fecha de respuesta", blank=True, null=True) #a que fecha corresponde?
    asunto = models.CharField(verbose_name="Asunto", max_length=300)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="propietario")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinatario")
    status = models.BooleanField(verbose_name="Status", default=0, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="proyecto")
    tipo = models.IntegerField(verbose_name="Tipo de Paquete", choices=TYPE_PQUETE, default=1)

    def __str__(self):
        return str(self.codigo)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['descripcion'] = {'id': self.descripcion, 'name': self.get_descripcion_display()}
        item['fecha_creacion'] = self.fecha_creacion
        return item

class PaqueteDocumento(models.Model): #Tabla auxiliar que basicamente es lo mismo que crea automaticamente django para la realizacion de un many to many, pero customizable a lo que necesitemos, cosa que mas adelante si necesitamos almacenar otra informacion del registro de los paquetes, se puede hacer
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.documento_id.Descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        item['version'] = {'id': self.version, 'name': self.get_version_display()}
        item['paquete'] = {'id': self.paquete, 'name': self.get_paquete_display()}
        item['fecha_creacion'] = self.fecha_creacion
        return item

class PaqueteAttachment(models.Model):
    paquete = models.ForeignKey(Paquete, verbose_name="Paquete", related_name="attachments", on_delete=models.CASCADE, null=True)
    file = models.FileField(verbose_name="Archivo", upload_to="proyecto/documentos/adjuntos")

#################################################
                # PREVIZUALIZACIONES
#################################################

# PREVISUALIZACION DEL LA VERSION
class PrevVersion(models.Model):
    prev_fecha = models.DateTimeField(verbose_name="Fecha Version", auto_now_add=True)
    prev_documento_fk = models.ForeignKey(Documento, on_delete=models.CASCADE) #relacion por defecto one to many en django
    prev_archivo = models.FileField(upload_to="proyecto/documentos/", blank=True, null=True)
    prev_revision = models.IntegerField(choices=TYPES_REVISION, verbose_name="Revisión", blank=True)
    prev_estado_cliente = models.IntegerField(choices=ESTADOS_CLIENTE, blank=True, null=True)
    prev_estado_contratista = models.IntegerField(choices=ESTADO_CONTRATISTA, blank=True, null=True)
    prev_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creador")
    prev_valido = models.BooleanField(verbose_name="Valido", default=1) #1=VALIDO  0=ANULADO


# FIN PREVISUALIZACION 

# PREVISUALIZACION DEL PAQUETE
class PrevPaquete(models.Model):
    TYPE_PQUETE = (
        ('', "------"),
        (1, "Información Técnica"),
        (2, "Informativo"),
    )
    prev_documento = models.ManyToManyField(PrevVersion, through='PrevPaqueteDocumento') #Relacion muchos a muchos, se redirecciona a la tabla auxiliar que se indica acá de otra manera no se podrian agregar varias veces los documentos, si bien se podria agregar 2 o mas veces el mismo documento, desconozco si se puede para varios proyectos el mismo documento.
    prev_comentario1 = models.FileField(upload_to="proyecto/comentarios/", blank=True, null=True)
    prev_comentario2 = models.FileField(upload_to="proyecto/comentarios/", blank=True, null=True)
    prev_fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    prev_fecha_respuesta = models.DateTimeField(verbose_name="Fecha de respuesta", editable=True, blank=True, null=True) #a que fecha corresponde?
    prev_asunto = models.CharField(verbose_name="Asunto", max_length=300)
    prev_descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    prev_propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prevpropietario")
    prev_receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prevdestinatario")
    prev_status = models.BooleanField(verbose_name="Status", default=0, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="prev_paquete", null=False)
    tipo = models.IntegerField(verbose_name="Tipo de Paquete", choices=TYPE_PQUETE, default=1)


    def __str__(self):
        return self.prev_asunto

# PREVISUALIZACION DEL PAQUETEDOCUMENTO
class PrevPaqueteDocumento(models.Model): #Tabla auxiliar que basicamente es lo mismo que crea automaticamente django para la realizacion de un many to many, pero customizable a lo que necesitemos, cosa que mas adelante si necesitamos almacenar otra informacion del registro de los paquetes, se puede hacer
    prev_version = models.ForeignKey(PrevVersion, on_delete=models.CASCADE)
    prev_paquete = models.ForeignKey(PrevPaquete, on_delete=models.CASCADE)
    prev_fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.prev_documento_id.Descripcion)

class PrevPaqueteAttachment(models.Model):
    prev_paquete = models.ForeignKey(PrevPaquete, related_name="attachments",verbose_name="Prev Paquete", on_delete=models.CASCADE, null=True)
    file = models.FileField(verbose_name="Archivo", upload_to="proyecto/documentos/adjuntos")

#################################################
                # BORRADORES
#################################################

class BorradorPaquete(models.Model):
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="propietario_borrador", blank=True, null=True, default=None)
    prev_paquete = models.OneToOneField(PrevPaquete, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.asunto