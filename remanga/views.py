from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator

from typing import Union, Any, Optional
import json
import os

from .models import *
from .forms import UserCreationForm

class CatalogView(generic.ListView):
    template_name = "catalog.html"
    filters = Q()
    count_titles_on_page = 30

    def get_queryset(self) -> None:
        return
    
    def get(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse, JsonResponse]:
        self.create_filters(request)
        
        if ('next_page' in request.GET):
            return JsonResponse(self.get_next_page_data(request))
        
        return super().get(request, *args, **kwargs)
        
    def create_filters(self, request: HttpRequest) -> None:
        """
        Iterate each query param and for different query params combine with a condition "and"
        """ 
        self.init_filters_variables()
        
        for query_key in list(request.GET.keys()): 
            query_values = self.request.GET.getlist(query_key)
            query_param_exception = self.is_query_param_exception(query_key, query_values)

            if (query_param_exception): continue
            
            self.create_query_key_filters(query_key, query_values)        
            self.filters &= self.query_key_filters

    def init_filters_variables(self) -> None:
        self.query_keys_adapted_for_table = {
            'types': 'manga_type',
            'rating': 'avg_rating',
            "_gte": "",
            "_lte": "",
            "exclude_": "",
        }

        self.title_table_columns = {
            'manga_type': Title.objects.values_list("manga_type", flat=True).distinct(),
            'genres': Genres.objects.all(),
            'categories': Categories.objects.all(),
        }

        self.title_table_columns_ranges = {
            'issue_year': None,
            'avg_rating': None,
            'count_chapters': None,
        }        

    def is_query_param_exception(self, query_key: str, query_values: list[str]) -> bool:
        for query_value in query_values:
            is_query_values_empty = query_value == str()
           
            if is_query_values_empty: break

        query_key_adapted = self.get_query_key_adapted(query_key)

        query_key_exists = query_key_adapted in self.title_table_columns \
        or query_key_adapted in self.title_table_columns_ranges

        return is_query_values_empty or not query_key_exists

    def get_query_key_adapted(self, query_key: str) -> str:
        query_key_adapted = query_key

        for query_key_for_adapte in self.query_keys_adapted_for_table:
            if not query_key_for_adapte in query_key: continue

            query_key_for_adapte_value = self.query_keys_adapted_for_table[query_key_for_adapte]

            if query_key_for_adapte_value == "":
                query_key_adapted = query_key_adapted.replace(query_key_for_adapte, "")
            else:
                query_key_adapted = query_key_for_adapte_value

            break

        return query_key_adapted

    def create_query_key_filters(self, query_key: str, query_values: list[str]) -> None:
        """
        Create filters for all values in query param
        """  
        query_key_adapted = self.get_query_key_adapted(query_key)
        self.query_key_filters = Q()
        
        for query_value_str in query_values:
            valid_query_value = self.is_valid_query_value(query_value_str)

            if not valid_query_value: continue

            query_value = float(query_value_str) if '.' in query_value_str else int(query_value_str)

            if query_key_adapted in self.title_table_columns_ranges:
                self.add_range_filters(query_key, query_key_adapted, query_value)
            elif type(query_value) == int:
                self.add_filter(query_key, query_key_adapted, query_value)

    def is_valid_query_value(self, query_value_str: str) -> bool:
        have_point = False

        for char in query_value_str:
            if char == '.' and not have_point: 
                have_point = True
            elif not char.isdigit():
                return False
            
        return True

    def add_range_filters(self, query_key: str, query_key_adapted: str, query_value: Union[float, int]) -> None:        
        """
        Filters ranging from to
        """  
        if 'lte' in query_key:
            range_argument = 'lte'
        elif 'gte' in query_key:
            range_argument = 'gte'
        else: 
            return
        
        self.query_key_filters |= Q(**{f"{query_key_adapted}__{range_argument}": query_value})

    def add_filter(self, query_key: str, query_key_adapted: str, query_value: Union[float, int]) -> None:                
        """
        Other filters except ranging from to
        """          
        if query_value >= len(self.title_table_columns[query_key_adapted]):
            return

        filtered_data = self.title_table_columns[query_key_adapted][query_value]

        Q_filter = Q(**{ query_key_adapted: filtered_data })        

        if "exclude" in query_key:
            self.query_key_filters &= ~Q_filter
        else:
            self.query_key_filters |= Q_filter

    def get_next_page_data(self, request: HttpRequest) -> dict[str, str]:
        filtered_titles = Title.objects.order_by('-count_rating').filter(self.filters).distinct()
        
        paginator = Paginator(filtered_titles, self.count_titles_on_page)
        next_page = self.request.GET.get('next_page')
        titles_list = paginator.get_page(next_page)        
        
        next_page_data = {
            'html': render(request, 'titles_template.html', { 'titles_list': titles_list }).content.decode(),
        }

        return next_page_data

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        database_tables_data = {
            "types_data": Title.objects.values("manga_type").distinct(),
            "categories_data": Categories.objects.values(),
            "genres_data": Genres.objects.values(),
        }

        for database_table_data_key in database_tables_data:
            context[database_table_data_key] = \
                json.dumps(list(database_tables_data[database_table_data_key])).replace('\'', '\\\'')

        filtered_titles = Title.objects.order_by('-count_rating').filter(self.filters).distinct()
        paginator = Paginator(filtered_titles, self.count_titles_on_page)
        titles_list = paginator.get_page(1)

        context['titles_list'] = titles_list
        context['num_pages'] = paginator.num_pages

        return context   

