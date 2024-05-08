from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django import forms

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2',)

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Indtast din nuværende adgangskode'
        self.fields['old_password'].label = ''
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Ny adgangskode'
        self.fields[
            'new_password1'].help_text = '<div class="form-text text-muted"><small><ul><li>Din adgangskode kan ikke være for ens med dine andre personlige oplysninger.</li><li>Din adgangskode skal indeholde mindst 8 tegn.</li><li>Din adgangskode kan ikke være en typisk brugt adgangskode.</li><li>Din adgangskode kan ikke bestå udelukkende af tal.</li></ul></small></div>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Gentag adgangskode'
        self.fields[
            'new_password2'].help_text = '<div class="form-text text-muted"><small>Indtast den samme nye adgangskode som før til bekræftelse.</small></div>'
        self.fields['new_password2'].label = ''

class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'type': 'hidden', }))
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Indtast email'}))
    first_name = forms.CharField(label="Fornavn", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast fornavn'}))
    last_name = forms.CharField(label="Efternavn", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast efternavn'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Indtast brugernavn'
        self.fields['username'].help_text = '<div class="form-text text-muted"><small>Påkrævet. 150 tegn eller færre. Kun bogstaver, cifre og @ /. / + / - / _.</small></div>'
        self.fields['username'].label = 'Brugernavn'


class SignUpForm(UserCreationForm):
    email = forms. EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Indtast email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Indtast fornavn'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Indtast efternavn'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Indtast brugernavn'
        self.fields['username'].help_text = '<div class="form-text text-muted"><small>Påkrævet. 150 tegn eller færre. Kun bogstaver, cifre og @ /. / + / - / _.</small></div>'
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Indtast adgangskode'
        self.fields['password1'].help_text = '<div class="form-text text-muted"><small>Din adgangskode kan ikke være for ens med dine andre personlige oplysninger.<ul><li>Din adgangskode skal indeholde mindst 8 tegn.</li><li>Din adgangskode kan ikke være en almindelig adgangskode.</li><li>Din adgangskode kan ikke være helt numerisk.</li></ul></small></div>'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Gentag adgangskode'
        self.fields['password2'].help_text = '<div class="form-text text-muted"><small>Indtast den samme adgangskode som før til bekræftelse.</small></div>'
        self.fields['password2'].label = ''
