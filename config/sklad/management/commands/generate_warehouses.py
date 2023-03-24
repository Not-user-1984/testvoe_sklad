
from decimal import Decimal
from random import choice, randint, uniform

from django.core.management.base import BaseCommand
from django.utils import timezone
from sklad.models import Product, Warehouse, WarehouseProduct

from config.settings import NUM_WAREHOUSES, PRODUCTS


class Command(BaseCommand):
    help = 'Generates warehouses'

    def handle(self, *args, **kwargs):
        for i in range(1, NUM_WAREHOUSES + 1):
            name = f"Warehouse {i}"
            limit = randint(50, 200)
            tariff = round(uniform(1.0, 10.0), 2)
            warehouse = Warehouse.objects.create(name=name, limit=limit, tariff=tariff)
            for product_name in choice(PRODUCTS):
                product = Product.objects.get(name=product_name)
                limit = randint(1, 100)
                WarehouseProduct.objects.create(warehouse=warehouse, product=product, limit=limit)
