from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users, admin_only
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
# Create your views here.
@unauthenticated_user 
def registerPage(request):

    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
           user = form.save()
           username = form.cleaned_data.get('username')

           group = Group.objects.get(name='customer')
           user.groups.add(group)


           messages.success(request, "Account created successfully for username: "+ username )
           return redirect('login')
    context ={'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
      
    if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is not correct')
    context ={}
    return render(request, 'accounts/login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
 
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    total_order = orders.count()
    context = {'orders': orders, 'customers':customers, 'delivered':delivered, 'pending':pending, 'total_order':total_order}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders =myFilter.qs
    context = {'customer':customer, 'orders':orders, 'total_order':total_order, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)