from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from typing import Union, Any

from remanga.tasks import send_async_email
from remanga.models import User

class SigninView(generic.ListView):
    template_name = "signin.html"
    
    def get(self, request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse]:
        if self.request.user.is_authenticated:
            return redirect('/manga')
        
        context = { 'form': AuthenticationForm() }
        return render(request, self.template_name, context)

    def post(self, request: Any) -> JsonResponse:
        is_email = 'email' in request.POST

        if is_email: 
            return self.get_send_email_response(request)

        return self.get_signin_response(request)

    def get_send_email_response(self, request: Any) -> JsonResponse:
        email = request.POST['email']
        is_email_exists = User.objects.filter(email=email).exists()
        
        if not is_email_exists:
            return JsonResponse({'detail': 'User with this email does not exist'})

        self.send_email(email)

        return JsonResponse({'message': 'Sent to email'})

    def send_email(self, to_mail: str) -> None:
        subject = "Manga password recovery"
        recipient_list = [to_mail]
        template_name = 'reset_password_letter.html'
        
        user = User.objects.get(email=to_mail)
        token = default_token_generator.make_token(user)

        context = {'user': user, 'token': token, 'domain': "http://localhost:8000"}
        message = render_to_string(template_name, context)

        if settings.USE_REDIS:
            send_async_email.delay(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        else:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=message)

    def get_signin_response(self, request: Any) -> JsonResponse:
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'authenticated success'})

        return JsonResponse({'detail': form.errors})    
