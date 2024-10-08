import os
import re
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL').replace(
    'postgres://',
    'postgresql://',
    1
)

# CREATE THE FLASK APP
app = Flask(__name__)
#FUNCTIONS FOR JINJA FILTERS
def nl2br(value):
    return value.replace('\n', '<br>')
def md_links_to_html(value):
    return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', value)
app.jinja_env.filters['nl2br'] = nl2br
app.jinja_env.filters['md_links_to_html'] = md_links_to_html

# CONFIGURE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CREATE THE DATABASE MODELS_
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
    

class ImagePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ImagePost {self.title}>'


def get_posts():
    return BlogPost.query.order_by(BlogPost.date_created.desc()).all()

# CREATE THE ROUTES
@app.route('/')
def index():
    latest_post = BlogPost.query.order_by(BlogPost.date_created.desc()).first()
    return render_template('index.html', post=latest_post)

@app.route('/archive')
def archive():
    posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
    return render_template('archive.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        return render_template('selected_post.html', post=post)
    else:
        return "Post not found", 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/img_gal')
def image_gallery():
    image_posts = ImagePost.query.order_by(ImagePost.date_created.desc()).all()
    return render_template('img_gal.html', image_posts=image_posts)

API_KEY = os.environ.get('KEY')
@app.route('/api/posts', methods=['GET'])
def api_posts():
    api_key = request.headers.get('KEY')
    if not api_key or api_key != API_KEY:
        abort(401), "Unauthorized, you do not have an API key bozo!"

    posts = get_posts()
    json_posts = []

    for post in posts:
        json_posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            "img": post.image_path or "No image associated with this post",
            'date_created': post.date_created.isoformat()
        })

    return jsonify(json_posts)

if __name__ == '__main__':
    app.run(debug=True)
