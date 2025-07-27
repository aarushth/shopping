from flask import Flask, render_template, request, redirect, url_for, session
import requests
from cart_utils import add_to_cart, remove_from_cart, update_quantity, clear_cart, calculate_total
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_URL = 'https://dummyjson.com/products'

@app.before_request
def ensure_cart_exists():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/')
def home():
    products = requests.get(API_URL).json()['products']
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = requests.get(f"{API_URL}/{product_id}").json()
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_item(product_id):
    quantity = int(request.form.get('quantity', 1))
    product = requests.get(f"{API_URL}/{product_id}").json()
    add_to_cart(session, product, quantity)
    return redirect(request.referrer)

@app.route('/remove_from_cart/<int:product_id>')
def remove_item(product_id):
    remove_from_cart(session, product_id)
    return redirect(url_for('view_cart'))

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_item_quantity(product_id):
    new_quantity = int(request.form['quantity'])
    update_quantity(session, product_id, new_quantity)
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    total = calculate_total(cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('view_cart'))

    total = calculate_total(cart)

    # Prepare receipt data
    receipt = {
        'items': list(cart.values()),
        'total': total,
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save to session temporarily
    session['receipt'] = receipt

    # Clear cart
    clear_cart(session)

    # Redirect to the receipt page
    return redirect(url_for('receipt'))


@app.route('/receipt')
def receipt():
    receipt = session.pop('receipt', None)
    if not receipt:
        return redirect(url_for('home'))
    return render_template('receipt.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)