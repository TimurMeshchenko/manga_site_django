from django.views import generic
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.tokens import default_token_generator

from remanga.models import User
from remanga.forms import CustomPasswordResetForm

class ResetPasswordView(generic.ListView):
    template_name = "reset_password.html"

    def get_queryset(self) -> None:
        return
    
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        user_id = kwargs['uidb64']
        user = User.objects.get(id=user_id)
        is_valid_token = default_token_generator.check_token(user, kwargs['token'])

        if not is_valid_token:
            return HttpResponse('Invalid token')
        
        context = { 'form': CustomPasswordResetForm() }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs) -> JsonResponse:
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():            
            user_id = kwargs['uidb64']
            user = User.objects.get(id=user_id)            
            password = form.cleaned_data.get('password1')

            user.set_password(password)
            user.save()
            
            user = authenticate(username=user.username, password=password)
            login(request, user)     
            
            return JsonResponse({'message': 'Password changed'})
            
        return JsonResponse({'detail': form.errors})
