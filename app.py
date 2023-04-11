from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv

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
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"Using database: {app.config['DATABASE_URL']}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CREATE THE DATABASE MODEL
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

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



if __name__ == '__main__':
    app.run(debug=True)
