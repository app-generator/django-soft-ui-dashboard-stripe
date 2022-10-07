from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.ecommerce.views import (
    ProductsView,
    AdminProductsView,
    stripe_config,
    create_checkout_session,
    success,
    cancelled,
    stripe_webhook,
    AdminSalesView,
    get_product_data
)

urlpatterns = [
    path("admin/products/", AdminProductsView.as_view()),
    path("admin/products/<int:product_id>/", AdminProductsView.as_view()),
    path("admin/sales/", AdminSalesView.as_view()),
    path("admin/sales/<int:product_id>/", AdminSalesView.as_view()),

    path("products/", ProductsView.as_view()),
    path("products/<int:product_id>/", ProductsView.as_view()),

    path("config/", stripe_config),
    path("create-checkout-session/", create_checkout_session),
    path("success/", success, name="stripe-success"),
    path("cancelled/", cancelled, name="stripe-cancelled"),
    path('webhook', csrf_exempt(stripe_webhook)),
    path('products/stripe_data/<str:product_stripe_id>/', get_product_data)

]
