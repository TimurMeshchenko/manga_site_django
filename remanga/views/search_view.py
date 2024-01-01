from django.views import generic
from typing import Any
import json

from remanga.models import Title

class SearchView(generic.ListView):
    template_name = "search.html"

    def get_queryset(self) -> None:
        return
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["json_data"] = json.dumps(list(Title.objects.values())).replace('\'', '\\\'')
        return context
 