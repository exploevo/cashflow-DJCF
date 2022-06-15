from turtle import circle
from django.contrib import admin
from .models import Client, Supplier, Invoice, XMLUpload

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['piva', 'company', 'name', 'last_name']
    list_filter = ['piva', 'company', 'name', 'last_name']
    search_fields = ['piva', 'company', 'name', 'last_name']
    ordering = ['company', 'name', 'last_name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['piva', 'company', 'name', 'last_name']
    list_filter = ['piva', 'company', 'name', 'last_name']
    search_fields = ['piva', 'company', 'name', 'last_name']
    ordering = ['company', 'name', 'last_name']

@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    list_display = ['client', 'seller', 'date_invoice', 'date_payment', 'amount_invoice']
    list_filter = ['date_invoice', 'date_payment', 'client', 'seller']
    search_fields = ['client', 'seller', 'date_invoice', 'date_payment']
    ordering = ['date_invoice', 'date_payment', 'client', 'seller']

@admin.register(XMLUpload)
class XMLUpload(admin.ModelAdmin):
    list_display = ['uploaded_by', 'datetime_uploaded', 'file']
    list_filter = ['uploaded_by', 'file']
    search_fields = ['uploaded_by', 'datetime_uploaded', 'file']
    ordering = ['uploaded_by', 'datetime_uploaded', 'file']