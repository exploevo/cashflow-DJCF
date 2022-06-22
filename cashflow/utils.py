import xmltodict
import pandas as pd
import re

from pathlib import Path

import sys
#library to work with p7m files
from OpenSSL import crypto
from OpenSSL._util import (
	ffi as _ffi,
	lib as _lib,
)

def process_xml_file(file):
    xml_text = Path(file.path).read_text()
    obj = xmltodict.parse(xml_text)
    df = pd.DataFrame(obj)
    client_data = get_client_from_xml(df)
    supplier_data = get_supplier_from_xml(df)
    invoice_data = get_invoice_from_xml(df)
    return (client_data, supplier_data, invoice_data)

def process_p7m_file(file):
    with open('media/xmlfiles/' + file, 'rb') as f:
	    p7data = f.read()
    p7 = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, p7data)
    bio_out =crypto._new_mem_buf()
    res = _lib.PKCS7_verify(p7._pkcs7, _ffi.NULL, _ffi.NULL, _ffi.NULL, bio_out, _lib.PKCS7_NOVERIFY|_lib.PKCS7_NOSIGS)
    if res == 1:
        databytes = crypto._bio_to_string(bio_out)
        obj = xmltodict.parse(databytes)
        df = pd.DataFrame(obj)
        client_data = get_client_from_xml(df)
        supplier_data = get_supplier_from_xml(df)
        invoice_data = get_invoice_from_xml(df)
        return (client_data, supplier_data, invoice_data)
    else:
        errno = _lib.ERR_get_error()
        errstrlib = _ffi.string(_lib.ERR_lib_error_string(errno))
        errstrfunc = _ffi.string(_lib.ERR_func_error_string(errno))
        errstrreason = _ffi.string(_lib.ERR_reason_error_string(errno))
        print(errstrreason)

def get_client_from_xml(df):
    iva = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
    fis = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['CodiceFiscale']
    try: 
        company = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Denominazione']
    except KeyError:
        company = ''
    try:
        name=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Nome']
        last_name = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CessionarioCommittente']['DatiAnagrafici']['Anagrafica']['Cognome']
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
    iva = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['IdFiscaleIVA']['IdCodice']
    fis = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['CodiceFiscale']
    try: 
        company=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Denominazione']
    except KeyError:
        company = ''
    try:
        name=df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Nome']
        last_name = df['p:FatturaElettronica']['FatturaElettronicaHeader']['CedentePrestatore']['DatiAnagrafici']['Anagrafica']['Cognome']
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
    doc_num = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiGenerali']['DatiGeneraliDocumento']['Numero']
    payment_cond = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['CondizioniPagamento']
    payment_mod = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['ModalitaPagamento']
    date_invoice = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['Data']
    try:
        payment_days = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['GiorniTerminiPagamento']
    except KeyError:
        payment_days = '0'
    date_payment = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['DataScadenzaPagamento']
    amount_invoice = df['p:FatturaElettronica']['FatturaElettronicaBody']['DatiPagamento']['DettaglioPagamento']['ImportoPagamento']
    return {  
        'doc_num': doc_num,
        'payment_cond': payment_cond,
        'payment_mod': payment_mod,
        'date_invoice': date_invoice,
        'payment_days': payment_days, 
        'date_payment': date_payment,
        'amount_invoice': amount_invoice,
    }