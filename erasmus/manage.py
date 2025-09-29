#!/usr/bin/env python
import os
import sys

def main():
    """Punto de entrada para las tareas de Django"""
    # manage.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
