# urls.py
from django.urls import path

from . import views
from .views import (
    AddToCartView,
    CartView,
    ProductDetailView,
    ProductListView,
    RemoveFromCartView,
)

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("add-to-cart/<int:pk>/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "remove-from-cart/<int:pk>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
]
