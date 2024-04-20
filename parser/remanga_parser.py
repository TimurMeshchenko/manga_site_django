import json
import urllib.request
import os 
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Optional
import aiohttp
import asyncio

class Remanga_parser():
    def __init__(self):        
        load_dotenv()

        self.title_data_keys = ['rus_name','dir', 'cover_high', 'type', 'issue_year', 'categories', 'genres']
        self.title_detailed_data_keys = ['description', 'count_chapters']
        self.connect_to_database()
        self.cursor = self.db_connection.cursor()        

        os.chdir('../') 

    def connect_to_database(self) -> None:
        self.db_connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    async def add_titles(self) -> None:
        tasks = list()
        start_page_parsing = 10
        end_page_parsing = 11 
        titles_count = 30

        for titles_page in range(start_page_parsing, end_page_parsing):
            catalog_url = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=" \
            + str(titles_page)

            for title_number in range(titles_count):
                tasks.append(self.add_title(catalog_url, title_number))

        await asyncio.gather(*tasks)

        self.cursor.close()
        self.db_connection.close()
   
    async def add_title(self, catalog_url: str, title_number: int) -> None:
        title_data_for_db = list()
        categories_genres = { 'categories': list(), 'genres': list() }
                
        title_json_data = await self.get_title_json_data(catalog_url)
        dir_name = title_json_data[title_number]['dir']
        await self.collect_title_data(title_json_data, title_data_for_db, categories_genres, title_number)
                
        title_url = 'https://api.remanga.org/api/titles/' + dir_name
        title_detailed_json_data = await self.get_title_json_data(title_url)
        title_detailed_categories_genres = None
        await self.collect_title_data(title_detailed_json_data, title_data_for_db, 
                                      title_detailed_categories_genres, title_number)

        await self.add_title_data_to_db(title_detailed_json_data, title_data_for_db, categories_genres, dir_name)        

    async def get_title_json_data(self, url: str) -> Any:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()
                title_json_data = json.loads(response_text)['content']
                return title_json_data

    async def collect_title_data(self, title_json_data: Any, title_data_for_db: list, categories_genres: Optional[dict[str, list]], 
            title_number: int) -> None:
        title_data_keys = self.title_detailed_data_keys if categories_genres is None else self.title_data_keys
        is_description_request = 'description' in title_data_keys
        
        for title_data_key in title_data_keys:
            title_data = await self.get_title_data_from_json(title_json_data, title_data_key, title_number, 
                                                             is_description_request)

            if title_data_key == 'cover_high':
                dir_name = title_json_data[title_number]['dir']
                await self.download_cover(title_data, dir_name)  
                title_data = title_data.replace('titles/', '')

            elif title_data_key in ['categories', 'genres']:
                await self.collect_categories_or_genres(title_data, categories_genres, title_data_key)
                continue

            title_data_for_db.append(title_data)
                        
    async def get_title_data_from_json(self, title_json_data: Any, title_data_key: str, 
                                 title_number: int, is_description_request: bool) -> None:
        if is_description_request:
            title_data = title_json_data[title_data_key]
        else:
            title_data = title_json_data[title_number][title_data_key]
        
        return title_data

    async def collect_categories_or_genres(self, title_data: str, categories_genres: dict[str, list], 
                                     title_data_key: str) -> None:
        for name_id in range(len(title_data)):
            categories_genres[title_data_key].append(title_data[name_id]['name'])

    async def download_cover(self, title_data: str, dir_name: str) -> None:
        url = f'https://remanga.org/media/{str(title_data)}'
        dir_name = url.rsplit('/')[-2]
        file_name = url.rsplit('/')[-1]

        img_dir = rf'remanga\media\titles\{dir_name}'
        file_path = os.path.join(img_dir, file_name)

        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

        urllib.request.urlretrieve(url, file_path)        

    async def add_title_data_to_db(self, title_detailed_json_data: Any, title_data_for_db: list, 
                             categories_genres: dict[str, list], dir_name: str) -> None:
        await self.add_title_to_db(title_data_for_db)

        self.cursor.execute(f"SELECT id FROM remanga_title WHERE dir_name = '{dir_name}'")
        title_id = self.cursor.fetchone()[0]

        await self.add_categories_genres(categories_genres, title_id)
        await self.add_chapters(title_detailed_json_data, title_id)        

    async def add_title_to_db(self, title_data_for_db: list) -> None:
        last_columns_values = [0, 0, 0]

        title_data_for_db.extend(last_columns_values)
        
        self.cursor.execute(
            "INSERT INTO remanga_title (rus_name, dir_name, img_url, manga_type, issue_year, \
            description, count_chapters, avg_rating, count_rating, count_bookmarks) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tuple(title_data_for_db))
        
        self.db_connection.commit()

    async def add_categories_genres(self, categories_genres: dict[str, list], title_id: int) -> None:
        for key in categories_genres:
            for data in categories_genres[key]:
                self.cursor.execute(f"SELECT id FROM remanga_{key} WHERE name = '{data}'")

                category_genre = self.cursor.fetchone()

                if category_genre:
                    category_genre_id = category_genre[0]
                else:
                    self.cursor.execute(f"INSERT INTO remanga_{key} (name) VALUES ('{data}') RETURNING id")
                    category_genre_id = self.cursor.fetchone()[0]

                self.cursor.execute(f"INSERT INTO remanga_title_{key} (title_id, {key}_id) VALUES (%s, %s)", 
                                    (title_id, category_genre_id))

        self.db_connection.commit()

    async def add_chapters(self, title_detailed_json_data: Any, title_id: int) -> None:
        branches_id = title_detailed_json_data['branches'][0]['id']   
        default_count_chapters_in_page = count_chapters_in_page = 40
        number_page = 1

        while (count_chapters_in_page == default_count_chapters_in_page):
            chapters_url = f'https://api.remanga.org/api/titles/chapters/?branch_id={branches_id}&ordering=-index&user_data=1&count=40&page={number_page}'
            title_chapters_json_data = await self.get_title_json_data(chapters_url)
            count_chapters_in_page = len(title_chapters_json_data)
 
            for i in range(count_chapters_in_page):
                chapter = title_chapters_json_data[i]['chapter']
                tome = title_chapters_json_data[i]['tome']
            
                await self.add_chapter(title_id, chapter, tome)
            
            number_page += 1

    async def add_chapter(self, title_id: int, chapter: str, tome: int) -> None:
        if '.' in chapter: return

        self.cursor.execute(
            "INSERT INTO remanga_title_chapters (title_id, chapter, tome) VALUES (%s, %s, %s)", (title_id, chapter, tome)
        )

        self.db_connection.commit()

if __name__ == "__main__":
    remanga_parser = Remanga_parser()
    asyncio.run(remanga_parser.add_titles())    
