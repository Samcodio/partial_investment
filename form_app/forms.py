from .models import *
from django.forms import *


class post_form(ModelForm):
    class Meta:
        model = Post_pdf
        fields = ['pdf_name', 'pdf_file']


class EditProfileInfo(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'bank_name', 'account_name', 'account_number']

