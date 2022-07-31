from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path deve puntare al nome dato a def in views.nomedef e name sarà il riferimento per il render
    #path('', views.index, name='cashflow-index'),
    path('', views.dashboard, name = 'dashboard'),
    path('counter/', views.counter, name = 'cashflow-count'), 
    #path('files/xml/add', views.add_xml_file, name = 'add_xml_file'),
    #Login embedded URL
    #path('login/', auth_views.LoginView.as_view(), name = 'login'),
    #path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    #change password
    #path('password-change/', auth_views.PasswordChangeView.as_view(),name = 'password_change'),
    #path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),name = 'password_change_done'),
    #reset password
    #path('password-reset/', auth_views.PasswordResetView.as_view(), name = 'password_reset'),
    #path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    #path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    #path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    #path('', include('django.contrib.auth.urls')),
    #path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('dash3/', views.dash3, name='dash3'),
    path('index_work/', views.index_work, name='index_work'),
    path('index_work/', include('django.contrib.auth.urls')),
    path('index_work/datacs/', views.data_cli_sup, name='data_cli_sup'),
    path('index_work/datacs/list_invoice/', views.list_invoces, name='list_invoices'),
    path('index_work/datacs/list_invoice/<int:invoice_id>/delete', views.invoice_delete, name='invoice_delete'),
    path('index_work/datacs/list_invoice/<int:invoice_id>/view', views.invoice_view, name='invoice_view'),
    path('index_work/files/xml/add/', views.add_xml_file, name='add_xml_file'),
]