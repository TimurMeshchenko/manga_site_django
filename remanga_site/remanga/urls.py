from django.urls import path
from . import views

app_name = "remanga"
urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("manga/<str:dir_name>/", views.TitleView.as_view(), name="title"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("logout/", views.LogutView.as_view(), name="logout"),
    path("user/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path("bookmarks/", views.BookmarksView.as_view(), name="bookmarks"),
]
