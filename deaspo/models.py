from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime
from django.core.validators import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
import StringIO
from decimal import Decimal

from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return 'Project: %s' % self.name


class Product(models.Model):
    pname= models.CharField(max_length=100, unique=True, default='Product')
    ppics = models.ImageField(upload_to='products/images', default='D:/Users\polyc/PycharmProjects/deaspo_inc/deaspo/media/products/default.jpg')
    pintro = models.CharField(max_length=50, default='Brief intro')
    pshortdesc = models.CharField(max_length=500, default='Short description')
    pdesc = models.TextField(max_length=3000, default='Product description')
    prel = models.ManyToManyField("self", blank=True)
    pproj = models.ManyToManyField(Project)
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