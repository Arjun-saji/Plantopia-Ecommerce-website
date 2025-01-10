from .models import *
from django import forms


class Applycouponform(forms.Form):
	code=forms.CharField(max_length=20)