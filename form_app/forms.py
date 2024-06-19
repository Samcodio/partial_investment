from .models import *
from django.forms import *


class post_form(ModelForm):
    class Meta:
        model = Post_pdf
        fields = ['pdf_name', 'pdf_file', 'price']


class EditProfileInfo(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'bank_name', 'account_name', 'account_number']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg',
                                               'autofocus': 'true', 'required': 'true',
                                               'id': 'exampleInputUsername1', 'placeholder': 'Username'}),
            'first_name': TextInput(attrs={'class': 'form-control form-control-lg',
                                                 'required': 'true',
                                                 'id': 'exampleInputFirstName', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-lg',
                                                'required': 'true',
                                                'id': 'exampleInputLastName', 'placeholder': 'Last Name'}),
            'bank_name': Select(attrs={'class': 'form-control form-control-lg', 'required': 'true',
                                       'id': 'exampleInputBankName', 'placeholder': 'Bank Name'}),
            'account_number': TextInput(attrs={'class': 'form-control form-control-lg',
                                                     'required': 'true',
                                                     'id': 'exampleInputAccountNumber',
                                                     'placeholder': 'Account Number'}),
            'account_name': TextInput(attrs={'class': 'form-control form-control-lg',
                                                   'required': 'true',
                                                   'id': 'exampleInputAccountName', 'placeholder': 'AccountName'})
        }


class AdjustAmount(ModelForm):
    class Meta:
        model = UserAmount
        fields = ['amount', 'currency']

