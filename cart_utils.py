def add_to_cart(session, product, quantity):
    cart = session.get('cart', {})
    pid = str(product['id'])

    if pid in cart:
        cart[pid]['quantity'] += quantity
    else:
        cart[pid] = {
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True

def remove_from_cart(session, product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    session.modified = True

def update_quantity(session, product_id, quantity):
    cart = session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] = quantity
    session['cart'] = cart
    session.modified = True

def clear_cart(session):
    session['cart'] = {}
    session.modified = True

def calculate_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart.values())