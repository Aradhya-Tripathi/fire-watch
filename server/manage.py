#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fire_watch.settings")
    import patches

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if "create-admin-user" in sys.argv:
        execute_from_command_line.create_admin_user()
    elif "remove-admin-user" in sys.argv:
        execute_from_command_line.remove_admin_user()
    elif "list-admins" in sys.argv:
        execute_from_command_line.list_admins()
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
