from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('export/', views.export_document, name='panel-export'),
    # path('import/', views.import_document, name='panel-import'),
    path('index/', views.ListDocumento.as_view(), name='PanelCarga'),
    path('seleccion/', views.ProyectoSelectView.as_view() , name="proyecto-select"),
    path('proyecto/lista/', login_required(views.ProyectoList.as_view()) , name="proyecto-lista"),
    path('proyecto/crear/', views.CreateProyecto.as_view() , name="proyecto-crear"),
    path('proyecto/detalle/', views.DetailProyecto.as_view() , name="proyecto-detalle"),
    path('documento/crear/', views.CreateDocumento.as_view() , name="documento-crear"),
    path('documento/detalle/', views.DetailDocumento.as_view() , name="documento-detalle"),
    path('documento/actualizar/<int:pk>/', views.UpdateDocumento.as_view() , name="documento-actualizar"),
    path('documento/eliminar/<int:pk>/', views.DeleteDocumento.as_view() , name="documento-eliminar"),
    path('revision/crear/', login_required(views.CreateRevision.as_view()) , name="revision-crear"),

]
