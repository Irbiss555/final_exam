from django.contrib.auth import get_user_model
from django import forms


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        strip=False,
        required=True,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Repeat password',
        strip=False,
        required=True,
    )
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('The passwords are not the same')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password',
            'password_confirm',
            'first_name',
            'email',
        ]
