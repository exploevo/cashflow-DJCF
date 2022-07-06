
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Client, Supplier, Invoice, XMLUpload, Profile
from .forms import XMLForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .utils import process_xml_file, process_p7m_file, insert_db

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

@login_required
def dashboard(request):
    #inserire un try except per reindirizzare (redirect) su messaggio di contatto.
    #potresti non trovare nessun record perché la partita Iva è inserita errata
    piva_u = Profile.objects.get(user = request.user)
    user_r = request.user
    clients = Client.objects.filter(user = user_r).exclude(piva = piva_u) #here I want to exclude the user piva from the list of client
    client_list = Client.objects.filter(user = request.user)
    #invoice_list = Invoice.objects.get(client = clients.piva)
    client_list2 ={}
    for client in clients:
        year = 2022
        month = 0o5 #create a range variable or xrange 
        tot = 0
        if client.name == '':
            #create a cicle of each month and create a dict
            # range from 1 to 12 or 0 to 11 where i insert the amount
            # for each month i create a dict key the number of the month value amount
            # insert an if statement to check if the month has value
            # if the month has value I sum the amount to a vatiable tot
            for m in range(1, 13):
                invoices = Invoice.objects.filter(client=client.piva, 
                                date_payment__year=year,
                                date_payment__month=m)
                if invoices.exists():
                    for invoice in invoices:
                        if client_list2:
                            client_list2[client.company].append(invoice.amount_invoice)
                        else:
                            client_list2[client.company] = [str(invoice.amount_invoice)]
                else:
                    if client_list2:
                        client_list2[client.company].append('0')
                    else:
                        client_list2[client.company] = ['0']
        else:
            for m in range(1, 13):
                invoices = Invoice.objects.filter(client=client.piva, 
                                date_payment__year=year,
                                date_payment__month=m)
                if invoices.exists():
                    for invoice in invoices:
                        if client_list2:
                            client_list2[client.name + ' ' + client.last_name].append(invoice.amount_invoice)
                        else:
                            client_list2[client.name + ' ' + client.last_name] = [str(invoice.amount_invoice)]
                else:
                    if client_list2:
                        client_list2[client.name + ' ' + client.last_name].append('0')
                    else:
                        client_list2[client.name + ' ' + client.last_name] = ['0']

    sell_for_month = {
        'cliente1': [{'gen': 100,
                    'feb': 200,
                    'mar': 150,
                    'apr': 300,
                    'mag': 230,
                    'giu': 100,
                    'lug': 50,
                    'ago': 20,
                    'set': 150,
                    'ott': 200,
                    'nov': 70,
                    'dic': 400,
                    'tot': 1970}],
        'cliente2': [{'gen': 80,
                    'feb': 230,
                    'mar': 120,
                    'apr': 230,
                    'mag': 260,
                    'giu': 50,
                    'lug': 0,
                    'ago': 40,
                    'set': 60,
                    'ott': 120,
                    'nov': 160,
                    'dic': 250,
                    'tot': 1600}],
        'cliente3': [{'gen': 10,
                    'feb': 20,
                    'mar': 15,
                    'apr': 30,
                    'mag': 20,
                    'giu': 10,
                    'lug': 5,
                    'ago': 2,
                    'set': 10,
                    'ott': 20,
                    'nov': 30,
                    'dic': 40,
                    'tot': 202}]
    }
    return render(request, 'cashflow/dashboard.html', {'piva_u' : piva_u,
                                                        'user_r' : user_r,
                                                        'clients' : client_list2,
                                                        'sells' : sell_for_month,
                                                        })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data=request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,
                                        data = request.POST,
                                        files = request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Data Successfully Updated!")
        #I would like to reload the page in order to see the image
        # Also the piva must be ad obliged field in order to be a valid user    
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    
    return render(request, 'cashflow/edit.html', 
                    {'user_form' : user_form, 
                    'profile_form' : profile_form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        pform = ProfileEditForm(data = request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile_form = pform.save(commit = False)
            #create the user profile
            #Profile.objects.create(user=new_user)
            messages.success(request, f"{new_user.id}")
            profile_form.user = new_user
            profile_form.save()
            messages.success(request, "Profile Successfully Created!")
            return render(request,
                          'cashflow/register_done.html',
                          {'new_user': new_user,
                          })
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request,
                  'cashflow/register.html',
                  {'user_form': user_form,
                  'profile_form' : profile_form})

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
                        insert_db(user,client_data, supplier_data, invoice_data, request)

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
                        insert_db(user,client_data, supplier_data, invoice_data, request)
                else:
                    messages.error(request, f"<h2>{file.name} Is not a valid File stopped! </h2>")
                    return redirect('cashflow-index')

        return redirect('dashboard')
    else:
        form = XMLForm()

    context = {'form': form}
    return render(request, 'cashflow/add_xml_file.html', context=context)










def counter(request):
    text = request.POST['text']
    number = len(text.split())
    return render(request, 'cashflow/counter.html', {'number': number})
