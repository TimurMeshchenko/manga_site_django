from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from typing import Union, Any

from remanga.forms import UserCreationForm

class SignupView(generic.View):
    template_name = 'signup.html'
 
    def get(self, request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse]: 
        if self.request.user.is_authenticated:
            return redirect('/manga/')
        
        context = { 'form': UserCreationForm() }
        return render(request, self.template_name, context)

    def post(self, request: Any) -> None:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({'message': 'registered success'})
        
        return JsonResponse({'detail': form.errors})
