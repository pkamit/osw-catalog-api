from typing import Any, Optional
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help= "Command information"

    def handle(self, *args, **kwargs):
        print("Hello")