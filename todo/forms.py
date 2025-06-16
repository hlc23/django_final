from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='確認密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw_confirm = cleaned_data.get('password_confirm')
        if pw != pw_confirm:
            raise forms.ValidationError("兩次輸入的密碼不一致！")
        return cleaned_data
