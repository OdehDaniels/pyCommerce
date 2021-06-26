from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path('accounts/login/', auth_views.LoginView.as_view()),
    path("create-listing", views.createListing, name="create listing"),
    path("list/<int:list_id>", views.list, name="list")
]
