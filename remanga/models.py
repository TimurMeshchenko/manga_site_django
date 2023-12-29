from django.db import models
from django.contrib.auth.models import AbstractUser

class Genres(models.Model):
    name = models.CharField(max_length=100, default='')
   
    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.name
     
class Title(models.Model):
    rus_name = models.CharField(max_length=100, default='')
    dir_name = models.CharField(max_length=100, default='')
    img_url = models.CharField(max_length=100, default='')
    manga_type = models.CharField(max_length=100, default='')
    avg_rating = models.FloatField(default=0.0)
    count_rating = models.IntegerField(default=0)
    issue_year = models.IntegerField(default=0)
    count_bookmarks = models.IntegerField(default=0)
    count_chapters = models.IntegerField(default=0)
    description = models.CharField(max_length=1500, default='')
    categories = models.ManyToManyField(Categories)
    genres = models.ManyToManyField(Genres)

    def __str__(self):
        return self.rus_name

class Title_chapters(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='chapters')
    chapter = models.IntegerField()
    tome = models.IntegerField()

    class Meta:
        ordering = ['-tome', '-chapter']

class User(AbstractUser):
    bookmarks = models.ManyToManyField(Title)
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)

    class Meta:
        db_table = 'auth_user'

class Title_rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    rating = models.IntegerField()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content    
    
class Comment_rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_liked = models.BooleanField()
