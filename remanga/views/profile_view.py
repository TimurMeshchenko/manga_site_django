from django.views import generic
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.http import JsonResponse
from typing import Any
import os

from remanga.models import User

class ProfileView(generic.ListView):
    template_name = "profile.html"
    
    def get_queryset(self) -> None:
        return

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')  
        profile = User.objects.filter(id=user_id)[0]

        context['profile'] = profile
        context['form'] = PasswordChangeForm(self.request.user)

        return context 

    def post(self, request: Any, **kwargs) -> JsonResponse:
        if ('old_password' in request.POST):
            return self.change_password(request)
        
        return self.change_avatar(request)
    
    def change_password(self, request: Any) -> JsonResponse:
        form = PasswordChangeForm(request.user, request.POST)
            
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)                    
            return JsonResponse({'message': 'Password changed'})
        
        return JsonResponse({'detail': form.errors})

    def change_avatar(self, request: Any) -> JsonResponse:
        avatar = request.FILES['avatar']
        if not avatar.content_type.startswith('image'):
            raise ValueError('Only image files are allowed')
        avatar.name = f"{self.request.user.id}.jpg"
        response_data = {}       
        avatar_path = os.path.join(settings.MEDIA_ROOT, "users_avatars", avatar.name)

        if (os.path.exists(avatar_path)):
            os.remove(rf'{avatar_path}')

        self.request.user.avatar = avatar
        self.request.user.save()

        return JsonResponse(response_data)
 