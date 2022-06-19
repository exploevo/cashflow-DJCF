from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
#from django.contrib.auth.models import AbstractUser

# Base User Model
User = get_user_model()

#How To inser a Custom User Model?
#class User(AbstractUser):
#    piva = models.CharField(max_length=11, unique=True)

# Create your models (tables) here.
class Client(models.Model):
    piva = models.CharField(primary_key=True, max_length=11)
    cod_fiscale = models.CharField(max_length=16)
    company = models.CharField(max_length=30, blank=True )
    name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    #ForeingKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company}, {self.name}, {self.last_name}'

class Supplier(models.Model):
    piva = models.CharField(primary_key=True, max_length=11)
    cod_fiscale = models.CharField(max_length=16)
    company = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company}, {self.name}, {self.last_name}'

class Invoice(models.Model):
    #Attrbutes
    PAYMENT_COND = (
        ('NCON', 'Non Indicato'),
        ('TP01', 'TP01 - Pagamento Rate'),
        ('TP02', 'TP02 - Pagamento effettuato'),
        ('TP03', 'TP03 - Pagamento Anticipato'),
    )
    PAYMENT_MOD = (
        ('MP01', 'MP01 - contanti'),
        ('MP02', 'MP02 - assegno'),
        ('MP03', 'MP03 - assegno circolare'),
        ('MP04', 'MP04 - contanti presso Tesoreria'),
        ('MP05', 'MP05 - bonifico'),
        ('MP06', 'MP06 - vaglia cambiario'),
        ('MP07', 'MP07 - bollettino bancario'),
        ('MP08', 'MP08 - carta di pagamento'),
        ('MP09', 'MP09 - RID'),
        ('MP10', 'MP10 - RID utenze'),
        ('MP11', 'MP11 - RID veloce'),
        ('MP12', 'MP12 - RIBA'),
        ('MP13', 'MP13 - MAV'),
        ('MP14', 'MP14 - quietanza erario'),
        ('MP15', 'MP15 - giroconto su conti di contabilità speciale'),
        ('MP16', 'MP16 - domiciliazione bancaria'),
        ('MP17', 'MP17 - domiciliazione postale'),
        ('MP18', 'MP18 - bollettino di c/c postale'),
        ('MP19', 'MP19 - SEPA Direct Debit'),
        ('MP20', 'MP20 - SEPA Direct Debit CORE'),
        ('MP21', 'MP21 - SEPA Direct Debit B2B'),
        ('MP22', 'MP22 - Trattenuta su somme già riscosse'),
    )
    payment_cond = models.CharField(max_length=4, choices=PAYMENT_COND)
    payment_mod = models.CharField(max_length=4, choices=PAYMENT_MOD)
    date_invoice = models.DateField()
    payment_days = models.IntegerField(blank=True)
    date_payment = models.DateField()
    amount_invoice = models.FloatField()
    # ForeignKey are Many to one relationship: Many invoices to one Client / Seller
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices', blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='invoices', blank=True)
    
    class Meta:
        ordering = ['date_invoice', 'date_payment']
    
    '''def get_absolute_url(self):
        #This is the URL that for the single invoice
        return reverse('invoice', kwargs={'id' : self.id})'''
    
    def __str__(self):
        return f'{self.date_invoice}, {self.date_payment}, {self.client}, {self.seller}'

class XMLUpload(models.Model):
    # Attributes of the model
    file = models.FileField(upload_to='xmlfiles')
    datetime_uploaded = models.DateField(auto_now_add=True)

    # Relationships from the model
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xml_uploads')

    def __str__(self):
        return f'{self.file}'
    
    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    