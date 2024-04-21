from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from typing import Union, Any

class BookmarksView(generic.ListView):
    template_name = "bookmarks.html"
    context_object_name = "titles"

    def get_queryset(self) -> Any:
        return self.request.user.bookmarks.all()
     
    def get(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse]:
        if not self.request.user.is_authenticated:
            return redirect('/manga')
        
        return super().get(request, *args, **kwargs)
