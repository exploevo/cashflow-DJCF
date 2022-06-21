
from django.shortcuts import render, redirect
# from django.views import generic
# from django.contrib.auth import login
from django.contrib import messages

from .models import Client, Supplier, Invoice, XMLUpload
from .forms import XMLForm
from .utils import process_xml_file


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
            for file in files:
                if file.name.split(".")[-1] == 'xml':
                    if XMLUpload.objects.filter(name=file.name).exists():
                        messages.warning(request, f"File {file.name} already exist")
                    else:
                        messages.success(request, f"New file uploaded: {file.name}")
                        xml_upload = XMLUpload(name=file.name, file=file)
                        xml_upload.uploaded_by = request.user
                        xml_upload.save()
                        client_data, supplier_data, invoice_data = process_xml_file(xml_upload.file)
                           
                        user = request.user
                        messages.info(request, 'CLIENT: {piva}, {cod_fiscale}, {company}, {name}, {last_name}'.format(**client_data))
                        client = Client(**client_data, user=user)
                        messages.info(request, 'SUPPLIER: {piva}, {cod_fiscale}, {company}, {name}, {last_name}'.format(**supplier_data))
                        supplier = Supplier(**supplier_data, user=user)
                        #Save client and supplier to the DB
                        client.save()
                        supplier.save()
                        messages.info(request, "INVOICE: {payment_cond}, {payment_mod}, {date_invoice}, {payment_days}, {date_payment}, {amount_invoice}, {client}, {supplier}".format(**invoice_data, client=client, supplier=supplier))
                        invoice = Invoice(**invoice_data, client=client, supplier=supplier)
                        #Save the data 
                        if Invoice.objects.filter(doc_num=invoice.doc_num).exists():
                            messages.warning(request, f"INVOICE number {invoice.doc_num} already exist.")
                        else:
                            invoice.save()
                            # the process of parsing the file
                            '''
                           OK 1 check if the invoice file already exists 
                           OK 2 check if the client or the seller is already inside the db 
                           OK 3 if it is not add client and seller and save the id 
                           OK 4 insert the data inside the invoice and the id of the client or the seller 
                           OK 5 save all and return success or error
                            '''
                else:
                    messages.error(request, f"{file.name} Is not an xml upload stopped! ")
                    return redirect('cashflow-index')
                #OLD PROCEDURE
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
