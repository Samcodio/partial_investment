from .models import *
from django.forms import *


class post_form(ModelForm):
    class Meta:
        model = Post_pdf
        fields = ['pdf_name', 'pdf_file']

