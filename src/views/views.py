import requests
from flask import Blueprint, render_template,flash, redirect, request, jsonify
from intasend import APIService

from src.models.models import Product, Cart, Order
from flask_login import login_required, current_user
from src import db
from requests.auth import HTTPBasicAuth

from src.views.test import phone_number

views = Blueprint('views', __name__)


API_PUBLISHABLE_KEY = 'ISPubKey_test_813ac5a8-6ddc-48e9-bc7c-77a6c32baa9d'

API_TOKEN = 'ISSecretKey_test_845b83ed-b8e9-43bd-ae6e-c713611e7971'

@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale = True)
    return render_template('home.html', items= items, cart= Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists =  Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f'Quantity of {item_exists.product.product_name} has been updated')
            return redirect(request.referrer)

        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of {item_exists.product.product_name} not updated')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to cart')

    return redirect(request.referrer)

@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount+200)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity



        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity



        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)



@views.route('/removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)















@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity

            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number=phone_number, email=current_user.email,
                                                                   amount=total + 200, narrative='Purchase of goods')

            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']

                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)

                product = Product.query.get(item.product_link)

                product.in_stock -= item.quantity

                db.session.delete(item)

                db.session.commit()

            flash('Order Placed Successfully')

            return redirect('/orders')
        except Exception as e:
            print(e)
            flash('Order not placed')
            return redirect('/')
    else:
        flash('Your cart is Empty')
        return redirect('/')


@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)



@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

    return render_template('search.html')

# # @views.route('/place-order')
# # @login_required
# # def place_order():
# #     customer_cart = Cart.query.filter_by(customer_link=current_user.id)
# #     if customer_cart:
# #         total = 0
# #         for item in customer_cart:
# #             total += item.product.current_price * item.quantity
# #
# #         service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
# #         create_order_response = service.collect.mpesa_stk_push(phone_number=)
#
#
#
#
#
#
#
#
#
# @views.route('/place-order')
# @login_required
# def place_order():
#     customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
#     if customer_cart:
#         total = 0
#         for item in customer_cart:
#             total += item.product.current_price * item.quantity
#
#         total_amount = str(total)
#
#         api_url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
#         client_id = "your_sandbox_business_client_id"
#         secret = "your_sandbox_business_secret"
#
#         basic_auth = HTTPBasicAuth(client_id, secret)
#         headers = {
#             "Content-Type": "application/json",
#         }
#
#         order_data = {
#             "intent": "CAPTURE",
#             "purchase_units": [{
#                 "amount": {
#                     "currency_code": "USD",
#                     "value": total_amount
#                 }
#             }]
#         }
#
#         response = requests.post(api_url, json=order_data, headers=headers, auth=basic_auth)
#
#         if response.status_code == 201:
#             order_response = response.json()
#             order_id = order_response.get("id")
#
#             return redirect(f"/payment/{order_id}")
#
#         else:
#             flash("Ошибка при создании заказа. Попробуйте снова.")
#             return redirect('/cart')
#
#
# @views.route('/payment/<order_id>')
# @login_required
# def payment(order_id):
#     api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}"
#     client_id = "your_sandbox_business_client_id"
#     secret = "your_sandbox_business_secret"
#
#     basic_auth = HTTPBasicAuth(client_id, secret)
#     headers = {
#         "Content-Type": "application/json",
#     }
#
#     response = requests.get(api_url, headers=headers, auth=basic_auth)
#
#     if response.status_code == 200:
#         order_data = response.json()
#         return render_template("payment.html", order_data=order_data)
#     else:
#         flash("Ошибка при получении данных о заказе. Попробуйте снова.")
#         return redirect('/cart')
#
#
# @views.route('/payments/<order_id>/capture', methods=["POST"])
# def capture_payment(order_id):
#     api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
#     client_id = "your_sandbox_business_client_id"
#     secret = "your_sandbox_business_secret"
#     basic_auth = HTTPBasicAuth(client_id, secret)
#
#     headers = {
#         "Content-Type": "application/json",
#     }
#
#     response = requests.post(api_url, headers=headers, auth=basic_auth)
#
#     if response.status_code == 200:
#         order_data = response.json()
#
#         flash("Спасибо за ваш платеж!")
#         return jsonify(order_data)
#     else:
#         flash("Ошибка при обработке платежа.")
#         return jsonify({"error": "Payment capture failed"}), 400
#
#
# @views.route('/invoice/<order_id>')
# @login_required
# def invoice(order_id):
#     order = Order.query.filter_by(id=order_id, customer_link=current_user.id).first()
#
#     if order:
#         order_items = Order.query.filter_by(order_id=order_id).all()
#
#         total_amount = sum(item.product.current_price * item.quantity for item in order_items)
#
#         return render_template('invoice.html', order=order, items=order_items, total=total_amount)
#     else:
#         flash("Заказ не найден.")
#         return redirect('/')