class TitleView(generic.ListView):
    template_name = "title.html"

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        dir_name = self.kwargs.get('dir_name')  
        title = Title.objects.get(dir_name=dir_name)
       
        context['title'] = title
        context['comments'] = title.comments.all().order_by('-created_at')

        if not self.request.user.is_authenticated: return context

        title_rating = self.get_title_rating(title)

        context['is_bookmark_added'] = self.request.user.bookmarks.filter(id=title.id).exists()
        context['title_rating'] = title_rating.rating if title_rating else title_rating
        context['user_title_comments_ratings'] = self.get_user_title_comments_ratings_dict(title)
        
        return context 

    def get_title_rating(self, title: Title) -> Optional[Title_rating]:
        return Title_rating.objects.filter(user=self.request.user, title=title).first()

    def get_user_title_comments_ratings_dict(self, title: Title) -> dict:
        """
        Get user-rated comments for a title in a dictionary to get a comment in O(1) in template
        """    
        comments_ratings = dict()
        user_title_comments_ratings = Comment_rating.objects.filter(user=self.request.user, title=title).all()

        for comment_rating in user_title_comments_ratings:
            comments_ratings[comment_rating.comment.id] = comment_rating.is_liked

        return comments_ratings

    def post(self, request, **kwargs):   
        if not self.request.user.is_authenticated: 
            return redirect("remanga:signin")

        dir_name = self.kwargs.get('dir_name')  
        title = Title.objects.get(dir_name=dir_name)
        form_name = request.POST['form_name']
        form_name_key = form_name.split("_")[0].replace("dis", "")
        response_data = {}
        
        post_forms_methods = self.init_post_forms_methods()
        post_forms_methods[form_name_key](title, form_name, response_data)

        title.save()

        return JsonResponse(response_data)

    def init_post_forms_methods(self) -> dict[str, Any]:
        return {
            'rating': self.change_rating,
            'like': self.rating_comment,
        }

    def change_rating(self, title: Title, form_name: str, response_data: dict) -> None:
        """
        Change the rating of a title by deleting or adding a new rating
        """         
        rating_str = [letter for letter in form_name if letter.isdigit()]
        rating = int("".join(rating_str)) 
        
        title_rating = self.get_title_rating(title)
        is_same_title_rating_exists = title_rating.rating == rating if title_rating else False 

        self.remove_rating(title, title_rating)
        self.add_rating(title, rating, is_same_title_rating_exists)
        
        title_rating = self.get_title_rating(title)

        response_data['avg_rating'] = title.avg_rating
        response_data['count_rating'] = title.count_rating
        response_data['title_rating'] = title_rating.rating if title_rating else "None"

    def remove_rating(self, title: Title, title_rating: Title_rating) -> None:
        if not title_rating: return

        count_rating_except_current = title.count_rating - 1 if title.count_rating > 1 else 1
        title.avg_rating = (title.avg_rating * title.count_rating - title_rating.rating) / count_rating_except_current
        title.count_rating -= 1

        title_rating.delete()

    def add_rating(self, title: Title, rating: int, is_same_title_rating_exists: bool) -> None:
        if (is_same_title_rating_exists): return

        title.avg_rating = (title.avg_rating * title.count_rating + rating) / (title.count_rating + 1)
        title.count_rating += 1
        title_rating_object = Title_rating(user=self.request.user, title=title, rating=rating)

        title_rating_object.save()

    def rating_comment(self, title: Title, form_name: str, response_data: dict):
        comment_rating_str = [letter for letter in form_name if letter.isdigit()]
        comment_rating = int("".join(comment_rating_str)) 
        comment = Comment.objects.get(id=comment_rating)
        
        comment_rating_object = Comment_rating.objects.filter(user=self.request.user, 
            title=comment.title, comment=comment).first()    

        is_same_comment_rating = self.is_same_comment_rating_exists(comment_rating_object, form_name)

        self.remove_comment_rating(comment, comment_rating_object)
        self.add_comment_rating(comment, form_name, is_same_comment_rating)

        comment.save()

        response_data['comment_likes'] = comment.likes
        response_data['comment_rating'] = None if is_same_comment_rating else form_name

    def is_same_comment_rating_exists(self, comment_rating_object: Comment_rating, form_name: str) -> bool:
        if comment_rating_object:
            return not comment_rating_object.is_liked if 'dislike' in form_name else comment_rating_object.is_liked
        
        return False

    def remove_comment_rating(self, comment: Comment, comment_rating_object: Comment_rating) -> None:    
        if not comment_rating_object: return
            
        if comment_rating_object.is_liked:
            comment.likes -= 1
        else:
            comment.likes += 1

        comment_rating_object.delete()    

    def add_comment_rating(self, comment: Comment, form_name: str, is_same_comment_rating: bool) -> None:
        if (is_same_comment_rating): return

        is_liked = False

        if 'dislike' in form_name:
            comment.likes -= 1
        else:
            comment.likes += 1
            is_liked = True   
        
        comment_rating_object = Comment_rating(user=self.request.user, title=comment.title, comment=comment, is_liked=is_liked)

        comment_rating_object.save()

