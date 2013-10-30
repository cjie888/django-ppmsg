# -*- coding: utf-8 -*-
""" user related forms """

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User as DjangoUser

from config import EMAIL_SUFFIX, PASSWORD_MIN_LENGTH, USER_ICON_SUFFIXS
from toollib.verificationcode import VerificationCodeField, VerificationCodeTextInput


class RegisterForm(UserCreationForm):
    class Meta:
        fields = ("username", "email",)
        model = DjangoUser

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["verificationcode"] = VerificationCodeField(label=u"验证码", widget=VerificationCodeTextInput({"class": "test"}),
                                                                help_text=u"请输入图片中的字母,不区分大小写。")

    def clean_email(self):
        email = self.cleaned_data["email"]

        if DjangoUser.objects.filter(email=email).count():
            raise forms.ValidationError(u"该邮箱已经被注册!")

        if EMAIL_SUFFIX and not email.endswith(EMAIL_SUFFIX):
            raise forms.ValidationError(u"邮箱域名必须是%s!" % EMAIL_SUFFIX)

        return email

    def clean_password1(self):
        return do_check_password_length(self, 'password1')


class LoginForm(AuthenticationForm):
    pass


class ChangePasswordForm(PasswordChangeForm):
    def clean_new_password1(self):
        return do_check_password_length(self, 'new_password1')


class PrepareResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label=u'注册邮箱')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if DjangoUser.objects.filter(email=email).count() < 1:
            raise forms.ValidationError(u"该邮箱未注册!")
        return email


class ResetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        return do_check_password_length(self, 'new_password1')


class ChangeUserIconForm(forms.Form):
    upload_file = forms.ImageField(label=u"", help_text=u"目前仅支持 <em>%s</em> 等格式文件!" % str(USER_ICON_SUFFIXS)[1:-1])

    def clean_upload_file(self):
        upload_file = self.cleaned_data["upload_file"]
        suffix = upload_file.name.split(".")[-1]
        if USER_ICON_SUFFIXS and suffix not in USER_ICON_SUFFIXS:
            raise forms.ValidationError(u"")
        return upload_file


def do_check_password_length(form, password_key):
    password = form.cleaned_data.get(password_key)
    if len(str(password).strip()) < PASSWORD_MIN_LENGTH:
        raise forms.ValidationError(u"至少 %s 位密码!" % PASSWORD_MIN_LENGTH)
    return password
