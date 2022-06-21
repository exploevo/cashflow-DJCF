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
                    if XMLUpload.objects.filter(name=f.name).exists():
                        messages.warning(request, f"File {f.name} already exist")
                    else:
                        messages.success(request, f"New file uploaded: {f.name}")
                        instance = XMLUpload(name=f.name, file=f)
                        instance.uploaded_by = request.user
                        instance.save()
                        with open('media/xmlfiles/'+f.name, encoding='unicode_escape') as fd:
                            obj = xmltodict.parse(fd.read())
                            df = pd.DataFrame(obj)
                            #CLIENT INSERT 
                            c_iva = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
                            c_fis = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['CodiceFiscale']
                            try: 
                                company=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Denominazione']
                            except KeyError:
                                company = ''
                            try:
                                name=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Nome']
                                l_name = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Cognome']
                            except KeyError:
                                name = ''
                                l_name = ''
                            user = request.user
                            messages.info(request, f"CLIENT: {c_iva}, {c_fis}, {company}, {name}, {l_name}")
                            client_ins = Client(piva=c_iva, cod_fiscale = c_fis, company = company, name = name, last_name = l_name, user = user)
                            
                            #SUPPLIER INSERT 
                            s_iva = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
                            s_fis = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['CodiceFiscale']
                            try: 
                                company=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Denominazione']
                            except KeyError:
                                company = ''
                            try:
                                name=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Nome']
                                l_name = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Cognome']
                            except KeyError:
                                name = ''
                                l_name = ''
                            messages.info(request, f"SUPPLIER: {c_iva}, {c_fis}, {company}, {name}, {l_name}")
                            supplier_ins = Supplier(piva=s_iva, cod_fiscale = s_fis, company = company, name = name, last_name = l_name, user = user)
                            #Save client and supplier to the DB
                            client_ins.save()
                            supplier_ins.save()
                            #INVOICE DATA
                            doc_num = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['Numero']
                            pay_cond = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['CondizioniPagamento']
                            pay_mod = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['ModalitaPagamento']
                            date_inv = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['DataRiferimentoTerminiPagamento']
                            pay_days = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['GiorniTerminiPagamento']
                            date_pay = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['DataScadenzaPagamento']
                            amount = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['ImportoPagamento']
                            client = Client.objects.get(piva=c_iva)
                            supplier = Supplier.objects.get(piva=s_iva)
                            messages.info(request, f"INVOICE: {pay_cond}, {pay_mod}, {date_inv}, {pay_days}, {date_pay}, {amount}, {client}, {supplier} ")
                            invoice_ins = Invoice(doc_num = doc_num, payment_cond=pay_cond, payment_mod = pay_mod, 
                                    date_invoice = date_inv, payment_days = pay_days, 
                                    date_payment = date_pay, amount_invoice = amount,
                                    client = client, supplier = supplier)
                            #Save the data 
                            if Invoice.objects.filter(doc_num=doc_num).exists():
                                messages.warning(request, f"INVOICE number {doc_num} already exixst ")
                            else:
                                invoice_ins.save()
                            # the process of parsing the file
                            '''
                           OK 1 check if the invoice file already exists 
                           OK 2 check if the client or the seller is already inside the db 
                           OK 3 if it is not add client and seller and save the id 
                           OK 4 insert the data inside the invoice and the id of the client or the seller 
                           OK 5 save all and return success or error
                            '''
                else:
                    messages.error(request, f"{f.name} Is not an xml upload stopped! ")
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
