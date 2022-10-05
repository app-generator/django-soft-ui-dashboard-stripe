import datetime
import json
from http import HTTPStatus

import stripe
from django import views
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apps.ecommerce.forms import ProductForm, SaleForm
from apps.ecommerce.models import Products, Sales


class AdminSalesView(views.View):

    def get(self, request):
        sales = Sales.objects.all().order_by("-timestamp")
        return render(request, "sales/datatable.html", context={
            "sales": sales
        })

    def put(self, request, sale_id):
        try:
            sale = Sales.objects.get(id=sale_id)
        except Sales.DoesNotExist:
            return JsonResponse(data={
                "message": "Sale not found."
            }, status=HTTPStatus.NOT_FOUND)
        data = json.loads(request.body)
        sales_form = SaleForm(data, instance=sale)
        if not sales_form.is_valid():
            return JsonResponse(data={
                "detail": sales_form.errors
            }, status=HTTPStatus.BAD_REQUEST)
        sales_form.save()
        return JsonResponse(data={}, status=HTTPStatus.OK)


class AdminProductsView(views.View):

    def get(self, request):
        form = ProductForm()
        products = Products.objects.all()
        return render(request, "products/datatable.html", context={
            "form": form,
            "products": products
        })

    def post(self, request):
        product_form = ProductForm(request.POST)
        if not product_form.is_valid():
            return JsonResponse(data={
                "detail": product_form.errors
            }, status=HTTPStatus.BAD_REQUEST)
        product_form.save()
        products = Products.objects.all()
        return render(request, "products/datatable.html", context={
            "form": ProductForm(),
            "products": products
        })

    def put(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return JsonResponse(data={
                "message": "Product not found"
            }, status=HTTPStatus.NOT_FOUND)
        data = json.loads(request.body)
        product_form = ProductForm(data, instance=product)
        if not product_form.is_valid():
            return JsonResponse(data={
                "detail": product_form.errors
            }, status=HTTPStatus.BAD_REQUEST)
        product_form.save()
        return JsonResponse(data={}, status=HTTPStatus.OK)

    def delete(self, request, product_id):
        to_delete_product = Products.objects.filter(id=product_id)
        if to_delete_product.count() == 0:
            return JsonResponse(data={
                "detail": "Product not found"
            }, status=HTTPStatus.NOT_FOUND)
        to_delete_product.delete()
        return JsonResponse(data={}, status=HTTPStatus.OK)


def purchase(request):
    return render(request, 'ecommerce/purchase.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY}, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        try:
            product_pk = request.GET.get('product')
            if not product_pk:
                raise Exception("product id not provided.")
            product = Products.objects.get(pk=product_pk)
            quantity = request.GET.get("quantity", 1)
            domain_url = 'http://localhost:8000'
            stripe.api_key = settings.STRIPE_SECRET_KEY
        except Exception as e:
            return JsonResponse({'error': str(e)})

        try:
            sale = Sales.objects.create(
                product=product,
                value=product.price * quantity,
                fees=product.price,
                quantity=quantity,
                client_id=request.user
            )
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + f'{reverse("stripe-success")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=domain_url + reverse("stripe-cancelled"),
                payment_method_types=['card'],
                mode='payment',
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                line_items=[
                    {
                        "price": product.stripe_price_id,
                        "quantity": quantity
                    }
                ],
                metadata={
                    "sale_id": sale.id
                }
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    return render(request, "ecommerce/success.html")


def cancelled(request):
    return render(request, "ecommerce/cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        sale_id = event.data.object.metadata.sale_id

        # Convert from unsuccessful payment to successful
        Sales.objects.filter(id=sale_id).bulk_update(is_successful=True, timestamp=datetime.datetime.now())

        print("Payment was successful.")
    if event['type'] == 'product.created':
        product = event.data.object
        product = Products.objects.create(
            stripe_product_id=product.stripe_id,
            name=product.name,
            full_description=product.description,
            info=product.description,
            payment=0 if product.type == 'one_time' else 1,
            image_url=product.images[0]
        )

        print(f'{product.name} created.')
    if event['type'] == 'product.updated':
        product = event.data.object
        if product.default_price is not None:

            price = stripe.Price.retrieve(
                product.default_price,
            )
            Products.objects.filter(stripe_product_id=product.stripe_id).update(
                stripe_price_id=product.default_price,
                price=float(price.unit_amount_decimal)/100,
                currency=price.currency,
                stripe_product_id=product.stripe_id,
                name=product.name,
                full_description=product.description,
                info=product.description,
            )


    return HttpResponse(status=200)


class ProductsView(views.View):

    def get(self, request, product_id=None):
        products = Products.objects.all()
        if product_id:
            return render(request, "products/product.html", context={
                "product": products.get(id=product_id),
                "products": products
            })
        return render(request, "products/product.html", context={
            "products": products
        })

