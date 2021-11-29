import os

import django
from channels.routing import get_default_application  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchat.settings")
django.setup()
application = get_default_application()
