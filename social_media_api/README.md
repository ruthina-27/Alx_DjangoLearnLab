# social_media_api

Minimal Django project scaffold for a Social Media API lab.

Setup

1. Create a virtualenv and activate it.
2. Install dependencies:

   pip install -r requirements.txt

3. Run migrations:

   python manage.py migrate

4. Create a superuser (optional):

   python manage.py createsuperuser

5. Run the dev server:

   python manage.py runserver

Endpoints

- POST /api/accounts/register/  {username, email, password} -> returns {token}
- POST /api/accounts/login/     {username, password} -> returns {token}
- GET  /api/accounts/profile/   (auth token required) -> returns user profile
