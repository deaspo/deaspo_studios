from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from deaspo.models import Product, Project, ProductWebOrder, EmailPlan, Plan, UserNext, Staff
from deaspo.forms import WebOrderForm, UserForm, CommentForm, ContactForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView
from django.utils.http import is_safe_url
from registration.models import RegistrationProfile

from django.contrib import messages

# Create your views here.

class RegisterView(RegistrationView):
    def get_success_url(self, user):
        try:
            return '/services/'
        except Exception, e:
            print str(e)
            pass

#def index(request):
 #   if request.POST:
 #       cform = ContactForm(request.POST)
 #       if cform.is_valid():
 #           cform.save()
 #           return HttpResponseRedirect('/')
 #   else:
 #       cform = ContactForm()
 #   products = Product.objects.all() #returns all the products and services
 #   #pintro = Product.objects.filter(Q(category__exact='Web')| Q(category__exact='Mobile'))
 #   pintro = Product.objects.filter(pmain=True)[:2][::1]
 #   pcont = Product.objects.filter(pmain=False)[:3][::1]
 #   return render(request, "home/index.html", {'services':products, 'servTwo':pintro, 'servThree':pcont,'cform':cform})


def services(request):
    if request.POST:
        cform = ContactForm(request.POST)
        if cform.is_valid():
            cform.save()
            return HttpResponseRedirect('/services')
    else:
        cform = ContactForm()
    products = Product.objects.all()  # returns all the products and services
    return render(request, "services/index.html", {'services':products,'cform':cform})

def service(request, service_id):
    service = get_object_or_404(Product, pk=service_id)
    if request.POST:
        if request.POST['form-type'] == u"review-form":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = service
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Review posted!. We value your feedback!",
                                     fail_silently=True)
                next = '/services/%d' % int(service_id)
                HttpResponseRedirect(next)
            else:
                print form.errors
        else:
            cform = ContactForm(request.POST)
            if cform.is_valid():
                cform.save()
                next = '/services/%d' % int(service_id)
                HttpResponseRedirect(next)
    else:
        form = CommentForm()
        cform = ContactForm()
    products = Product.objects.all()  # returns all the products and services
    half_preducts = (len(products) + 1) / 2
    # half_preducts = (products.count()+1)/2
    projects = Project.objects.all()  # return all the projects
    return render(request, 'services/service.html', {'form':form,'cform':cform,'service': service,'services':products, 'projects':projects,'half':half_preducts})

@login_required
def order(request, service_id, plan_id):
    products = Product.objects.all()  # returns all the products and services
    projects = Project.objects.all()  # return all the projects
    eplans = EmailPlan.objects.all()
    service =  get_object_or_404(Product, pk=service_id)
    splan = get_object_or_404(Plan, pk=plan_id)
    activate = False
    if not request.POST:
        form = WebOrderForm()
        form.total_price = splan.pn_yearly

    else:
        form = WebOrderForm(request.POST)
        form.hosting_plan = splan.pn_name
    return render(request,'services/order.html',{'activate':activate,'eplans':eplans,'service':service,'splan':splan,'form':form,'services':products,'projects':projects,'email':request.user.email,'fullname':request.user.get_full_name(),'username':request.user.username,'picture':request.user.profile.picture})


def selfCheck(request, service_id, plan_id):
    context = RequestContext(request)
    prodId = request.session.get('prodId')
    planId = request.session.get('planId')
    if not prodId:
        prodId = service_id
    else:
        if request.session.get('prodId') != service_id:
            prodId = service_id
    request.session['prodId'] = prodId

    if not planId:
        planId = plan_id
    else:
        if request.session.get('planId') != plan_id:
            planId = plan_id
    request.session['planId'] = planId

    if request.user.is_authenticated:
        return HttpResponseRedirect('/service/%d/%d/order' % (int(prodId), int(planId)))
    else:
        return render(request, 'users/signup.html', context)



    #del request.session['prodId']
    #del request.session['planId']#  to review
    #session_keys = list(request.session.keys())
    #for key in session_keys:
     #   del request.session[key]


    #sets next page depending on status of login or logout

    #return render_to_response('users/signup.html',{},context)



def signin(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    prodId = request.session.get('prodId')
    planId = request.session.get('planId')
    if  planId and prodId:
        next = request.GET.get('next', '/service/%d/%d/order' % (int(prodId), int(planId)))
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)

                return HttpResponseRedirect(next)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:

        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('users/signup.html', {}, context)


@login_required
def sign_out(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/services')

@login_required
def profile(request):
    context = RequestContext(request)
    next = request.GET.get('next')
    activate = True
    return render_to_response('users/profile.html',{'next':next,'user':request.user,'activate':activate,'email':request.user.email,'fullname':request.user.get_full_name(),'username':request.user.username,'lastname':request.user.last_name,'firstname':request.user.first_name,'about':request.user.profile.about,'picture':request.user.profile.picture},context)

@login_required
def backToCart(request):

    activate = False
    return redirect(next)

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.POST:
        next = request.GET.get('next')
        user.profile.about = request.POST['about']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return HttpResponseRedirect(next)

#@staff_member_required
@login_required
def del_user(request, user_id):
    try:
        u = User.objects.get(pk=user_id)
        u.delete()
        products = Product.objects.all()  # returns all the products and services
        return render(request, "services/index.html", {'services': products})
    except Exception as e:
        return render(request, 'users/profile.html',{'err':e.message})

def projects(request):
    projects = Project.objects.all()
    return render(request,'projects/projects.html',{'projects':projects})


def project(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)
    return render(request,'projects/project.html',{'project':project})

def about(request):
    staffs = Staff.objects.all()
    products = Product.objects.all()
    projects = Project.objects.all()
    return render(request,'about/about.html',{'staffs':staffs,'services':products,'projects':projects})


def index(request):
    if request.POST:
        cform = ContactForm(request.POST)
        if cform.is_valid():
            cform.save()
            return HttpResponseRedirect('/')
    else:
        cform = ContactForm()
    products = Product.objects.all() #returns all the products and services
    half_preducts = (len(products)+1)/2
    #half_preducts = (products.count()+1)/2
    projects = Project.objects.all()#return all the projects
    return render(request, "base.html", {'services':products, 'projects':projects, 'cform':cform, 'half':half_preducts})
