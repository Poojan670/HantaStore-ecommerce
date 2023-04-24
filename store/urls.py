from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name="store"),

    path('cart/', views.cart, name="cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.update_item, name="update_item"),

    path('process_order/', views.process_order, name="process_order"),

    path('register/', views.register_user, name="register"),

    path('login/', views.login_user, name="login"),

    path('logout/', views.logout_user, name="logout"),

    path('view/<int:pk>', views.product_view, name="view"),

    path('search/', views.search, name="search"),

    path('category/<int:pk>', views.category_filter, name="category"),

    path('ratings/<int:num>', views.ratings_filter, name="ratings"),

    path("contact", views.contact, name="contact"),

    path("about", views.about, name="about"),

]
