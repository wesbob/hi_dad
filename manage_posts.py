from app import app, db
from app import BlogPost
from datetime import datetime
import json

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

def count_posts():
    with app.app_context():
        num_posts = BlogPost.query.count()
    print(f'There are {num_posts} posts in the database.')

def write_posts_to_json():
    with app.app_context():
        posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
        posts_json = []
        for post in posts:
            posts_json.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "date_created": post.date_created.isoformat()
            })
        with open("posts.json", "w") as f:
            json.dump(posts_json, f, indent=4)



# if __name__ == "__main__":
#     # Add your CRUD operations here, for example:
#     # create_post("Hey Bucko, Here's my second post!", "I tried to use some sf-ipsum, but it did not paste over right.")
#     # list_posts()
#     # update_post(1, "Updated Post Title", "Updated post content.")
#     # delete_post(2)
#     # count_posts()
#     # write_posts_to_json()
#     pass


import tkinter as tk
from tkinter import messagebox, simpledialog

# ... Rest of your existing manage_posts.py code ...

def gui_create_post():
    title = simpledialog.askstring("New Post", "Enter the post title:")
    content = simpledialog.askstring("New Post", "Enter the post content:")

    if title and content:
        create_post(title, content)
        messagebox.showinfo("Success", "Post created successfully!")
    else:
        messagebox.showerror("Error", "Post title and content cannot be empty.")

def list_posts():
    with app.app_context():
        posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
        return posts

def gui_list_posts():
    posts = list_posts()

    if not posts:
        messagebox.showinfo("No posts", "There are no posts in the database.")
        return

    posts_text = ""
    for post in posts:
        posts_text += f"ID: {post.id}\nTitle: {post.title}\nDate: {post.date_created}\n\n"

    messagebox.showinfo("All Posts", posts_text)


def delete_post(post_id):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False

def gui_delete_post():
    post_id = simpledialog.askinteger("Delete Post", "Enter the post ID to delete:")

    if post_id is not None:
        if delete_post(post_id):
            messagebox.showinfo("Success", f"Post with ID {post_id} deleted successfully.")
        else:
            messagebox.showerror("Error", f"Post with ID {post_id} not found.")


if __name__ == "__main__":
    # Create a simple tkinter window
    root = tk.Tk()
    root.title("Manage Posts")

    create_button = tk.Button(root, text="Create Post", command=gui_create_post)
    create_button.pack(pady=10)

    list_button = tk.Button(root, text="List Posts", command=gui_list_posts)
    list_button.pack(pady=10)

    delete_button = tk.Button(root, text="Delete Post", command=gui_delete_post)
    delete_button.pack(pady=10)

    root.mainloop()

write_posts_to_json()

# import subprocess

# def run_on_heroku(command):
#     subprocess.run(["heroku", "run", "python", "-c", command])

# # Usage example:
# run_on_heroku("from app import create_post; create_post('New post title', 'New post content')")

# if __name__ == "__main__":
#     # Add your CRUD operations here, for example:
#     # run_on_heroku("from app import create_post; create_post('New post title', 'New post content')")
#     # run_on_heroku("from app import list_posts; list_posts()")
#     # run_on_heroku("from app import update_post; update_post(1, 'Updated Post Title', 'Updated post content')")
#     # run_on_heroku("from app import delete_post; delete_post(1)")
#     pass
