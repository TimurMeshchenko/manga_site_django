from django.views import generic
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from typing import Union, Any, Optional

from remanga.models import Title, Title_rating, Comment, Comment_rating

class TitleView(generic.ListView):
    template_name = "title.html"

    def get_queryset(self) -> None:
        return

    def get_context_data(self, **kwargs) -> dict[str, Any]:        
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

    def post(self, request: Any, **kwargs) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse]:   
        if not self.request.user.is_authenticated: 
            return redirect("remanga:signin")

        dir_name = self.kwargs.get('dir_name')  
        title = Title.objects.get(dir_name=dir_name)
        form_name = request.POST['form_name']
        form_name_key = form_name.split("_")[0].replace("dis", "")
        response_data = {}
        
        post_forms_methods = {'rating': self.change_rating, 'like': self.rating_comment}

        if not form_name_key in post_forms_methods: 
            return JsonResponse({"detail": "Invalid form name"})

        post_forms_methods[form_name_key](title, form_name, response_data)

        title.save()

        return JsonResponse(response_data)

    def change_rating(self, title: Title, form_name: str, response_data: dict) -> None:
        """
        Change the rating of a title by deleting or adding a new rating
        """         
        rating_str = [letter for letter in form_name if letter.isdigit()]
        
        if not rating_str: return
        
        rating = int("".join(rating_str)) 
        
        if (rating < 1 or rating > 10): return

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

        if not comment_rating_str: return

        comment_rating = int("".join(comment_rating_str)) 
        comment = Comment.objects.filter(id=comment_rating).first()

        if comment is None: return

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
