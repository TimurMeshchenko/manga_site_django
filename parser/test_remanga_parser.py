from remanga_parser import *

class Test_Remanga_parser():
    remanga_parser = Remanga_parser()
    catalog_url: str = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
    title_data_keys: list[str] = ['rus_name','dir', 'cover_high', 'type', 'issue_year', 'categories', 'genres']
    title_number: int = 1

    def test_request_json_data(self):
        self.remanga_parser.request_json_data(self.catalog_url)

        assert len(self.remanga_parser.json_data) > 0
    
    def test_collect_title_data(self) -> None:
        self.remanga_parser.title_data_values = list()
        self.remanga_parser.categories_genres: dict[str, list] = { 'categories': list(), 'genres': list() }

        self.remanga_parser.request_json_data(self.catalog_url)
        self.remanga_parser.collect_title_data(self.title_data_keys, self.title_number)

        assert len(self.remanga_parser.title_data_values) + len(self.remanga_parser.categories_genres) \
        == len(self.title_data_keys)

    def test_get_title_data(self) -> None:
        is_description_request: bool = False

        title_data: str = self.remanga_parser.get_title_data(self.title_data_keys[0] , self.title_number, is_description_request)        
        
        assert len(title_data) > 0
    
    def test_collect_title_detailed_data(self):
        title_detailed_data_keys: list[str] = ['description', 'count_chapters']
        self.remanga_parser.title_data_values = list()

        self.remanga_parser.request_json_data(self.catalog_url)
        self.remanga_parser.dir_name = self.remanga_parser.json_data[self.title_number]['dir']
        self.remanga_parser.collect_title_detailed_data(self.title_number)

        assert len(self.remanga_parser.title_data_values) == len(title_detailed_data_keys)