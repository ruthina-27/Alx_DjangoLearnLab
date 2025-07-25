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