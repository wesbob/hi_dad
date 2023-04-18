import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Import your models and database configuration
from app import ImagePost

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL').replace(
    'postgres://',
    'postgresql://',
    1
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def add_image_post(title, image_url):
    new_image_post = ImagePost(title=title, image_url=image_url)
    session.add(new_image_post)
    session.commit()
    print(f"Added new image post: {title}")


if __name__ == "__main__":
    title = input("Enter the image post title: ")
    image_url = input("Enter the image URL: ")

    add_image_post(title, image_url)
