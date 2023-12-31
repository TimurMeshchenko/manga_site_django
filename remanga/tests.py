from django.test import TestCase
from django.urls import reverse
from django.db.models import Q

from remanga.models import *
from remanga.views import CatalogView


def create_test_db_data():
    test_data = ['a', 'b']

    Title.objects.create(
        manga_type = 'Западный комикс', 
        avg_rating = 8.8 , 
        dir_name = "the_beginning_after_the_end",      
        rus_name = "Начало после конца", 
        description = "<p>Король Грей обладает непревзойденной силой, богатством и престижем в мире", 
        img_url = "the_beginning_after_the_end/high_cover.jpg", 
        count_bookmarks = 199119, 
        count_chapters = 179, 
        issue_year = 2018, 
        count_rating = 28986
    )

    Title.objects.create(
        manga_type = 'b', 
        avg_rating = 8.8 , 
        dir_name = "b",      
        rus_name = "b", 
        description = "<p>Король Грей обладает непревзойденной силой, богатством и престижем в мире", 
        img_url = "the_beginning_after_the_end/high_cover.jpg", 
        count_bookmarks = 199119, 
        count_chapters = 179, 
        issue_year = 2018, 
        count_rating = 28986
    )
    
    for i in test_data:
        Genres.objects.create(name = i)
        Categories.objects.create(name = i)

class CatalogViewTests(TestCase): 
    catalogView = CatalogView()

    def setUp(self):
        create_test_db_data()
        self.catalogView.init_filters_variables()

    def test_query_params_exceptions(self) -> None:        
        query_params_exceptions = [
            'types=', 'random_query_key=0', 'types=random_query_value',
            'types=0.0', 'issue_year_gte=0.0.0', 'types_gte=0',
            'issue_year_exclude=0', 'types=999999999'
        ]
        
        for query_param in query_params_exceptions:
            response = self.client.get(f"/?{query_param}")

            self.assertEqual(response.status_code, 200)    

    def test_create_manga_types_filters(self) -> None:
        query_values = ['0', '1']

        self.catalogView.create_query_key_filters('manga_type', query_values)
        expected_manga_types_filters = self.get_expected_filters(self.catalogView, 'manga_type', query_values) 

        self.assertEqual(self.catalogView.query_key_filters, expected_manga_types_filters)

    def get_expected_filters(self, catalogView: CatalogView, query_key: str, query_values: list[str]) -> Q:
        expected_filters = Q()
        query_key_adapted = catalogView.get_query_key_adapted(query_key)
        title_table_column_data = catalogView.title_table_columns[query_key_adapted]

        for query_value in query_values:
            Q_filter = Q(**{ query_key_adapted: title_table_column_data[int(query_value)] })

            if "exclude" in query_key:
                expected_filters &= ~Q_filter
            else:
                expected_filters |= Q_filter

        return expected_filters
    
    def test_create_greater_range_filters(self) -> None:
        query_values = ['0']

        self.catalogView.create_query_key_filters('issue_year_gte', query_values)
        expected_greater_range_filter = self.get_expected_range_filter(self.catalogView, 'issue_year_gte', query_values) 
        
        self.assertEqual(self.catalogView.query_key_filters, expected_greater_range_filter)

    def get_expected_range_filter(self, catalogView: CatalogView, query_key: str, query_values: list[str]) -> Q:        
        query_key_adapted = catalogView.get_query_key_adapted(query_key)
        query_value = int(query_values[0])
        range_argument = 'lte' if 'lte' in query_key else 'gte'
        
        expected_range_filter = Q(**{f"{query_key_adapted}__{range_argument}": query_value})        

        return expected_range_filter

    def test_create_less_range_filters(self) -> None:
        query_values = ['0']

        self.catalogView.create_query_key_filters('issue_year_lte', query_values)
        expected_less_range_filter = self.get_expected_range_filter(self.catalogView, 'issue_year_lte', query_values) 
        
        self.assertEqual(self.catalogView.query_key_filters, expected_less_range_filter)

    def test_create_other_filters(self) -> None:
        """
        Drop menu filters except manga types
        """  
        query_values = ['0', '1']

        self.catalogView.create_query_key_filters('genres', query_values)
        expected_genres_filters = self.get_expected_filters(self.catalogView, 'genres', query_values) 

        self.assertEqual(self.catalogView.query_key_filters, expected_genres_filters)

    def test_create_filter_manga_types_exclude(self) -> None:
        query_values = ['0', '1']

        self.catalogView.create_query_key_filters('exclude_manga_type', query_values)
        expected_manga_types_filters = self.get_expected_filters(self.catalogView, 'exclude_manga_type', query_values) 

        self.assertEqual(self.catalogView.query_key_filters, expected_manga_types_filters)

class TitleViewTests(TestCase):   
    test_title = None
    url = None

    def setUp(self) -> None:
        create_test_db_data()
        self.create_user()

        self.test_title = Title.objects.all().first()
        self.url = reverse("remanga:title", args=[self.test_title.dir_name])

    def create_user(self) -> None:
        data = {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword', 'email': 'abc@mail.ru'}
        url = reverse("remanga:signup")
            
        self.client.post(url, data)      

    def test_title_post_exceptions(self) -> None:
        data = { 'form_name': 'random_form_name'}
        
        response = self.client.post(self.url, data).json()
        
        self.assertTrue('detail' in response)

    def test_title_rating_exceptions(self) -> None:
        rating_exceptions_values = ['rating_', 'rating_11', 'rating_a']
        
        for rating_exception_value in rating_exceptions_values:
            data = { 'form_name': rating_exception_value}
            response = self.client.post(self.url, data).json()
        
            self.assertFalse(response)

    def test_add_title_rating(self) -> None:
        data = { 'form_name': 'rating_5' }
        previous_count_rating = self.test_title.count_rating

        response = self.client.post(self.url, data).json()
    
        self.assertEquals(response['count_rating'], previous_count_rating + 1)

    def test_remove_title_rating(self) -> None:
        data = { 'form_name': 'rating_5' }
        title_count_rating = self.test_title.count_rating

        self.client.post(self.url, data).json()
        response = self.client.post(self.url, data).json()
    
        self.assertEquals(response['count_rating'], title_count_rating)
        
    def test_rating_comment_exceptions(self) -> None:
        rating_comment_exceptions_values = ['like_', 'like_999', 'like_a']

        for rating_exception_value in rating_comment_exceptions_values:
            data = { 'form_name': rating_exception_value}
            response = self.client.post(self.url, data).json()
        
            self.assertFalse(response) 

    def test_like_comment(self) -> None:
        comment = self.create_comment()
        data = { 'form_name': f'like_{comment.id}' }
        
        self.client.post(self.url, data).json()

        self.assertTrue(Comment_rating.objects.all().first().is_liked)     

    def create_comment(self) -> Comment:
        user = User.objects.all().first()
        comment = Comment.objects.create(author=user, title=self.test_title, content="comment_content")

        comment.save()

        return comment

    def test_dislike_comment(self) -> None:
        comment = self.create_comment()
        data = { 'form_name': f'dislike_{comment.id}' }
        
        self.client.post(self.url, data).json()

        self.assertFalse(Comment_rating.objects.all().first().is_liked)