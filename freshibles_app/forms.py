from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
User = get_user_model()


class QuickPasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There's no user registered with the specified email.")
        return email

    def save(self, commit=True):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        password = self.cleaned_data['new_password1']
        user.set_password(password)
        if commit:
            user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')
    phone_number = forms.CharField(required=True, help_text='Required. Add a valid phone number.')

    class Meta:
        model = User
        fields = ('name', 'email', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Assuming username is used as email
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            return self.cleaned_data
        raise forms.ValidationError("Email and password are required")

