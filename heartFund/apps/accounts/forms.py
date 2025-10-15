from django import forms
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    conf_pass = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]

    def clean_conf_pass(self):
        password = self.cleaned_data.get("password")
        conf_pass = self.cleaned_data.get("conf_pass")
        if password and conf_pass and password != conf_pass:
            raise forms.ValidationError("Passwords do not match")
        return conf_pass
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user