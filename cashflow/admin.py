from django.contrib import admin
from .models import Client, Supplier, Invoice, XMLUpload, Profile

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['piva', 'company', 'name', 'last_name']
    list_filter = ['company', 'name', 'last_name']
    search_fields = ['piva', 'company', 'name', 'last_name']
    ordering = ['company', 'name', 'last_name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['piva', 'company', 'name', 'last_name']
    list_filter = ['company', 'name', 'last_name']
    search_fields = ['piva', 'company', 'name', 'last_name']
    ordering = ['company', 'name', 'last_name']

@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    list_display = ['client', 'supplier', 'date_invoice', 'date_payment', 'amount_invoice']
    list_filter = ['date_invoice', 'date_payment', 'client', 'supplier']
    search_fields = ['client__name', 'client__last_name', 'client__company',
                    'supplier__name', 'supplier__last_name', 'supplier__company',
                    'amount_invoice']
    ordering = ['date_invoice', 'date_payment', 'client', 'supplier']

@admin.register(XMLUpload)
class XMLUpload(admin.ModelAdmin):
    list_display = ['name', 'uploaded_by', 'datetime_uploaded', 'file']
    list_filter = ['name', 'uploaded_by']
    search_fields = ['name']
    ordering = ['name', 'uploaded_by', 'datetime_uploaded']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'piva', 'photo']
    raw_id_fields = ['user']