class SearchView(generic.ListView):
    template_name = "search.html"

    def get_queryset(self):
        return
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_data"] = json.dumps(list(Title.objects.values())).replace('\'', '\\\'')
        return context
    
class SignupView(generic.View):
    template_name = 'signup.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        
        context = { 'form': UserCreationForm() }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({'message': 'registered success'})
        
        return JsonResponse({'detail': form.errors})

class SigninView(generic.ListView):
    template_name = "signin.html"
    
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        
        context = { 'form': AuthenticationForm() }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'authenticated success'})

        return JsonResponse({'detail': form.errors})

class LogutView(generic.ListView):
    def get(self, request):
        logout(request)
        return redirect('/')

class ProfileView(generic.ListView):
    template_name = "profile.html"
    
    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')  
        profile = User.objects.filter(id=user_id)[0]

        context['profile'] = profile
        context['form'] = PasswordChangeForm(self.request.user)

        return context 

    def post(self, request, **kwargs):
        if ('old_password' in request.POST):
            return self.change_password(request)
        
        return self.change_avatar(request)
    
    def change_password(self, request):
        form = PasswordChangeForm(request.user, request.POST)
            
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)                    
            return JsonResponse({'message': 'Password changed'})
        
        return JsonResponse({'detail': form.errors})

    def change_avatar(self, request):
        avatar = request.FILES['avatar']
        avatar.name = f"{self.request.user.id}.jpg"
        response_data = {}       
        avatar_path = os.path.join(settings.MEDIA_ROOT, "users_avatars", avatar.name)

        if (os.path.exists(avatar_path)):
            os.remove(rf'{avatar_path}')

        self.request.user.avatar = avatar
        self.request.user.save()

        return JsonResponse(response_data)
    
class BookmarksView(generic.ListView):
    template_name = "bookmarks.html"
    context_object_name = "titles"

    def get_queryset(self):
        return self.request.user.bookmarks.all()
    
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        return super().get(request, *args, **kwargs)
