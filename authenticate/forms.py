from django import forms
from .models import User
from spare.models import Supplier
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password
from django.contrib.admin.widgets import FilteredSelectMultiple

class EditMyProfile(forms.ModelForm):
    _role = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True}),
    )
    _register_date = forms.DateField(
        widget=forms.DateInput(attrs={'readonly': True}),
    )

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'role', 'register_date', 'is_admin']
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        sex = cleaned_data.get('sex')
        if (not username) or (not first_name) or (not last_name) or (not sex):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data



class ChangePassword(forms.Form):
    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('password', None)
        super(ChangePassword, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )
    password_regex = RegexValidator(
        regex=r'^\S{4,1024}',
        message='password must be at least 4 character'
    )
    new_password = forms.CharField(
        label='New password:',
        validators=[password_regex],
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='minimum 4 character'
    )
    confirm = forms.CharField(
        label='New password confirmation:',
        max_length=1024,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm')
        if (not old_password) or (not new_password) or (not confirm_password):
            raise forms.ValidationError("Please correct the errors below.")
        # print(check_password(old_password, self.password))

        if check_password(old_password, self.password):
            if new_password:
                if new_password == confirm_password:
                    return
                else:
                    raise forms.ValidationError("password is not confirmed")
        else:
            raise forms.ValidationError("Your old password was entered incorrectly. Please enter it again.")

        return cleaned_data



class SupplierRegister(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'  


class EditSupplier(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__' 


class SellerRegister(forms.ModelForm):
    password_regex = RegexValidator(
        regex=r'^\S{4,1024}',
        message='password must be at least 4 character'
    )
    user_password = forms.CharField(
        validators=[password_regex],
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='*Enter password minimum 4 character',
        label='Password'
    )
    confirm_password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='*Confirm password'
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'sex', 'phone', 'email', 'user_password', 'confirm_password', 'photo']
        # exclude = ['last_login', 'password', 'register_date', 'role', 'is_admin']
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        sex = cleaned_data.get('sex')
        user_password = cleaned_data.get('user_password')
        confirm = cleaned_data.get('confirm_password')
        if (not username) or (not first_name) or (not last_name) or (not sex) or (not user_password) or (not confirm):
            raise forms.ValidationError("Please correct the errors below.")

        if user_password != confirm:
            raise forms.ValidationError("password is not confirmed")
        
        return cleaned_data



class EditSeller(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'register_date', 'role','is_admin']
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        sex = cleaned_data.get('sex')
        if (not username) or (not first_name) or (not last_name) or (not sex):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data

