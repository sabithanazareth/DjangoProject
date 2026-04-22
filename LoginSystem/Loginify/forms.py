from django import forms
from .models import UserDetails

class SignupForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserDetails.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=12)

