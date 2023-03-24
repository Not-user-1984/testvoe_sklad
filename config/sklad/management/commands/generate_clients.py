from random import choice, randint

from django.core.management.base import BaseCommand
from sklad.models import Product, Warehouse, WarehouseProduct

from config.settings import NUM_WAREHOUSES, PRODUCTS


class Command(BaseCommand):
    help = 'Generates clients'
