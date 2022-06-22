
from django.shortcuts import render, redirect
# from django.views import generic
# from django.contrib.auth import login
from django.contrib import messages

from .models import Client, Supplier, Invoice, XMLUpload
from .forms import XMLForm
from .utils import process_xml_file, process_p7m_file

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
                        xml_upload = XMLUpload(name=file.name, file=file)
                        xml_upload.uploaded_by = request.user
                        xml_upload.save()
                        messages.success(request, f"New file uploaded: {file.name}")
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

                elif file.name.split(".")[-1] == 'p7m':
                    if XMLUpload.objects.filter(name=file.name).exists():
                        messages.warning(request, f"File {file.name} already exist")
                    else:
                        xml_upload = XMLUpload(name=file.name, file=file)
                        xml_upload.uploaded_by = request.user
                        xml_upload.save()
                        messages.success(request, f"New file uploaded: {file.name}")
                        client_data, supplier_data, invoice_data = process_p7m_file(file.name)
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
                    return redirect('cashflow-index')
                else:
                    messages.error(request, f"<h2>{file.name} Is not a valid File stopped! </h2>")
                    return redirect('cashflow-index')

        return redirect('cashflow-index')
    else:
        form = XMLForm()

    context = {'form': form}
    return render(request, 'cashflow/add_xml_file.html', context=context)










def counter(request):
    text = request.POST['text']
    number = len(text.split())
    return render(request, 'cashflow/counter.html', {'number': number})
