import os
from flask import render_template, url_for, flash, redirect, request, session, abort
from flaskweb import app, db, bcrypt
from flaskweb.forms import Login, Registration, UpdateAccount, Checkout, ReviewForm
from flaskweb.models import Console, Game, User, Review
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    games = Game.query.all()
    return render_template('home.html', games=games)


@app.route("/mycheckout", methods=['GET', 'POST'])
@login_required
def mycheckout():
    form = Checkout()
    if form.validate_on_submit():
        return redirect(url_for('confirmation'))
    return render_template('mycheckout.html', form=form)


@app.route("/confirmation")
@login_required
def confirmation():
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
        flash('Thank you for creating an account! You can now log in.', 'success')
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

    flash("The game is added to your shopping cart!", 'success')
    return redirect("/cart")



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


#FILTERS

@app.route("/price")
def price():
    games = Game.query.filter(Game.price <= 10.00)
    return render_template('filter.html', title='Price: Less than £10' , games=games) 


@app.route("/price2")
def price2():
    games2 = Game.query.filter(Game.price >= 25.00)
    return render_template('filter.html', title='Price: £25+' , games2=games2) 



@app.route("/console1")
def console1():
    my_list = [1,4]
    games3 = Game.query.filter(Game.console_id.in_(my_list))
    return render_template('filter.html', title='Console: PlayStation 4' , games3=games3)


@app.route("/console2")
def console2():
    my_list2 = [2,4]
    games4 = Game.query.filter(Game.console_id.in_(my_list2))
    return render_template('filter.html', title='Console: Xbox One' , games4=games4)


@app.route("/console3")
def console3():
    games5 = Game.query.filter(Game.console_id == 3)
    return render_template('filter.html', title='Console: Nintendo Switch' , games5=games5) 


@app.route("/age")
def age():
    games6 = Game.query.filter(Game.age_rating == 3)
    return render_template('filter.html', title='Age Rating: 3' , games6=games6) 

@app.route("/age7")
def age7():
    games10 = Game.query.filter(Game.age_rating == 7)
    return render_template('filter.html', title='Age Rating: 7' , games10=games10) 

@app.route("/age2")
def age2():
    games7 = Game.query.filter(Game.age_rating == 12)
    return render_template('filter.html', title='Age Rating: 12' , games7=games7)  

@app.route("/age3")
def age3():
    games8 = Game.query.filter(Game.age_rating == 16)
    return render_template('filter.html', title='Age Rating: 16' , games8=games8)   

@app.route("/age4")
def age4():
    games9 = Game.query.filter(Game.age_rating == 18)
    return render_template('filter.html', title='Age Rating: 18' , games9=games9) 




#REVIEWS
@app.route("/reviews")
def reviews():
    reviews = Review.query.all()
    return render_template('reviews.html', reviews=reviews)


@app.route("/review/new", methods=['GET', 'POST'])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(title=form.title.data, content=form.content.data, game_title=form.game.data, author=current_user)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been posted!', 'success')
        return redirect(url_for('reviews'))
    return render_template('create_review.html', title='New Review',
                           form=form, legend='New Review')


@app.route("/review/<int:review_id>")
def review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('reviewPage.html', title=review.title, review=review)


@app.route("/review/<int:review_id>/update", methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data
        review.game = form.game.data
        review.content = form.content.data
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(url_for('review', review_id=review.id))
    elif request.method == 'GET':
        form.title.data = review.title
        form.game.data = review.game_title
        form.content.data = review.content
    return render_template('create_review.html', title='Update Review',
                           form=form, legend='Update Review')


@app.route("/review/<int:review_id>/delete", methods=['POST'])
@login_required 
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted!', 'success')
    return redirect(url_for('reviews'))