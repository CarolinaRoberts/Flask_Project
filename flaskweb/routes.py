import os
import secrets
from flask import render_template, url_for, flash, redirect, request, session
from flaskweb import app, db, bcrypt
from flaskweb.forms import Login, Registration, UpdateAccount
from flaskweb.models import Console, Game, User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    games = Game.query.all()
    return render_template('home.html', games=games)


@app.route("/checkout")
@login_required
def checkout():
    #add help messages
    #validation
    #total price
    return render_template('checkout.html', cart=cart)


@app.route("/confirmation")
@login_required
def confirmation():
    #and you wanna reset the basket too look at how he does it on the third vid
    flash(f'Thank you for your purchase { current_user.username }!', 'success')
    return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='img/' + current_user.image)
    return render_template('account.html', title='Account',
                           image=image, form=form)


@app.route("/game/<int:game_id>")
def game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game.html', title=game.title, game=game)   


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() 
        flash('Thank you for creating an account!. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unable to Login. Username or password may be incorrect.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add_to_cart/<int:game_id>")
def add_to_cart(game_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(game_id)

    flash("The game is added to your shopping cart!")
    return redirect("/cart")



#work on this
@app.route("/cart", methods=['GET', 'POST'])
@login_required
def cart():
    if "cart" not in session:
        flash('There is nothing in your cart.', 'info')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            game = Game.query.get_or_404(item)

            total_price += game.price
            if game.id in cart:
                cart[game.id]["quantity"] += 1
            else:
                cart[game.id] = {"quantity":1, "title": game.title, "price":game.price}
            total_quantity = sum(item['quantity'] for item in cart.values())


        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)

    return render_template('cart.html')



@app.route("/delete_game/<int:game_id>", methods=['GET', 'POST'])
def delete_game(game_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].remove(game_id)

    flash("The game has been removed from your shopping cart!", 'info')

    session.modified = True

    return redirect("/cart")


