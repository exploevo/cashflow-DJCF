from contextvars import Context
from email import message
from django.shortcuts import render, redirect
# from django.views import generic
# from django.contrib.auth import login
from django.contrib import messages
import pandas as pd
import xmltodict

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
                    instance = XMLUpload(file=f)
                    instance.uploaded_by = request.user
                    instance.save()
                    with open('media/xmlfiles/'+f.name, encoding='unicode_escape') as fd:
                        obj = xmltodict.parse(fd.read())
                        df = pd.DataFrame(obj)
                        messages.info(request, f"File xml: {df}")
                        # the process of parsing the file
                        '''
                        1 check if the invoice is selling or buyng in relation to the user
                        2 check if the client or the seller is already inside the db
                        3 if it is not add client and seller and save the id
                        4 insert the data inside the invoice and the id of the client or the seller
                        5 save all and return success or error
                        '''
                else:
                    messages.error(request, f"{f.name} Is not an xml upload stopped! ")
                    return redirect('cashflow-index')
                #instance = XMLUpload(file=f)
                #instance.uploaded_by = request.user
                #instance.save()
                
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
