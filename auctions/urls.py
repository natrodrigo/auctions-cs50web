from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_new_listing", views.create_new_listing, name="create_new_listing"),
    path("my_auctions",views.my_auctions,name="my_auctions"),
    path("my_watchlist",views.my_watchlist,name="my_watchlist"),
    path("add_to_watchlist/<int:auction_id>",views.add_to_watchlist,name="add_to_watchlist"),
    path("remove_from_watchlist/<int:auction_id>",views.remove_from_watchlist,name="remove_from_watchlist"),
    path("auction/<int:auction_id>",views.auction,name="auction"),
    path("categories/<int:category_id>",views.category_auctions,name="category_auctions"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories",views.categories,name="categories")
]
