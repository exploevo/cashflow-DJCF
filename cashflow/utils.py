from pathlib import Path

import xmltodict
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
#library to work with p7m files
import subprocess
from OpenSSL import crypto
from OpenSSL._util import (
	ffi as _ffi,
	lib as _lib,
)

from .models import Client, Supplier, Invoice, XMLUpload

def process_xml_file(file):
    obj = xmltodict.parse(file)
    client_data = get_client_from_xml(obj)
    supplier_data = get_supplier_from_xml(obj)
    invoice_data = get_invoice_from_xml(obj)
    return (client_data, supplier_data, invoice_data)


def process_p7m_file(file):
    with open('media/xmlfiles/' + file, 'rb') as f:
        p7data = f.read()
    try:
        p7 = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, p7data)
        bio_out =crypto._new_mem_buf()
        res = _lib.PKCS7_verify(p7._pkcs7, _ffi.NULL, _ffi.NULL, _ffi.NULL, bio_out, _lib.PKCS7_NOVERIFY|_lib.PKCS7_NOSIGS)
        if res == 1:
                databytes = crypto._bio_to_string(bio_out)
    except:
        databyte = subprocess.check_output(["openssl", "cms", "-verify", "-in", 'media/xmlfiles/' + file, "-inform",
                            "der", "-noverify", "-signer", "cert.pem", "-out", "media/xmlfiles/textdata4.xml"]) 
        databytes = databyte.encode("utf-8").split(b'\x00')
  
    obj = xmltodict.parse(databytes)
    #df = pd.DataFrame(obj)
    client_data = get_client_from_xml(obj)
    supplier_data = get_supplier_from_xml(obj)
    invoice_data = get_invoice_from_xml(obj)
    return (client_data, supplier_data, invoice_data)

def get_client_from_xml(df):

    try:
        df['p:FatturaElettronica']
        head = 'p:FatturaElettronica'
    except KeyError:
        all_keys = list(df)
        head = all_keys[0]

    try:
        iva = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
    except:
        iva = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['CodiceFiscale']
    try:
        fis = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['CodiceFiscale']
    except KeyError:
        fis = ''
    try: 
        company = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Denominazione']
    except KeyError:
        company = ''
    try:
        name=df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Nome']
        last_name = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Cognome']
    except KeyError:
        name = ''
        last_name = ''
    return {
        'piva': iva,
        'cod_fiscale': fis,
        'company': company,
        'name': name,
        'last_name': last_name,
    }

def get_supplier_from_xml(df):
    try:
        df['p:FatturaElettronica']
        head = 'p:FatturaElettronica'
    except KeyError:
        all_keys = list(df)
        head = all_keys[0]
    try:
        iva = df[head]['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
    except:
        iva = df[head]['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['CodiceFiscale']
    try:
        fis = df[head]['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['CodiceFiscale']
    except KeyError:
        fis = ''
    try: 
        company=df[head]['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Denominazione']
    except KeyError:
        company = ''
    try:
        name=df[head]['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Nome']
        last_name = df[head]['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Cognome']
    except KeyError:
        name = ''
        last_name = ''
    return {
        'piva': iva,
        'cod_fiscale': fis,
        'company': company,
        'name': name,
        'last_name': last_name,
    }

def get_invoice_from_xml(df):
    try:
        df['p:FatturaElettronica']
        head = 'p:FatturaElettronica'
    except KeyError:
        all_keys = list(df)
        head = all_keys[0]
    
    doc_num = df[head]['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['Numero']
    try:
        payment_cond = df[head]['FatturaElettronicaBody']['DatiPagamento']['CondizioniPagamento']
    except KeyError:
        payment_cond = 'NCON'
    try:
        payment_mod = df[head]['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['ModalitaPagamento']
    except KeyError:
        payment_mod = 'MP01'
    date_invoice = df[head]['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['Data']
    try:
        payment_days = df[head]['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['GiorniTerminiPagamento']
    except KeyError:
        payment_days = '0'
    try:
        date_payment = df[head]['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['DataScadenzaPagamento']
    except KeyError:
        date_payment = df[head]['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['Data']
    
    amount_invoice = df[head]['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['ImportoTotaleDocumento']
    pay_conf_list = ['MP01','MP02','MP03','MP08','MP09','MP10','MP11','MP12',
                    'MP13','MP14','MP15','MP19','MP20','MP21','MP22']

    payed = payment_mod in pay_conf_list
  
    return {  
        'doc_num': doc_num,
        'payment_cond': payment_cond,
        'payment_mod': payment_mod,
        'date_invoice': date_invoice,
        'payment_days': payment_days, 
        'date_payment': date_payment,
        'amount_invoice': amount_invoice,
        'payed': payed,
    }


#Client dashboard 

def get_client_dashboard_data(clients, year=timezone.now().year):
    """Create the table for the dashboard."""
    client_list = {}
    for client in clients:
        value = []
        #this could be made in one function to be reusable
        for m in range(1, 13):
            tot_month = 0
            invoices = Invoice.objects.filter(client=client.piva, 
                                                date_payment__year=year,
                                                date_payment__month=m)
            if invoices.exists():
                #for imvoice of the same month must sum the import 
                #and create a single value
                for invoice in invoices:
                    tot_month += invoice.amount_invoice
                value.append(round(tot_month ,2))
            else:
                value.append(0)
        tot = sum(value)
        if tot == 0:
            pass
        else:
            value.append(round(tot, 2))
            if not client.name:
                client_list[client.company] = [client.piva], value
            else:
                client_list[client.name + ' ' + client.last_name] = [client.piva], value 
    return client_list

def get_supplier_dashboard_data(suppliers, year=timezone.now().year):
    supplier_list = {}
    for supplier in suppliers:
        value = []
        
        #this could be made in one function to be reusable
        for m in range(1, 13):
            tot_month = 0
            invoices = Invoice.objects.filter(supplier=supplier.piva, 
                                                date_payment__year=year,
                                                date_payment__month=m)
            if invoices.exists():
                #for imvoice of the same month must sum the import 
                #and create a single value
                for invoice in invoices:
                    tot_month += invoice.amount_invoice
                value.append(round(tot_month ,2))
            else:
                value.append(0)
        tot = sum(value)
        if tot == 0:
            pass
        else:
            value.append(round(tot, 2))
            if not supplier.name:
                supplier_list[supplier.company] = value
            else:
                supplier_list[supplier.name + ' ' + supplier.last_name] = value 
    return supplier_list

def get_client_invoice_list(list_inovices):
    invoice_list = {}
    for invoice in list_inovices:
        value = []
        value.append(invoice.date_invoice)
        value.append(invoice.date_payment)
        value.append(invoice.amount_invoice)
        value.append(invoice.payed)
        invoice_list[invoice.client]=value
        return invoice_list

def get_client_invoice_payment_years(clients):
    all_payment_years = []
    for client in clients:
        invoices = client.invoices.all()
        for invoice in invoices:
            all_payment_years.append(invoice.date_payment.year)
    invoice_year_range = list(set(all_payment_years))  
    # invoice_year_ragne = set(invoice.payment_date.year for client in clients for invoice in client.invoices.all())
    return invoice_year_range