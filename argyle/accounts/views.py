from accounts.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime, random, sha

from google.appengine.api import mail

from accounts.forms import LoginForm, RegistrationForm

def test(request):
    test = None
    if request.method == 'POST':
        recipient = request.POST['recipient'] + " <" + request.POST['recipient'] + ">"
        message = mail.EmailMessage()
        message.sender = "Argyle <cs198.juatsemilla@gmail.com>"
        message.to = recipient
        message.subject = request.POST['subject']
        message.body = request.POST['body']
        message.send()
    else:
        test = None
    
    return render_to_response('test.html', 
                {'test':test}, context_instance=RequestContext(request))

def register(request):
    code = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        form = RegistrationForm(request.POST)
        if form.is_valid():
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_code = sha.new(salt+username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(7)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.activation_code = activation_code
            profile.key_expires = key_expires
            profile.save()
            return render_to_response('accounts/register.html', 
                {'code':activation_code, 'profile':profile}, context_instance=RequestContext(request))
        else:
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_code = sha.new(salt+username).hexdigest()
            return render_to_response('accounts/register.html',
                {'form':form, 'code':activation_code}, context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
        return render_to_response('accounts/register.html',{'form':form, 'code':code})
        
@login_required
def profile(request):
    
    return render_to_response('accounts/profile.html')
    
def login_view(request):
    data = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = user.get_profile()
                return render_to_response('accounts/profile.html',{'profile':profile},
                    context_instance=RequestContext(request))
            else:
                data = "User is inactive."
                return render_to_response('accounts/activate.html',{'data':True, 'user':user},
                    context_instance=RequestContext(request))
        form = LoginForm()
        return render_to_response('accounts/login.html',{'form':form, 'errors':True},
            context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response('accounts/login.html',{'form':form, 'data':data},
            context_instance=RequestContext(request))
            
def logout_view(request):
    logout(request)
    return render_to_response('accounts/logout.html',{'data':True},
            context_instance=RequestContext(request))
            
def activate(request,code=None):
    username = None
    password = None
    user = None
    if request.method == 'POST':
        if code is None:
            username = request.POST['username']
            password = request.POST['password']
            code = request.POST['activation_code']
            user = User.objects.get(username=username, password=password)
            profile = user.get_profile()
        else:
            profile = UserProfile.objects.get(activation_code=code)
            user = profile.user
    else:
        profile = UserProfile.objects.get(activation_code=code)
        user = profile.user
        
    if user is not None:
        if profile.activation_code == code:
            user.is_active = True
            user.save()
            profile.key_expires = None
            profile.save()
            return render_to_response('accounts/success.html',{'data':True},
                    context_instance=RequestContext(request))
        else:
            return render_to_response('accounts/unsuccessful.html',{'data':True},
                    context_instance=RequestContext(request))
    return render_to_response('accounts/logout.html',{'data':True},
            context_instance=RequestContext(request))

def resend_activate(request, username=None):
    user = User.objects.get(username=username)
    profile = user.get_profile()
    #print profile.activation_code
    message = mail.EmailMessage()
    message.sender = "Argyle <cs198.juatsemilla@gmail.com>"
    message.to = user.email
    message.subject = "Activate your Argyle account"
    message.body = """This is your activation code: """ + str(profile.activation_code) + """
    You could also visit http://127.0.0.1:8000/accounts/activate/""" + str(profile.activation_code) + """ to activate your account."""
    
    message.send()
    return render_to_response('accounts/activate.html',{'user':user},
            context_instance=RequestContext(request))
