from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from re import match

User = get_user_model()

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class CustomPasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        if self.is_invalid_password(password1):
            raise forms.ValidationError('Invalid password. </br>\
            Password must be minimum 6 characters long </br>\
            and matches (a-z, A-Z, 0-9, _@$!%*?&-)')
    
    def is_invalid_password(self, password: str) -> bool:
        password_pattern = r'^[a-zA-Z0-9_@$!%*?&-]{6,}$'
        return match(password_pattern, password) is None