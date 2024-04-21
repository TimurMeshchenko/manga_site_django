from django.urls import path
from remanga.views import catalog_view, profile_view, search_view, title_view, bookmarks_view
from remanga.views.auth_views import logut_view, reset_password_view, signin_view, signup_view

app_name = "remanga"
urlpatterns = [
    path("manga", catalog_view.CatalogView.as_view(), name="catalog"),
    path("manga/search/", search_view.SearchView.as_view(), name="search"),
    path("manga/signup/", signup_view.SignupView.as_view(), name="signup"),
    path("manga/signin/", signin_view.SigninView.as_view(), name="signin"),
    path("manga/reset_password/<uidb64>/<token>/", reset_password_view.ResetPasswordView.as_view(), name="reset_password"),
    path("manga/logout/", logut_view.LogutView.as_view(), name="logout"),
    path("manga/user/<int:user_id>/", profile_view.ProfileView.as_view(), name="profile"),
    path("manga/bookmarks/", bookmarks_view.BookmarksView.as_view(), name="bookmarks"),
    path("manga/<str:dir_name>/", title_view.TitleView.as_view(), name="title"),
]
