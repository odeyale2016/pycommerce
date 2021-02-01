from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Order, Customer

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
class CustomerForm(ModelForm):
    class meta:
        model = Customer
        fields = '__all__'
class CreateUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username','email','password1','password2']