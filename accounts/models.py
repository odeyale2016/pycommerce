from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (('Indoor', 'Indoor'),
              ('Outdoor', 'Outdoor'))
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=300, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str_(self):
        return self.name


class Order(models.Model):
    STATUS = (('Pending', 'Pending'),
              ('Out for delivery', 'Out for delivery'),
              ('Delivered', 'Delivered') )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now=True, null=True)

    def __str_(self):
        return self.product.name