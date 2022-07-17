
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import xmltodict
import pandas as pd

from .models import Client, Supplier, Invoice, XMLUpload, Profile
from .forms import XMLForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .utils import get_client_invoice_payment_years, process_xml_file, insert_db, get_client_dashboard_data, get_supplier_dashboard_data

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
    #piva_u = Profile.objects.get(user = request.user)
    piva = request.user.profile.piva
    clients = Client.objects.filter(user=request.user).exclude(piva=piva)
    supplier = Supplier.objects.filter(user=request.user).exclude(piva=piva)
    year = request.GET.get('year') #?year=2020
    if not year:
        year = timezone.now().year
    client_list = get_client_dashboard_data(clients, int(year))
    supplier_list = get_supplier_dashboard_data(supplier, int(year))
    years = get_client_invoice_payment_years(clients)
    #print(years)
    context = {
        'clients': client_list,
        'suppliers': supplier_list,
        'years': years,
    }
    return render(request, 'cashflow/dashboard.html', context)

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
                        #return redirect('add_xml_file')
                    else:
#I need a control that the client or the supplier has the piva of the user
# otherwise I'm uploadin invoice of another user
#message the invoice does not contain the piva of the user error!
                        xml_upload = XMLUpload(name=file.name, file=file)
                        xml_upload.uploaded_by = request.user
                        # Check if xml file content is correct, if not, send error.
                        try:
                            client, supplier, _ = process_xml_file(file)
                        except Exception as e:
                            print('Error')
                            print(e)
                            messages.error(request, f"File {file.name} is NOT a correct File you must upload an XML file")
                            return redirect('add_xml_file')
                        
                        # Check if user.piva is client or suppler, if not, send error.
                        if request.user.profile.piva in {client['piva'], supplier['piva']}:
                            xml_upload.save()
                            messages.success(request, f"New file uploaded: {file.name}")
                            client_data, supplier_data, invoice_data = process_xml_file(xml_upload.file)
                            user = request.user
                            insert_db(user, client_data, supplier_data, invoice_data, request)
                        else:
                            error_message = f'File {file.name} is not an invoice of the logged in user.'
                            messages.error(request, error_message)
                            return redirect('add_xml_file')
                
                elif file.name.split(".")[-1] == 'p7m':
                    messages.error(request, f"File {file.name} is NOT a correct File you must upload an XML file")
                    return redirect('add_xml_file')
                    '''if XMLUpload.objects.filter(name=file.name).exists():
                        messages.warning(request, f"File {file.name} already exist")
                    else:
                        xml_upload = XMLUpload(name=file.name, file=file)
                        xml_upload.uploaded_by = request.user
                        xml_upload.save()
                        messages.success(request, f"New file uploaded: {file.name}")
                        client_data, supplier_data, invoice_data = process_p7m_file(file.name)
                        user = request.user
                        insert_db(user,client_data, supplier_data, invoice_data, request)'''
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
