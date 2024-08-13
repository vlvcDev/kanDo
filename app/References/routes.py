from datetime import datetime
import uuid
from app import app, db, load_user
from app.models import User, Order, Product, Item, Admin
from app.forms import ProductForm, SignUpForm, SignInForm, OrderForm
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

# sign-in functionality from previous homework
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    signInForm = SignInForm()

    checkMota = load_user('tmota')
    if checkMota == None:
        newAdmin = Admin(id='tmota', email='admin', password=bcrypt.hashpw('1'.encode('utf-8'), bcrypt.gensalt()), title='Professor', name='Thyago Mota')
        db.session.add(newAdmin)
        newProduct1 = Product(code='door-001', description='Ugly Door', type='Door', available=True, price='32.50')
        newProduct2 = Product(code='door-002', description='Gigantic Door', type='Door', available=True, price='3249.99')
        newProduct3 = Product(code='window-001', description='Generic Window', type='Window', available=True, price='19.99')
        # More products can be added in the /add_product page
        db.session.add(newProduct1)
        db.session.add(newProduct2)
        db.session.add(newProduct3)
        db.session.commit()

    if signInForm.validate_on_submit():
        userID = signInForm.id.data
        userPass = signInForm.password.data.encode('utf-8')

        checkUser = load_user(userID)
        if checkUser == None:
            return ('<p>No user found</p>')
        

        if bcrypt.checkpw(userPass, checkUser.password):
            login_user(checkUser)
            print("match")
            return redirect('/orders')
        else:
            return ('<p>Incorrect Password</p>')
    return render_template('signin.html', form=signInForm)

# sign-up functionality from previous homework
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    signUp = SignUpForm()

    if signUp.validate_on_submit():
        password = signUp.password.data
        password_confirm = signUp.password_confirm.data

        existing_user = load_user(signUp.id.data)
        if existing_user:
            flash('User already exists, Please choose a different one', 'error')
            return redirect(url_for('users_signup'))

        if password == password_confirm:
            hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            creation_date = datetime.now().date()
            newUser = User(id=signUp.id.data, email=signUp.email.data, password=hashedPass, creation_date=creation_date)
            db.session.add(newUser)
            db.session.commit()
            return redirect('/index')
        else:
            return ('<p>Password didn\'t match confirmation</p>')
        
    return render_template('signup.html', form=signUp)

    
# sign-out functionality from previous homework
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    if users_signout:
        logout_user()
        return redirect('/index')
    

@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', user=current_user, orders=user_orders)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if not isinstance(current_user._get_current_object(), Admin):
        return redirect(url_for('products'))
    if form.validate_on_submit():
        code = form.code.data
        price = form.price.data
        windowOrDoor = form.type.data
        description = form.description.data
        available = form.available.data

        new_product = Product(code=code, price=price, type=windowOrDoor, description=description, available=available)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('products'))
    
    return render_template('add_product.html', form=form)

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    is_admin = isinstance(current_user._get_current_object(), Admin)
    products = Product.query.all()
    return render_template('products.html', products=products, is_admin=is_admin)

@app.route('/ordered', methods=['POST'])
@login_required
def ordered():
    selected_items = []
    items_for_order = []
    orderID = str(uuid.uuid4())
    i = 0
    newOrder = Order(id=orderID, user_id=current_user.id, creation_date=datetime.utcnow(), status='new')
    for key, quantity in request.form.items():
        if key.startswith('quantity_') and int(quantity) > 0:
            i+=1
            product_code = key.split('_')[1]
            product = Product.query.get(product_code)
            newItem = Item(order_id=orderID, sequential_number=i, product_code=product.code, quantity=quantity)
            if product:
                selected_items.append({
                    'product': product,
                    'quantity': int(quantity)
                })
                items_for_order.append(newItem)
                newOrder.items = items_for_order
                print(selected_items)
                print(newOrder)
                print(items_for_order)
    
    db.session.add(newOrder)
    db.session.commit()
    
        
    return render_template('confirm_order.html', items=selected_items)




# TODO Luis: 
# We need a page for creating an order, and a page for displaying orders
# You need to reference orders.html and order_create.html (neither of them are finished so if you want to figure them out too you can)