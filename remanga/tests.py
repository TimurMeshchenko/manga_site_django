from django.test import TestCase
from django.urls import reverse

from remanga.models import *
from .forms import UserCreationForm


def create_titles():
    Title.objects.create(manga_type = 'Западный комикс', avg_rating = 8.8 , dir_name = "the_beginning_after_the_end", 
                        rus_name = "Начало после конца", 
                        description = "<p>Король Грей обладает непревзойденной силой, богатством и престижем в мире", 
                        img_url = "the_beginning_after_the_end/high_cover.jpg", count_bookmarks = 199119, 
                        count_chapters = 179, issue_year = 2018, count_rating = 28986)
    
    Title.objects.create(manga_type = "Манхва", avg_rating = 6 , dir_name = "omniscient-reader", 
                        rus_name = "Всеведущий читатель", 
                        description = "<p>&laquo;Я знаю то, что сейчас произойдёт", 
                        img_url = "", count_bookmarks = 1, 
                        count_chapters = 157, issue_year = 2020, count_rating = 3)
    
    Title.objects.create(manga_type = "Маньхуа", avg_rating = 5.3 , dir_name = "martial_peak", 
                        rus_name = "Пик боевых искусств", 
                        description = "<p>На основе одноименного романа. Путь на вершину боевых искусств", 
                        img_url = "", count_bookmarks = 1, 
                        count_chapters = 3248, issue_year = 2019, count_rating = 3)

class CatalogViewTests(TestCase): 
    def test_titles_filters(self):    
        create_titles()

        response = self.client.get("")
        titles_count = len(response.context["titles_list"])

        self.assertGreater(titles_count, 0)

        self.apply_filters(titles_count)
    
    def apply_filters(self, titles_count):
        response = self.client.get("/?issue_year_gte=2020&issue_year_lte=2020&count_chapters_gte=100&count_chapters_lte=200&exclude_types=0&rating_gte=1&rating_lte=9")

        filtered_titles_count = len(response.context["titles_list"]);  
        
        self.assertLess(filtered_titles_count, titles_count)
        self.assertGreater(filtered_titles_count, 0)

class TitleViewTests(TestCase):     
    def init(self):
        create_titles()
        self.userCreationForm()

        first_title_dir_name = Title.objects.all()[0].dir_name
        self.url = reverse("remanga:title", args=[first_title_dir_name])
        response = self.client.get(self.url) 
        self.title = response.context['title']
        
        self.assertEquals(response.status_code, 200)

    def test_title_post(self):
        self.init()
        self.bookmark_post()
        self.title_rating_post()
        self.comment_post()
        self.like_comment()
        self.dislike_comment()

    def userCreationForm(self):
        data = {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword', 'email': 'abc@mail.ru'}
        form = UserCreationForm(data)
        url = reverse("remanga:signup")

        self.assertTrue(form.is_valid())
            
        self.client.post(url, data)  
    
    def bookmark_post(self):
        data = { 'form_name': 'bookmark' }
        previous_count_bookmarks = self.title.count_bookmarks
        
        response = self.client.post(self.url, data).json()
    
        self.assertTrue(response['is_bookmark_added'])
        self.assertEquals(response['title_count_bookmarks'], previous_count_bookmarks + 1)

    def title_rating_post(self):
        data = { 'form_name': 'rating_5' }
        previous_avg_rating = self.title.avg_rating
        previous_count_rating = self.title.count_rating

        response = self.client.post(self.url, data).json()
    
        self.assertEquals(response['count_rating'], previous_count_rating + 1)
        self.assertNotEquals(response['avg_rating'], previous_avg_rating)
        self.assertNotEquals(response['title_rating'], "None")

        self.title_remove_rating_post(data, previous_count_rating, previous_avg_rating)

    def title_remove_rating_post(self, data, previous_count_rating, previous_avg_rating):
        response = self.client.post(self.url, data).json()

        self.assertEquals(response['count_rating'], previous_count_rating)
        self.assertEquals(response['avg_rating'], previous_avg_rating)
        self.assertEquals(response['title_rating'], "None")        

    def comment_post(self):
        title_comments_count = self.title.comments.count()
        data = { 'form_name': 'comment', 'text': '' }
        
        self.client.post(self.url, data)

        self.assertEquals(self.title.comments.count(), title_comments_count + 1)

    def like_comment(self):
        self.comment_post()

        created_comment = self.title.comments.last()
        data = { 'form_name': f'like_{created_comment.id}' }
        
        response = self.client.post(self.url, data).json()

        self.assertEquals(response['comment_likes'], 1)     

    def dislike_comment(self):
        self.comment_post()

        created_comment = self.title.comments.last()
        data = { 'form_name': f'dislike_{created_comment.id}' }
        
        response = self.client.post(self.url, data).json()

        self.assertEquals(response['comment_likes'], -1)        