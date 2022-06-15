### Markdown Notes:
- **bold**
- *italic*
- ***bold italic***
# Super Big
## Sub Big
### Sub Sub Big

### Tipo di Documento
- TD01	Fattura
- TD02	Acconto/anticipo su fattura
- TD03	Acconto/Anticipo su parcella
- TD04	Nota di Credito
- TD05	Nota di Debito
- TD06	Parcella
- TD16	Integrazione fattura reverse charge interno
- TD17	Integrazione/autofattura per acquisto servizi dall’estero
- TD18	Integrazione per acquisto di beni intracomunitari
- TD19	Integrazione/autofattura per acquisto di beni ex art.17 c.2 DPR n. 633/72
- TD20	Autofattura per regolarizzazione e integrazione delle fatture (art.6 c.8 d.lgs. 471 97 o art.46 c.5 D.L. 331/93)
- TD21	Autofattura per splafonamento
- TD22	Estrazione beni da Deposito IVA
- TD23	Estrazione beni da Deposito IVA con versamento dell’IVA
- TD24	Fattura differita di cui all’art.21, comma 4, lett. a)
- TD25	Fattura differita di cui all’art.21, comma 4, terzo periodo lett. b)
- TD26	Cessione di beni ammortizzabili e per passaggi interni (ex art.36 DPR 633/72)
- TD27	Fattura per autoconsumo o per cessioni gratuite senza rivalsa

### Tipo Cassa Previdenza
- TC01	Cassa Nazionale Previdenza e Assistenza Avvocati e Procuratori Legali
- TC02	Cassa Previdenza Dottori Commercialisti
- TC03	Cassa Previdenza e Assistenza Geometri
- TC04	Cassa Nazionale Previdenza e Assistenza Ingegneri e Architetti Liberi Professionisti
- TC05	Cassa Nazionale del Notariato
- TC06	Cassa Nazionale Previdenza e Assistenza Ragionieri e Periti Commerciali
- TC07	Ente Nazionale Assistenza Agenti e Rappresentanti di Commercio (ENASARCO)
- TC08	Ente Nazionale Previdenza e Assistenza Consulenti del Lavoro (ENPACL)
- TC09	Ente Nazionale Previdenza e Assistenza Medici (ENPAM)
- TC10	Ente Nazionale Previdenza e Assistenza Farmacisti (ENPAF)
- TC11	Ente Nazionale Previdenza e Assistenza Veterinari (ENPAV)
- TC12	Ente Nazionale Previdenza e Assistenza Impiegati dell'Agricoltura (ENPAIA)
- TC13	Fondo Previdenza Impiegati Imprese di Spedizione e Agenzie Marittime
- TC14	Istituto Nazionale Previdenza Giornalisti Italiani (INPGI)
- TC15	Opera Nazionale Assistenza Orfani Sanitari Italiani (ONAOSI)
- TC16	Cassa Autonoma Assistenza Integrativa Giornalisti Italiani (CASAGIT)
- TC17	Ente Previdenza Periti Industriali e Periti Industriali Laureati (EPPI)
- TC18	Ente Previdenza e Assistenza Pluricategoriale (EPAP)
- TC19	Ente Nazionale Previdenza e Assistenza Biologi (ENPAB)
- TC20	Ente nazionale previdenza e assistenza professione infermieristica (ENPAPI)
- TC21	Ente nazionale previdenza e assistenza psicologi (ENPAP)
- TC22	INPS

### Condizioni di pagamento Fatt. elettroniche - Payment Conditions
- **Non configurato**: non viene gestito il tipo di pagamento;
- **TP01 Pagamento a rate**: viene impostato un pagamento a rate dove è possibile impostare una sola rata, nel caso infatti in cui il cliente non abbia saldato la fattura al momento dell’emissione o sia necessario indicare dei dati Bancari, attraverso questo tipo di pagamento sarà possibile impostare tali dati.
- **TP02 Pagamento completo**: va impostato nel caso in cui il pagamento sia stato già completato;
- **TP03 Anticipo**: nel caso in cui un cliente depositi un anticipo si potrà utilizzare questa modalità di pagamento indicando i dati specifici.

### Modalità pagamento Fatt. elettroniche
- **MP01** contanti
- **MP02** assegno
- **MP03** assegno circolare
- **MP04** contanti presso Tesoreria
- **MP05** bonifico
- **MP06** vaglia cambiario
- **MP07** bollettino bancario
- **MP08** carta di pagamento
- **MP09** RID
- **MP10** RID utenze
- **MP11** RID veloce
- **MP12** RIBA
- **MP13** MAV
- **MP14** quietanza erario
- **MP15** giroconto su conti di contabilità speciale
- **MP16** domiciliazione bancaria
- **MP17** domiciliazione postale
- **MP18** bollettino di c/c postale
- **MP19** SEPA Direct Debit
- **MP20** SEPA Direct Debit CORE
- **MP21** SEPA Direct Debit B2B
- **MP22** Trattenuta su somme già riscosse

### Elementi XML per dizinario e DB
- p:FatturaElettronica 
    - FatturaElettronicaHeader
        - CedentePrestatore ***Table CedentePrestatore -supplier ***
            - IdFiscaleIVA
               - **IdCodice** -> P.IVA
            - **CodiceFiscale** -> Cod.Fis (può essere diverso per persona fisica)
            - Anagrafica
               - **Denominazione** -> Deniminazione Ditta Cedente
            ---
        - CessionarioCommittente ***Table CessionarioCommittente client ***
            - IdFiscaleIVA
               - **IdCodice** -> P.IVA
            - **CodiceFiscale** -> Cod.Fis (può essere diverso per persona fisica)
            - Anagrafica
               - **Denominazione** -> Denominazione ditta Committente
               - **Nome** -> Nome ditta (per ditte individuali)
               - **Cognome** -> Cognome ditta (per ditte individuali)
    - FatturaElettronicaBody **Table Fatture Elettroniche - invoice **
        - DatiPagamento
            - CondizioniPagamento -> **Scelta multipla condizioni di pagamento (foreinKey Prestatore - Committene)**
        - DettaglioPagamento
            - ModalitaPagamento -> **scleta multipla Modalità di pagamento (foreinKey Prestatore - Committene)**
            - **DataRiferimentoTerminiPagamento** -> data emissione fattura
            - **GiorniTerminiPagamento** -> numero giorni di pagamento
            - **DataScadenzaPagamento** -> data di pagamento per cassa
            - **ImportoPagamento** -> importo da pagare
            - 
				