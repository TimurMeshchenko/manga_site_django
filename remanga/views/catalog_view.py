from django.views import generic
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator

from typing import Union, Any
import json

from remanga.models import Title, Genres, Categories

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

    def add_filter(self, query_key: str, query_key_adapted: str, query_value: int) -> None:                
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
