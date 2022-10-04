from django.urls import path
from apps.ecommerce.views import (
    ProductsView,
    AdminProductsView,
    purchase,
    stripe_config,
    create_checkout_session,
    success,
    cancelled,
    stripe_webhook, AdminSalesView
)

urlpatterns = [
    path("admin/products/", AdminProductsView.as_view()),
    path("admin/products/<int:product_id>/", AdminProductsView.as_view()),
    path("admin/sales/", AdminSalesView.as_view()),
    path("admin/sales/<int:product_id>/", AdminSalesView.as_view()),

    path("products/", ProductsView.as_view()),
    path("products/<int:product_id>/", ProductsView.as_view()),

    path("purchase/", purchase),
    path("config/", stripe_config),
    path("create-checkout-session/", create_checkout_session),
    path("success/", success, name="stripe-success"),
    path("cancelled/", cancelled, name="stripe-cancelled"),
    path('webhook/', stripe_webhook)

]
