import requests
from django.core.mail import EmailMessage

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, TemplateView, UpdateView
from rest_framework import generics
from django.contrib.auth import update_session_auth_hash

from registration import forms
from .forms import CustomUserCreationForm,UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from  django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import editprofile
from .models import User
import nexmo


# Rest Api's

from .serializer import UserSerializer

# Create your views here.

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

def Indexview(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            user=f.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            mail_subject="Activate your account"
            message1=render_to_string('registration/acc_active_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = f.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message1, to=[to_email]
            )
            email.send()

            return HttpResponse('Please verify your email')

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/welcome.html', {'form': f})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user1 = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user1 = None
    if user1 is not None and account_activation_token.check_token(user1, token):
        user1.is_active = True
        user1.save()
        login(request, user1,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return redirect('verify')
    else:
        return HttpResponse('Activation link is invalid!')


class loginform(View):

    template_name="registration/login.html"
    form_class=UserForm

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})


    def post(self,request):
        form=self.form_class(request.POST)

        if (form.is_valid()):
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                user1 = User.objects.get(id=request.user.id)
                return render(request, 'registration/home.html', {'user': user1})
            else:
                return HttpResponse("User login failed")
        else:
            return HttpResponse("Form is invalid")


class phoneverify(View):

    template_name="registration/phone_verification.html"

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        pnumber=request.POST['phonenumber']
        response = self.send_verification_request(request, pnumber)

        if (response['status'] == '0'):
            request.session['verification_id'] = response['request_id']
            return HttpResponseRedirect(reverse('phoneverification')+"?next="+request.POST['next'])
        else:
            return HttpResponse('Invalid Number')

    def send_verification_request(self, request, pnumber):
        client = nexmo.Client(key='47adadf8', secret='Glb8ibBghFair7Lj')
        return client.start_verification(number=pnumber, brand='Test')



class phoneverification(TemplateView):
    template_name='registration/verify.html'



class ConfirmView(View):
    def post(self, request):
        response = self.check_verification_request(request)

        if (response['status'] == '0'):
            request.session['verified'] = True
            return redirect('login')
        else:
            return HttpResponse("Sorry pin failed")

    def check_verification_request(self, request):
        return nexmo.Client(key='47adadf8', secret='Glb8ibBghFair7Lj').check_verification(request.session['verification_id'], code=request.POST['code'])




class home(LoginRequiredMixin,View):

    template_name="registration/home.html"

    def get(self,request,user_id):
        user1 = User.objects.get(id=user_id)
        return render(request,self.template_name,{'user',user1})

#Upload pic submit this will open in our update view
'''class second(LoginRequiredMixin,View):

    template_name='registration/secondpage.html'
    form_class=editprofile

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST,request.FILES)

        if (form.is_valid()):
          profile=form.save(commit=False)
          user_save=User.objects.get(id=request.user.id)
          profile.user=user_save
          profile.save()

          return redirect('home')
        else:
            return render(request,self.template_name,{'form':form})'''


class seeprofile(View):

   template_name='registration/viewprofile_2.html'

   def get(self, request):
       user1 = User.objects.get(id=request.user.id)
       return render(request, self.template_name, {'user': user1})

#log-in user id
class editView(UpdateView):
    model = User
    form_class=editprofile
    template_name = 'registration/secondpage.html'


    def get_form_kwargs(self):
        kwargs = super(editView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs







class Createuser(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class Updateuser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Deleteuser(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer









