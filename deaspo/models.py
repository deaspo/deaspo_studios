from __future__ import print_function
from __future__ import unicode_literals
from django.core.validators import *
from datetime import datetime
from django.core.validators import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
import StringIO
from django.contrib.auth.models import User
from django.dispatch import receiver
from decimal import Decimal
from django.db.models.signals import post_save

from django.db import models

# Create your models here.
def path_profile_image(instance, filename):
    subfolder = 'users'
    subsubfolder = filename
    return '/'.join(filter(None, ('profile_images',subfolder,subsubfolder, filename)))

class Contact(models.Model):
    cl_email = models.EmailField()
    cl_name = models.CharField(max_length=100)
    cl_message = models.TextField(max_length=3000)

    def __str__(self):
        return self.cl_email

class Plan(models.Model):
    pn_name = models.CharField(max_length=50,unique=True)
    pn_yearly = models.DecimalField(decimal_places=2,max_digits = 5,default=5)
    pn_ssd =models.IntegerField(default=20, name='SSD')
    pn_transfer = models.IntegerField(default=1, name='Transers')
    pn_ram = models.IntegerField(default=512,name='Ram')
    pn_cpu = models.IntegerField(default=1, name='CPU')

    def __str__(self):
        return 'Plan: %s' % self.pn_name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    groups = (
        ('A', 'Self-personal'),
        ('B', 'Company'),
        ('C', 'Contractor'),
        ('D', 'Others'),
    )

    category = models.CharField(choices=groups, default='Company',max_length=50)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to=path_profile_image,default='profile.png')

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


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
    ppics = models.ImageField(upload_to=path_file_name, default='products/default.jpg')
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

class UserNext(models.Model):
   user = models.OneToOneField(User)
   next = models.CharField(max_length=100, null=True, blank=True, default=None)
   create_date = models.DateTimeField(default=datetime.now())


class Comment(models.Model):
    post = models.ForeignKey(Product, related_name='comments')
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(default=0,validators=[MinValueValidator(limit_value=0,message="Cannot be less than 0"),MaxValueValidator(limit_value=5,message="Max value allowed is 5")])
    pic = models.ImageField(upload_to='comments_images',default='profile.png')
    body = models.TextField(max_length=3000)
    posted = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.approved = True
        super(Comment,self).save(*args,**kwargs)

    def __str__(self):
        return self.user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=3000,blank=True)
    picture = models.ImageField(upload_to='profile_images',default='profile.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save(
    )



class Social(models.Model):
    platform = (
        ('A', 'Facebook'),
        ('B', 'Twitter'),
        ('C', 'Instagram'),
        ('D', 'Google Plus'),
    )
    category = models.CharField(choices=platform, default="Facebook", max_length=50)
    link = models.URLField(name='Link to profile',blank=True)
    s_class = models.CharField(max_length=100, default="wow fadeInDown")

    def save(self, *args, **kwargs):
        if self.category == 'A':
            self.s_class = 'wow fadeInUp fa fa-facebook'
        elif self.category == 'B':
            self.s_class = 'wow fadeInDown fa fa-twitter'
        elif self.category == 'C':
            self.s_class = 'wow fadeIn fa fa-instagram'
        elif self.category == 'D':
            self.s_class = 'wow fadeInUp fa fa-google-plus-square'
        else:
            self.s_class = 'wow fadeInDown'

        super(Social, self).save(*args, **kwargs)

    def __str__(self):
        return '%s link' % self.category


class Staff(models.Model):
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='staff/images', default='profile.png')
    about = models.TextField(max_length=1000)
    group = (
        ('A', 'Developer'),
        ('B', 'Product Manager'),
        ('C', 'Director, Sales Operations'),
        ('D', 'Senior Developer'),
        ('B', 'Account Manager'),
        ('E', 'Visual Designer'),
        ('F', 'Manager, Product Design'),
        ('G', 'Company Lawyer'),
        ('H', 'Director, Sales Operations'),
        ('I', 'Manager, Marketing'),
        ('J', 'Business Analyst'),
        ('K', 'Community Director'),
        ('L', 'Chief Executive Officer'),
        ('M', 'Director, Customer Support'),
        ('N', 'Data Center Manager'),
    )
    position = models.CharField(choices=group, default="Developer", max_length=50)
    social = models.ForeignKey(Social, blank=True)
    joined = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pic:
            img = Img.open(StringIO.StringIO(self.pic.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            (width, height) = (self.pic.width, self.pic.height)
            (width, height) = scale_dimensions(width,height,longest_side=500)
            img.thumbnail((width, height), Img.ANTIALIAS)
            output = StringIO.StringIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            self.pic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.pic.name.split('.')[0],
                                            'image/jpeg', output.len, None)
        super(Staff, self).save(*args,**kwargs)



    def __str__(self):
        return '%s /n Position: %s' % (self.name, self.position)


def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side * 1. / width
            return (int(width * ratio), int(height * ratio))
        elif height > longest_side:
            ratio = longest_side * 1. / height
            return (int(width * ratio), int(height * ratio))
    return (width, height)