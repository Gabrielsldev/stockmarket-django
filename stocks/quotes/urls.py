from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("add_stock", views.add_stock, name="add_stock"),
    path("delete/<stock_id>", views.delete, name="delete"),
    path("delete_stock", views.delete_stock, name="delete_stock"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register_user"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("chan_password", views.change_password, name="change_password"),
]
