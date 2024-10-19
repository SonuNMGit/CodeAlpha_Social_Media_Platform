# CodeAlpha_Social_Media_Platform

Overview-
SnapNest is a vibrant social media platform that allows users to connect, share, and discover content through images and videos. The platform is designed to enhance user engagement with features for posting, liking, commenting, and following other users, creating a dynamic social experience.


Features-
User Registration and Authentication: Secure sign-up and login processes.
User Profiles: Personalized user profiles with profile pictures, bios, and the ability to showcase user posts.
Post Creation: Users can upload photos.
Feed: A dynamic feed displaying posts from followed users and popular content.
Likes and Comments: Users can like and comment on posts to encourage interaction.
Follow/Unfollow System: Users can follow other users to see their content in their feed.
Explore Page: Discover trending posts and new users.


Technologies Used-
Backend: Django.
Frontend: HTML, CSS, JavaScript 
Database: SQLite 
Authentication: built in Django Authentication


Installation-
git clone https://github.com/SonuNMGit/CodeAlpha_Social_Media_Platform-SnapNest.git

cd CodeAlpha_Social_Media_Platform-SnapNest

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

On Windows:

venv\Scripts\activate
On macOS/Linux:

source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser :

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Access the application at http://127.0.0.1:8000.

Usage-
Users can create accounts and personalize their profiles.
Post photos.
Engage with posts through likes and comments.
Follow other users to see their content in your feed.
Explore trending posts and new users through the Explore page.
