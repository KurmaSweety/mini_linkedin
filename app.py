from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from models import db, User, Post
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from forms import RegisterForm, EditProfileForm, PostForm
import secrets
from PIL import Image
from flask import current_app
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuioasdfghjklzxcvbnm'  #WTForms key

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MINI_LINKEDIN_DB', 'sqlite:///linkedin_clone.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

#Login-flask
login_manager = LoginManager()
login_manager.init_app(app)

# Set the folder to store uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'profile_pics')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route('/')
def home():
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return render_template('home.html', posts=posts)
    else:
        return render_template('landing.html')  # For guests


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Hash the password
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),  # gets the raw password from form
            method='pbkdf2:sha256',  # secure hashing algorithm
            salt_length=8  # adds 8-character salt for extra security
        )

        # Handle profile picture
        profile_pic_filename = 'default.jpg'
        if form.profile_pic.data:
            pic_file = form.profile_pic.data
            filename = secure_filename(pic_file.filename)
            pic_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pic_file.save(pic_path)
            profile_pic_filename = filename

        # Create user object
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password,
            headline=form.headline.data,
            current_title=form.current_title.data,
            company=form.company.data,
            location=form.location.data,
            skills=form.skills.data,
            education=form.education.data,
            experience_years=form.experience_years.data,
            profile_pic=profile_pic_filename,
            date_joined=datetime.utcnow()
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user)
        flash("Registration successful! You are now logged in.", "success")
        return redirect(url_for('profile'))

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')

        #Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    # Passing True or False if the user is authenticated.
    return render_template("login.html", logged_in = current_user.is_authenticated)
        # Check stored password hash against entered password hashed.


# Only logged-in users can access the route
@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been shared!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #  Resize the image before saving
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            current_user.profile_pic = picture_file

        current_user.headline = form.headline.data
        current_user.current_title = form.current_title.data
        current_user.company = form.company.data
        current_user.location = form.location.data
        current_user.skills = form.skills.data
        current_user.education = form.education.data
        current_user.experience_years = form.experience_years.data

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.headline.data = current_user.headline
        form.current_title.data = current_user.current_title
        form.company.data = current_user.company
        form.location.data = current_user.location
        form.skills.data = current_user.skills
        form.education.data = current_user.education
        form.experience_years.data = current_user.experience_years

    return render_template('edit_profile.html', form=form)

@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully.', 'success')
        return redirect(url_for('profile'))

    form.content.data = post.content
    return render_template('edit_post.html', form=form)

@app.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('profile'))


@app.route('/profile')
@login_required
def profile():
    user = current_user
    posts = user.posts  # SQLAlchemy relationship
    return render_template('profile.html', user=user, posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port= 5003)