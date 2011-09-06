from accounts.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
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
            user.is_active = True
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

def profile(request):
    send_mail('Subject here', 'Here is the message.', 'cs198.juatsemilla@gmail.com', ['semillastan@gmail.com'], fail_silently=False)
    return render_to_response('accounts/profile.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    else:
        form = LoginForm()
        return render_to_response('accounts/login.html',{'form':form})
