from app import app, db
from app import BlogPost
from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Text, END, Button
import pytz

#--------------------MANUAL CRUD FUNCTIONS--------------------#
# if __name__ == "__main__":
#     # Add your CRUD operations here, for example:
#     # create_post("Hey Bucko, Here's my second post!", "I tried to use some sf-ipsum, but it did not paste over right.")
#     # list_posts()
#     # update_post(1, "Updated Post Title", "Updated post content.")
#     # delete_post(2)
#     # count_posts()
#     # write_posts_to_json()
#     pass

#--------------------CRUD FUNCTIONS--------------------#

#DATE FUNCTION
def get_date():
    timeZ_Ce = pytz.timezone('America/Chicago') 
    return datetime.now(timeZ_Ce).strftime("%m/%d/%Y %I:%M %p")


#CREATE
def create_post(title, content):
    with app.app_context():
        new_post = BlogPost(title=title, content=content, date_created=get_date())
        db.session.add(new_post)
        db.session.flush()  # Add this line
        db.session.commit()
        print(f"New post '{title}' created.")

#READ
def get_post(post_id):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        return post

#UPDATE
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

#DELETE
def delete_post(post_id):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            print(f"Post '{post_id}' deleted.")
            return True
        else:
            print(f"Post '{post_id}' not found.")
            return False

#--------------------OTHER FUNCTIONS--------------------#

#LIST
def list_posts():
    with app.app_context():
        posts = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
        return posts


#COUNT
def count_posts():
    with app.app_context():
        num_posts = BlogPost.query.count()
    print(f'There are {num_posts} posts in the database.')

#WRITE TO JSON
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



#--------------------GUI FUNCTIONS--------------------#

#CENTER WINDOW
def center_window(window, width=None, height=None):
    window.update_idletasks()

    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

#Create Post GUI
def gui_create_post():
    create_post_window = Toplevel(root)
    create_post_window.title("Create Post")
    center_window(create_post_window, width=400, height=300)

    title_label = Label(create_post_window, text="Title:")
    title_label.pack(pady=(10, 0))

    title_entry = Entry(create_post_window, width=50)
    title_entry.pack(pady=(0, 10))

    content_label = Label(create_post_window, text="Content:")
    content_label.pack(pady=(0, 0))

    content_text = Text(create_post_window, width=50, height=10)
    content_text.pack(pady=(0, 10))

    create_button = Button(
    create_post_window,
    text="Create Post",
    command=lambda: gui_create_post_success(create_post_window, title_entry, content_text),
)

    create_button.pack()

    create_post_window.mainloop()

#CREATE POST SUCCESS
def gui_create_post_success(create_post_window, title_entry, content_text):
    create_post(title_entry.get(), content_text.get("1.0", END))
    messagebox.showinfo("Success", "Post created successfully!")
    create_post_window.destroy()

#EDIT POST GUI
def gui_edit_post():
    post_id = simpledialog.askinteger("Edit Post", "Enter the post ID to edit:")

    if post_id is not None:
        post = get_post(post_id)

        if post:
            edit_post_window = Toplevel(root)
            edit_post_window.title("Edit Post")
            center_window(edit_post_window, width=400, height=300)

            title_label = Label(edit_post_window, text="Title:")
            title_label.pack(pady=(10, 0))

            title_entry = Entry(edit_post_window, width=50)
            title_entry.insert(0, post.title)
            title_entry.pack(pady=(0, 10))

            content_label = Label(edit_post_window, text="Content:")
            content_label.pack(pady=(0, 0))

            content_text = Text(edit_post_window, width=50, height=10)
            content_text.insert("1.0", post.content)
            content_text.pack(pady=(0, 10))

            save_button = Button(
                edit_post_window,
                text="Save Changes",
                command=lambda: gui_edit_post_success(edit_post_window, post.id, title_entry, content_text),
            )

            save_button.pack()

            edit_post_window.mainloop()
        else:
            messagebox.showerror("Error", f"Post with ID {post_id} not found.")

#EDIT POST SUCCESS
def gui_edit_post_success(edit_post_window, post_id, title_entry, content_text):
    update_post(post_id, title_entry.get(), content_text.get("1.0", END))
    messagebox.showinfo("Success", f"Post {post_id} updated successfully!")
    edit_post_window.destroy()


#LIST POSTS GUI
def gui_list_posts():
    with app.app_context():
        posts = list_posts()
        if not posts:
            messagebox.showinfo("No Posts", "There are no posts in the database.")
        else:
            list_window = Toplevel(root)
            list_window.title("List of Posts")
            center_window(list_window, width=400, height=300)

            for post in posts:
                post_label = Label(
                    list_window,
                    text=f"ID: {post.id}, Title: {post.title}, Date: {post.date_created}",
                )
                post_label.pack(pady=(0, 5))

            list_window.mainloop()

#DELETE POST GUI
def gui_delete_post():
    post_id = simpledialog.askinteger("Delete Post", "Enter the post ID to delete:")

    if post_id is not None:
        success = delete_post(post_id)

        if success:
            messagebox.showinfo("Success", f"Post with ID {post_id} deleted.")
        else:
            messagebox.showerror("Error", f"Post with ID {post_id} not found.")

#MAIN GUI
if __name__ == "__main__":
    # Create a simple tkinter window
    root = tk.Tk()
    root.title("Manage Posts")

    list_posts_button = Button(root, text="List Posts", command=gui_list_posts)
    list_posts_button.pack(pady=(10, 0))

    create_post_button = Button(root, text="Create Post", command=gui_create_post)
    create_post_button.pack(pady=(10, 0))

    edit_post_button = Button(root, text="Edit Post", command=gui_edit_post)
    edit_post_button.pack(pady=(10, 0))

    delete_post_button = Button(root, text="Delete Post", command=gui_delete_post)
    delete_post_button.pack(pady=(10, 0))


    center_window(root, width=300, height=200)

    root.mainloop()

#WRITE POSTS TO JSON
write_posts_to_json()









