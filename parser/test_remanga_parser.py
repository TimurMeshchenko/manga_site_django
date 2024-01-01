import pytest
from remanga_parser import *

class Test_Remanga_parser():
    pytestmark = pytest.mark.asyncio

    remanga_parser = Remanga_parser()
    catalog_url = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
    title_number = 1
    
    async def test_get_title_json_data(self) -> None:
        title_json_data = await self.remanga_parser.get_title_json_data(self.catalog_url)

        assert len(title_json_data) > 0
    
    async def test_collect_title_data(self) -> None:
        title_data_for_db = list()
        categories_genres = { 'categories': list(), 'genres': list() }
        title_json_data = await self.remanga_parser.get_title_json_data(self.catalog_url)

        await self.remanga_parser.collect_title_data(title_json_data, title_data_for_db, categories_genres, self.title_number)

        assert len(title_data_for_db) + len(categories_genres) == len(self.remanga_parser.title_data_keys)

    async def test_get_title_data(self) -> None:
        title_json_data = await self.remanga_parser.get_title_json_data(self.catalog_url)
        is_description_request = False

        title_data = await self.remanga_parser.get_title_data_from_json(title_json_data, 
            self.remanga_parser.title_data_keys[0] , self.title_number, is_description_request)        
        
        assert len(title_data) > 0
    
    async def test_collect_title_detailed_data(self) -> None:
        """
        Data that is used only on the page with the title
        """
        title_data_for_db = list()
        title_json_data = await self.remanga_parser.get_title_json_data(self.catalog_url)
        dir_name = title_json_data[self.title_number]['dir']
        title_url = 'https://api.remanga.org/api/titles/' + dir_name
        title_detailed_json_data = await self.remanga_parser.get_title_json_data(title_url)        
        title_detailed_categories_genres = None

        await self.remanga_parser.collect_title_data(title_detailed_json_data, title_data_for_db, title_detailed_categories_genres, self.title_number)

        assert len(title_data_for_db) == len(self.remanga_parser.title_detailed_data_keys)
