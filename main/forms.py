from django import forms
from django.contrib.auth import get_user_model
from gamewebsite import settings

User = get_user_model()


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'User is not validate')
        if not user.check_password(password):
            raise forms.ValidationError(f'User is not validate')
        return self.cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()
    birthday = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['email'].label = 'Email'
        self.fields['birthday'].label = 'Birthday'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already registered')
        return username

    def clen(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise  forms.ValidationError('Password mismatch')
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'password', 'confirm_password']
        widgets = {
            'birthday': DateInput()
        }


class ButtonForm(forms.Form):
    btn = forms.CharField()