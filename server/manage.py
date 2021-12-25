#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


_commands = (
    "create-admin-user",
    "remove-admin-user",
    "list-admins",
    "show-configs",
    "change-admin-password",
)


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
    for command in sys.argv:
        if command in _commands:
            getattr(execute_from_command_line, command.replace("-", "_"))()
            sys.exit(0)

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
