# Permissions and Groups Setup for Bookshelf App

## Custom Permissions
The `Book` model defines the following custom permissions in its `Meta` class:
- `can_view`: Can view book
- `can_create`: Can create book
- `can_edit`: Can edit book
- `can_delete`: Can delete book

## Groups
Create the following groups in the Django admin:
- **Editors**: Assign `can_create`, `can_edit`, and `can_view` permissions.
- **Viewers**: Assign `can_view` permission.
- **Admins**: Assign all four permissions (`can_create`, `can_edit`, `can_delete`, `can_view`).

## Assigning Users to Groups
- Use the Django admin interface to add users to the appropriate groups.

## Enforcing Permissions in Views
- The views for listing, creating, editing, and deleting books use the `@permission_required` decorator to enforce these permissions.
- Example: Only users with `bookshelf.can_edit` can access the edit view.

## Testing
- Log in as users with different group memberships and verify access to each view.
- Users without the required permission will receive a 403 Forbidden error.

## Notes
- Permissions and groups can be managed at any time via the Django admin interface. 

# Security Best Practices

## Secure Settings
- `DEBUG = False` in production
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `CSRF_COOKIE_SECURE = True`
- `SESSION_COOKIE_SECURE = True`

## CSRF Protection
- All forms must include `{% csrf_token %}` in their templates.
- Django's `@csrf_protect` is enabled by default for class-based and function-based views.

## Content Security Policy (CSP)
- The `book_list` view sets a `Content-Security-Policy` header to restrict content sources and reduce XSS risk.

## Secure Data Access
- All user input is handled via Django forms, which provide validation and sanitization.
- Django ORM is used for all database access, preventing SQL injection.

## Testing
- Manually test forms and input fields for CSRF and XSS vulnerabilities.
- Attempt to submit forms without CSRF tokens and verify a 403 error is returned.
- Try injecting scripts in form fields and verify they are not executed.

# HTTPS and Secure Redirects

## Django Settings
- `SECURE_SSL_REDIRECT = True`: Redirects all HTTP requests to HTTPS.
- `SECURE_HSTS_SECONDS = 31536000`: Enforces HSTS for 1 year.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Applies HSTS to all subdomains.
- `SECURE_HSTS_PRELOAD = True`: Allows site to be included in browser preload lists.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`: Cookies only sent over HTTPS.
- `X_FRAME_OPTIONS = 'DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF = True`, `SECURE_BROWSER_XSS_FILTER = True`: Security headers for clickjacking, MIME sniffing, and XSS protection.

## Deployment Configuration
- Obtain and install an SSL/TLS certificate (e.g., via Let's Encrypt).
- Configure your web server (Nginx/Apache) to serve your Django app over HTTPS and redirect all HTTP traffic to HTTPS.
- Example Nginx snippet:

```
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    # ... other SSL settings ...
    # proxy_pass to Django app
}
```

## Security Review
- All HTTP traffic is redirected to HTTPS, ensuring encrypted communication.
- HSTS is enabled, instructing browsers to only use HTTPS for the site and subdomains.
- Secure cookies and security headers are enforced.
- **Potential improvements:**
  - Regularly review SSL/TLS configuration and renew certificates.
  - Use a service like [securityheaders.com](https://securityheaders.com/) to audit your HTTP headers.
  - Consider enabling additional headers such as `Referrer-Policy` and `Feature-Policy` for further hardening.

--- 