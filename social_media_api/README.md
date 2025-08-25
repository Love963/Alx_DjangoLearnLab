# Social Media API

A feature-rich **Django REST Framework (DRF)** powered backend for a social media platform.  
This project supports **user accounts, posts, comments, following, likes, and notifications**.

##  Features
- User Accounts
  - Register, Login, Logout
  - Profile with bio and profile picture
  - Follow/unfollow users

- Posts & Comments
  - CRUD operations for posts
  - Comment on posts
  - Feed based on followed users

- Engagement
  - Like/unlike posts
  - Notifications for likes, comments, and follows

- Authentication
  - Token-based authentication (via Django REST Framework)


## Tech Stack
- Backend: Django, Django REST Framework  
- Database: PostgreSQL (for production) / SQLite (for development)  
- Deployment: Heroku with Gunicorn & Whitenoise  
- Other Tools: Django Signals, DRF Pagination & Filtering  


# Installation & Setup

### 1. Clone repository
git clone https://github.com/<your-username>/social_media_api.git
cd social_media_api
