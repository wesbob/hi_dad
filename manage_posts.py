from app import app, db
from app import BlogPost
from datetime import datetime

def create_post(title, content):
    with app.app_context():
        new_post = BlogPost(title=title, content=content, date_created=datetime.utcnow())
        db.session.add(new_post)
        db.session.commit()
        print(f"New post '{title}' created.")

def list_posts():
    with app.app_context():
        posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
        for post in posts:
            print(f"{post.id}: {post.title} - {post.date_created}")

def update_post(post_id, new_title, new_content):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        if post:
            post.title = new_title
            post.content = new_content
            db.session.commit()
            print(f"Post '{post_id}' updated.")
        else:
            print(f"Post '{post_id}' not found.")

def delete_post(post_id):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            print(f"Post '{post_id}' deleted.")
        else:
            print(f"Post '{post_id}' not found.")

if __name__ == "__main__":
    # Add your CRUD operations here, for example:
    create_post("My Second Post", "This is the content of my first post.")
    list_posts()
    # update_post(1, "Updated Post Title", "Updated post content.")
    # delete_post(1)
    pass
