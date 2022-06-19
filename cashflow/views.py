from contextvars import Context
from email import message
from django.shortcuts import render, redirect
# from django.views import generic
# from django.contrib.auth import login
from django.contrib import messages
from pathlib import Path

from .models import Client, Supplier, Invoice, XMLUpload
from .forms import XMLForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    client_list = Client.objects.all()
    supplier_list = Supplier.objects.all()
    invoice_list = Invoice.objects.all()
    
    context = {
    'client_list' : client_list,
    'supplier_list' : supplier_list,
    'invoice_list' : invoice_list,
    }

    return render(request, 'index.html', context=context)


def add_xml_file(request):
    if request.method == 'POST':
        form = XMLForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                if f.name.split(".")[-1] == 'xml':
                    messages.success(request, f"New file uploaded: {f.name}")
                else:
                    messages.error(request, f"{f.name} Is not an xml upload stopped! ")
                    return redirect('cashflow-index')
                instance = XMLUpload(file=f)
                instance.uploaded_by = request.user
                instance.save()
                
                #xml_upload = f.save(commit=False) #to upload the form without saving it
                #xml_upload.uploaded_by = request.user #to assign the user field 
                #xml_upload.save()

        return redirect('cashflow-index')
    else:
        form = XMLForm()

    context = {'form': form}
    return render(request, 'cashflow/add_xml_file.html', context=context)
            












def counter(request):
    text = request.POST['text']
    number = len(text.split())
    return render(request, 'cashflow/counter.html', {'number': number})
