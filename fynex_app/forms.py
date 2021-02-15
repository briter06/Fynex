from django import forms
from captcha.fields import CaptchaField

class CaptchaTestModelForm(forms.Form):
    captcha = CaptchaField()