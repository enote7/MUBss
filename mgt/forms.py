from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

#USER MODEL
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


#password reset
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')



#Tasks editing
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }
