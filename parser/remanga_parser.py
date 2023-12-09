import requests
import json
import urllib.request
import os 
import psycopg2

class Remanga_parser():
    def __init__(self):
        self.connect_to_database()
        self.cursor = self.db_connection.cursor()
         
        os.chdir('../') 

    def connect_to_database(self) -> None:
        self.db_connection = psycopg2.connect(
            database="remanga",
            user="postgres",
            password="Qewads",
            host="127.0.0.1",
            port='5432'
        )

    def add_titles_to_database(self) -> None:
        title_data_keys: list[str] = ['rus_name','dir', 'cover_high', 'type', 'issue_year', 'categories', 'genres']
        # catalog_url: str = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
        titles_count: int = 30

        for titles_page in range(11, 12):
            catalog_url: str = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=" + str(titles_page)
            
            for title_number in range(titles_count):
                self.title_data_values: list = list()
                self.categories_genres: dict[str, list] = { 'categories': list(), 'genres': list() }
                
                self.request_json_data(catalog_url)
                self.dir_name: str = self.json_data[title_number]['dir']
                
                self.collect_title_data(title_data_keys, title_number)
                self.collect_title_detailed_data(title_number)
                self.add_title()

                self.cursor.execute(f"SELECT id FROM remanga_title WHERE dir_name = '{self.dir_name}'")
                temp_title_id = self.cursor.fetchone()[0]

                self.add_categories_genres(temp_title_id)
                self.add_chapters(temp_title_id)

        self.cursor.close()
        self.db_connection.close()
   
    def request_json_data(self, url: str) -> None:
        response = requests.get(url)

        self.json_data = json.loads(response.text)['content']

    def collect_title_data(self, title_data_keys: list[str], title_number: int) -> None:
        is_description_request: bool = 'description' in title_data_keys
        
        for title_data_key in title_data_keys:
            title_data: str = self.get_title_data(title_data_key, title_number, is_description_request)

            if title_data_key == 'cover_high':
                self.download_cover(title_data)  
                title_data = title_data.replace('titles/', '')

            elif title_data_key in ['categories', 'genres']:
                self.collect_categories_or_genres(title_data, title_data_key)
                continue

            self.title_data_values.append(title_data)
                        
    def get_title_data(self, title_data_key: str, title_number: int, is_description_request: bool) -> None:
        if is_description_request:
            title_data = self.json_data[title_data_key]
        else:
            title_data = self.json_data[title_number][title_data_key]
        
        return title_data

    def collect_categories_or_genres(self, title_data: str, title_data_key: str) -> None:
        for name_id in range(len(title_data)):
            self.categories_genres[title_data_key].append(title_data[name_id]['name'])

    def download_cover(self, title_data: str) -> None:
        url: str = f'https://remanga.org/media/{str(title_data)}'
        dir_name: str = url.rsplit('/')[-2]
        file_name: str = url.rsplit('/')[-1]

        img_dir: str = rf'remanga_site\remanga\media\titles\{dir_name}'
        file_path: str = os.path.join(img_dir, file_name)

        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        urllib.request.urlretrieve(url, file_path)        

    def collect_title_detailed_data(self, title_number: int) -> None:    
        url: str = 'https://api.remanga.org/api/titles/' + str(self.dir_name)
        title_detailed_data_keys: list[str] = ['description', 'count_chapters']

        self.request_json_data(url)
        self.collect_title_data(title_detailed_data_keys, title_number)

    def add_title(self) -> None:
        self.cursor.execute("INSERT INTO remanga_title (rus_name, dir_name, img_url, manga_type, issue_year, \
                            description, count_chapters) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                            tuple(self.title_data_values))
        
        self.db_connection.commit()

    def add_categories_genres(self, temp_title_id) -> None:
        for key in self.categories_genres:
            for data in self.categories_genres[key]:
                self.cursor.execute(f"SELECT id FROM remanga_{key} WHERE name = '{data}'")
                temp_category_genre_id = self.cursor.fetchone()[0]

                self.cursor.execute(f"INSERT INTO remanga_title_{key} (title_id, {key}_id) VALUES (%s, %s)", 
                                    (temp_title_id, temp_category_genre_id))

        self.db_connection.commit()

    def add_chapters(self, temp_title_id) -> None:
        branches_id: str = self.json_data['branches'][0]['id']   
        default_count_chapters_in_page = count_chapters_in_page = 40
        number_page: int = 1

        while (count_chapters_in_page == default_count_chapters_in_page):
            url: str = f'https://api.remanga.org/api/titles/chapters/?branch_id={branches_id}&ordering=-index&user_data=1&count=40&page={number_page}'
            self.request_json_data(url)
            count_chapters_in_page = len(self.json_data)
 
            for index in range(count_chapters_in_page):
                chapter: str = self.json_data[index]['chapter']
                tome: str = self.json_data[index]['tome']
            
                self.add_chapter(temp_title_id, chapter, tome)
            
            number_page += 1

    def add_chapter(self, temp_title_id, chapter: str, tome: str) -> None:
        if '.' in chapter: return

        self.cursor.execute(f"SELECT id FROM remanga_chapters WHERE chapter = '{chapter}' AND tome = {tome}")
        
        row = self.cursor.fetchone()
        
        if row:
            chapter_id: str = row[0]
        else:
            self.cursor.execute(f"INSERT INTO remanga_chapters (chapter, tome) VALUES ('{chapter}', {tome}) RETURNING id")
            chapter_id: str = self.cursor.fetchone()[0]

        self.cursor.execute("INSERT INTO remanga_title_chapters (title_id, chapters_id) VALUES (%s, %s)", 
                            (temp_title_id, chapter_id))

        self.db_connection.commit()

if __name__ == "__main__":
    Remanga_parser().add_titles_to_database()     

