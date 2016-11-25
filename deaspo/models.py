from __future__ import print_function
from __future__ import unicode_literals
from django.core.validators import *
from datetime import datetime
from django.core.validators import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
import StringIO
from decimal import Decimal

from django.db import models

# Create your models here.

class Plan(models.Model):
    pn_name = models.CharField(max_length=50,unique=True)
    pn_yearly = models.DecimalField(decimal_places=2,max_digits = 5,default=5)
    pn_ssd =models.IntegerField(default=20, name='SSD')
    pn_transfer = models.IntegerField(default=1, name='Transers')
    pn_ram = models.IntegerField(default=512,name='Ram')
    pn_cpu = models.IntegerField(default=1, name='CPU')

    def __str__(self):
        return 'Plan: %s' % self.pn_name

class EmailPlan(models.Model):
    pn_ename = models.CharField(max_length=50,unique=True)
    pn_eprice = models.DecimalField(decimal_places=2,max_digits=3,default=5)

    def __str__(self):
        return 'Plan: %s' % self.pn_ename

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return 'Project: %s' % self.name


def path_file_name(instance, filename):
    if instance.category == 'A':
        subfolder = 'web'
    elif instance.category == 'B':
        subfolder = 'desktop'
    elif instance.category == 'C':
        subfolder = 'mobile'
    else:
        subfolder = 'others'

    return '/'.join(filter(None, ('products',subfolder, filename)))


class Product(models.Model):
    pname= models.CharField(max_length=100, unique=True, default='Product')
    ppics = models.ImageField(upload_to=path_file_name, default='D:/Users\polyc/PycharmProjects/deaspo_inc/deaspo/media/products/default.jpg')
    pintro = models.CharField(max_length=50, default='Brief intro')
    pshortdesc = models.CharField(max_length=500, default='Short description')
    pdesc = models.TextField(max_length=3000, default='Product description')
    prel = models.ManyToManyField("self", blank=True)
    pproj = models.ManyToManyField(Project)
    plan = models.ManyToManyField(Plan)
    type = (
        ('A', 'Web'),
        ('B', 'Desktop'),
        ('C', 'Mobile'),
        ('D', 'Others'),
    )
    category = models.CharField(choices=type,default="Web", max_length=50)

    pmain = models.BooleanField(default=False)

    # compressing and resizing the image before saving
    def save(self, *args, **kwargs):
        if self.ppics:
            img = Img.open(StringIO.StringIO(self.ppics.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((767 * self.ppics.width / 1.5, 388 * self.ppics.height / 1.5), Img.ANTIALIAS)
            output = StringIO.StringIO()
            img.save(output, format='JPEG', quality=80)
            output.seek(0)

            self.ppics = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.ppics.name.split('.')[0],
                                              'image/jpeg', output.len, None)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return 'Product: %s' % self.pname


class ProductWebOrder(models.Model):
    sites = models.IntegerField(default=1, validators=[MinValueValidator(limit_value=1, message='Cannot be less than 1!')])
    hosting_plan = models.CharField(max_length=50)
    backup = models.BooleanField(default=False)
    wed_design = models.BooleanField(default=True)
    web_design_name = models.CharField(max_length=50, blank=True)
    domain = models.BooleanField(default=True)
    domain_name = models.CharField(max_length=50)
    custom_email = models.BooleanField(default=False)
    custom_email_name = models.CharField(max_length=50, blank=True)
    custom_email_price = models.DecimalField(decimal_places=2, validators=[MinValueValidator(limit_value=0, message='Negatives not allowed')], blank=True, max_digits=7)
    dedicated_inbox = models.BooleanField(default=False)
    dedicated_inbox_plan = models.CharField(max_length=50, blank=True)
    total_price = models.DecimalField(decimal_places=2, validators=[MinValueValidator(limit_value=0, message='Negatives not allowed')],max_digits=7)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(validators=[EmailValidator()])
    contact_no = models.IntegerField()
    contact_address = models.TextField(max_length=1000)
    notes = models.TextField(max_length=1000)
    acceptance_terms = models.BooleanField(default=True)
    posted_date = models.DateTimeField(default=datetime.now(), editable=False)

