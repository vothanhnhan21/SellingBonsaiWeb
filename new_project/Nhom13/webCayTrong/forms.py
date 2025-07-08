import re
from django import forms
from django.contrib.auth.models import User
import phonenumbers
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm

class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput({'placeholder': 'Enter your email',}), label="Email",  help_text="Ví dụ: example@domain.com.",required=True)
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Enter your password'}),help_text="Ví dụ: MyPassword123!" ,label="Password",required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Confirm your password'}), label="Confirm Password", required=True)
    phone_number = forms.CharField(
        max_length=15, 
        label="Phone Number", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )

    # Địa chỉ
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}),
        label="Address",
        help_text= "Ví dụ: 123 Đường ABC, Quận 1, TP.HCM, 700000.",
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Kiểm tra mật khẩu và xác nhận mật khẩu có khớp nhau không
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Kiểm tra mật khẩu có ít nhất một chữ hoa
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một chữ hoa.")

        # Kiểm tra mật khẩu có ít nhất một chữ thường
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một chữ thường.")

        # Kiểm tra mật khẩu có ít nhất một số
        if not re.search(r'\d', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một số.")

        # Kiểm tra mật khẩu có ít nhất một ký tự đặc biệt
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một ký tự đặc biệt (@, $, !, %, *, ?, &).")
        
        return password  # Trả về mật khẩu nếu hợp lệ
    def clean_phone_number(self):

        phone_number = self.cleaned_data.get('phone_number')

        try:
            # Phân tích số điện thoại với mã quốc gia là 'VN' (Việt Nam)
            parsed_number = phonenumbers.parse(phone_number, 'VN')

            # Kiểm tra tính hợp lệ của số điện thoại
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Số điện thoại không hợp lệ.")

            # Kiểm tra xem số điện thoại có phải là số di động không
            if not phonenumbers.is_valid_number_for_region(parsed_number, 'VN'):
                raise ValidationError("Số điện thoại không hợp lệ đối với khu vực.")
            
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Số điện thoại không hợp lệ.")
        
        return phone_number


class rePasswordForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput({'placeholder': 'Enter your email',}),  help_text="Ví dụ: example@domain.com.",required=True)
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Enter your new password'}),help_text="Ví dụ: MyPassword123!" ,required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Confirm your new password'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Kiểm tra mật khẩu và xác nhận mật khẩu có khớp nhau không
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Kiểm tra mật khẩu có ít nhất một chữ hoa
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một chữ hoa.")

        # Kiểm tra mật khẩu có ít nhất một chữ thường
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một chữ thường.")

        # Kiểm tra mật khẩu có ít nhất một số
        if not re.search(r'\d', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một số.")

        # Kiểm tra mật khẩu có ít nhất một ký tự đặc biệt
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất một ký tự đặc biệt (@, $, !, %, *, ?, &).")
        
        return password  # Trả về mật khẩu nếu hợp lệ




class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'input_medium',
        'placeholder': 'Enter your email address',
        'type': 'email',
        'name': 'email'
        }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=(""),
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Enter your new password',
                                        'type': 'password',
                                        }))
    new_password2 = forms.CharField(label=(""),
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm your new password',
                                        'type': 'password',
                                        }))
    