from django.urls import path
from . import views

# app_name = "store"

urlpatterns = [
    path('', views.store, name="store"),

    path('cart/', views.cart, name="cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),

    path('process_order/', views.processOrder, name="process_order"),

    path('register/', views.registerUser, name="register"),

    path('login/', views.loginUser, name="login"),

    path('logout/', views.logoutUser, name="logout"),

    path('view/<int:pk>', views.ProductView, name="view"),

    path('search/', views.search, name="search"),

    path('category/<int:pk>', views.categoryFilter, name="category"),

    path('ratings/<int:num>', views.ratingsFilter, name="ratings"),

    path("contact", views.contact, name="contact"),

    path("about", views.about, name="about"),

]
