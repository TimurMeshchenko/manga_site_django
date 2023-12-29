from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator

from typing import Union, Any
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

        if not Title_comments_ratings.objects.filter(title_id=title.id).exists():
            Title_comments_ratings.objects.create(title_id=title.id)
        
        context['title'] = title
        context['comments'] = title.comments.all().order_by('-created_at')

        if not self.request.user.is_authenticated: return context

        is_bookmark_added = self.request.user.titles.filter(id=title.id).exists()
        title_rating = self.request.user.ratings.filter(title_id=title.id)

        context['is_bookmark_added'] = is_bookmark_added
        context['title_rating'] = title_rating[0].rating if title_rating.exists() else None
        context['title_comments_ratings'] = self.request.user.titles_comments_ratings.get_or_create(title_id=title.id)[0]
        
        return context 

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

    def init_post_forms_methods(self):
        return \
        {
            'bookmark': self.change_bookmark,
            'rating': self.change_rating,
            'comment': self.post_comment,
            'like': self.rating_comment,
        }

    def change_bookmark(self, title, form_name, response_data):
        is_bookmark_added = self.request.user.titles.filter(id=title.id).exists()

        if is_bookmark_added: 
            self.request.user.titles.remove(title.id)
            title.count_bookmarks -= 1
        else: 
            self.request.user.titles.add(title)
            title.count_bookmarks += 1

        response_data['is_bookmark_added'] = self.request.user.titles.filter(id=title.id).exists()
        response_data['title_count_bookmarks'] = title.count_bookmarks

    def change_rating(self, title, form_name, response_data):
        rating_str = [letter for letter in form_name if letter.isdigit()]
        rating = int("".join(rating_str)) 
        
        is_same_title_rating_exists = self.request.user.ratings.filter(title_id=title.id, rating=rating).exists()

        self.remove_rating(title)
        self.add_rating(title, rating, is_same_title_rating_exists)
        
        title_rating = self.request.user.ratings.filter(title_id=title.id)

        response_data['avg_rating'] = title.avg_rating
        response_data['count_rating'] = title.count_rating
        response_data['title_rating'] = title_rating[0].rating if title_rating.exists() else "None"

    def remove_rating(self, title):
        title_rating = self.request.user.ratings.filter(title_id=title.id)
        
        if not title_rating.exists(): return

        count_rating_except_current = title.count_rating - 1 if title.count_rating > 1 else 1
        title.avg_rating = (title.avg_rating * title.count_rating - title_rating[0].rating) / count_rating_except_current
        title.count_rating -= 1

        self.request.user.ratings.remove(title_rating[0])

    def add_rating(self, title, rating, is_same_title_rating_exists):
        if (is_same_title_rating_exists): return

        rating_object, is_created = Rating.objects.get_or_create(title_id=title.id, rating=rating)
        title.avg_rating = (title.avg_rating * title.count_rating + rating) / (title.count_rating + 1)
        title.count_rating += 1
        self.request.user.ratings.add(rating_object)

    def post_comment(self, title, form_name, response_data):
        comment = Comment.objects.create(author=self.request.user, content=self.request.POST['text'])
        title.comments.add(comment)

        response_data["comment_id"] = comment.id

    def rating_comment(self, title, form_name, response_data):
        comment_rating_str = [letter for letter in form_name if letter.isdigit()]
        comment_rating = int("".join(comment_rating_str)) 
        comment = title.comments.get(id=comment_rating)
        
        self.title_comments_ratings = self.request.user.titles_comments_ratings.filter(title_id=title.id)

        is_same_comment_rating_exists, is_comment_rating_exists, is_comment_liked = \
        self.get_comment_rating_properties(comment, form_name)

        self.remove_comment_rating(comment, is_comment_rating_exists, is_comment_liked)
        self.add_comment_rating(comment, form_name, is_same_comment_rating_exists)

        comment.save()

        response_data['comment_likes'] = comment.likes
        response_data['comment_rating'] = None if is_same_comment_rating_exists else form_name

    def get_comment_rating_properties(self, comment, form_name):
        is_comment_liked = self.title_comments_ratings.filter(comments_likes=comment).exists()
        is_comment_disliked = self.title_comments_ratings.filter(comments_dislikes=comment).exists()
        is_comment_rating_exists = is_comment_liked or is_comment_disliked
        is_same_comment_rating_exists = bool()

        if 'dislike' in form_name:
            is_same_comment_rating_exists = is_comment_disliked
        else:
            is_same_comment_rating_exists = is_comment_liked
                        
        return is_same_comment_rating_exists, is_comment_rating_exists, is_comment_liked

    def remove_comment_rating(self, comment, is_comment_rating_exists, is_comment_liked):    
        if not is_comment_rating_exists: return
        
        if is_comment_liked:
            comment.likes -= 1
            self.title_comments_ratings[0].comments_likes.remove(comment)
        else:
            comment.likes += 1
            self.title_comments_ratings[0].comments_dislikes.remove(comment)

    def add_comment_rating(self, comment, form_name, is_same_comment_rating_exists):
        if (is_same_comment_rating_exists): return
        
        if 'dislike' in form_name:
            comment.likes -= 1
            self.title_comments_ratings[0].comments_dislikes.add(comment)
        else:
            comment.likes += 1
            self.title_comments_ratings[0].comments_likes.add(comment)       

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
        return self.request.user.titles.all()
        
    
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        return super().get(request, *args, **kwargs)
