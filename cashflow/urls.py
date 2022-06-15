from django.urls import path
from . import views

urlpatterns = [
    #path deve puntare al nome dato a def in views.nomedef e name sarà il riferimento per il render
    path('', views.index, name='cashflow-index'),
    path('counter/', views.counter, name='cashflow-count'), 
    path('files/xml/add', views.add_xml_file, name='add_xml_file'),
]