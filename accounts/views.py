from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm, CustomerForm
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    total_order = orders.count()
    context = {'orders': orders, 'customers':customers, 'delivered':delivered, 'pending':pending, 'total_order':total_order}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {'customer':customer, 'orders':orders, 'total_order':total_order}
    return render(request, 'accounts/customers.html', context)

def orders(request):
    return render(request, 'accounts/orders.html')

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) 
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method=='POST':
        formset=OrderForm(request.POST, instance = customer)
        if formset.is_valid:
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form =OrderForm(instance=order)
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)

def createCustomer(request):
    form = CustomerForm()
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)