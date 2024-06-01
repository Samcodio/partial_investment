from django import forms
from form_app.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg',
                                                                 'required': 'true', 'type': 'password',
                                                                 'id': 'exampleInputPassword1', 'placeholder': 'Password',
                                                                 'autocomplete': 'new-password'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg',
                                                                         'required': 'true', 'type': 'password',
                                                                         'id': 'exampleInputPassword2',
                                                                         'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'account_number', 'account_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                               'autofocus': 'true', 'required': 'true',
                                               'id': 'exampleInputUsername1', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                 'required': 'true',
                                                 'id': 'exampleInputFirstName', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                'required': 'true',
                                                'id': 'exampleInputLastName', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                            'required': 'true', 'type': 'email',
                                            'id': 'exampleInputEmail', 'placeholder': 'Email'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                     'required': 'true',
                                                     'id': 'exampleInputAccountNumber',
                                                     'placeholder': 'Account Number'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                   'required': 'true',
                                                   'id': 'exampleInputAccountName', 'placeholder': 'AccountName'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', 'Password and Confirm Password do not match')
        return confirm_password

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
