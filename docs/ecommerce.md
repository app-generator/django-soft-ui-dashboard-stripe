# eCommerce Stripe Integration

Stripe integration has been added to the project with admin and user panels.

## APP Configuration

add 2 environment variables to `.env` file with these names:
```text
STRIPE_PUBLISHABLE_KEY=<Insert-from-stripe-dashboard>
STRIPE_SECRET_KEY=<Insert-from-stripe-dashboard>
```

## Stripe Configuration

1. add products to stripe dashboard
2. copy `product_id` and `price_id` of stripe product
3. go to product admin page and add a product
4. paste copied ids to this product fields.

## Routes and Pages

`/ecommerce/admin/products/` : Add, Update and delete products from app (product admin page)

`/ecommerce/admin/sales/` : See succeed pays

`/ecommerce/products/` : Shopping page

## Manage Stripe Hooks (local env)

- Install Stripe CLI: ` scoop install stripe`
- Login to Stripe: `stripe login`
- Forward events to app webhook point:
  - `stripe listen --forward-to localhost:8000/webhook`
  - copy generated signature to variable `STRIPE_ENDPOINT_SECRET` of `setting.py`

## How to use the feature

### Create one-time payment product 

> Create product in app

@ToDo

> The Stripe related configuration for each product

@ToDo

<br />

### Create recurent (subscription) payment 

> Create product in app

@ToDo

> The Stripe related configuration for each product

@ToDo

<br />

### Manage existing products

> List all products

@ToDo

> View product

<br />

### Purchase 

> Purchase One-time payment product 

@ToDo

> Purchase subscription payment product 

@ToDo

### Visualize sales 

> List all sales

@ToDo

> View sale 

@ToDo

> Update sale 

