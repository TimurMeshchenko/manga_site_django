from django.views import generic
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib.auth import logout
from typing import Union

class LogutView(generic.ListView):
    def get(self, request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
        logout(request)
        return redirect('/manga')