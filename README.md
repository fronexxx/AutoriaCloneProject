Run project:

```bash
docker compose up --build
```

Open shell inside container:

```bash
docker compose run --rm app sh
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create test users:
```bash
python manage.py seed_db
```

Created users credentials:

| Role | Email | Password |
|--------|--------|--------|
| Admin | admin@test.com | admin123 |
| Manager | manager@test.com | manager123 |
| Premium Seller | premium@test.com | premium123 |
| Basic Seller | basic@test.com | basic123 |
| Buyer | buyer@test.com | buyer123 |


## Email Configuration

The application uses Gmail SMTP for email delivery.

To enable email functionality (account activation emails and manager notifications), configure the following variables in the `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### Generate Gmail App Password

1. Enable Two-Factor Authentication (2FA) on your Google account.
2. Open Google Account Settings.
3. Navigate to:
   Security → 2-Step Verification → App Passwords
4. Create a new App Password.
5. Copy the generated password and use it as `EMAIL_HOST_PASSWORD`.

### Features Using Email Service

- Account activation emails
- Notifications to managers and administrators about missing car brands or models requested by users
- Profanity validation notifications

### Testing

Register a new account and check the email inbox configured in `EMAIL_HOST_USER`.


## Development Mode

For local testing you can disable real email delivery and print emails directly to the application console:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

All emails will be displayed in Docker logs instead of being sent.


## Database

The project supports PostgreSQL.

During development a local PostgreSQL container can be used.

The application can also be connected to a cloud PostgreSQL database (Neon/Supabase) by updating the database credentials in the `.env` file.


## Postman Collection

Import the collection:

```text
postman/autoria-clone-project.postman_collection.json
autoria-clone-project.postman_environment.json
```

The collection contains all endpoints required to test the application.
```