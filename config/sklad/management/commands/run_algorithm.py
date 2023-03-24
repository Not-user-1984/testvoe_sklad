
from decimal import Decimal
from random import choice, randint, uniform
from django.db.models import Sum, Q
from django.core.management.base import BaseCommand
from django.utils import timezone
from sklad.models import Product, Warehouse, WarehouseProduct
import random
from config.settings import NUM_WAREHOUSES, PRODUCTS


class Command(BaseCommand):
    help = 'run_algorim'

    def handle(self, *args, **kwargs):
        # получаем список складов и товаров из предложения
        warehouses = Warehouse.objects.all()
        products = Product.objects.filter(name__in=PRODUCTS)

        # генерируем список клиентов
        clients = []
        for i in range(settings.NUMBER_OF_CLIENTS):
            client_products = {}
            for product in products:
                quantity = random.randint(0, product.limit)
                client_products[product.name] = quantity
            clients.append(client_products)

        # проходим по каждому клиенту
        for client in clients:
            # ищем оптимальные предложения
            optimal_convenience = None
            optimal_price = None
            for warehouse in warehouses:
                # проверяем, что склад может хранить все товары клиента
                if not set(client.keys()).issubset(set(warehouse.allowed_products)):
                    continue
                # проверяем, что склад не превышает лимит хранения для каждого товара и общий лимит
                if (warehouse.get_total_quantity() + sum(client.values())) > settings.OVERALL_LIMIT:
                    continue
                # вычисляем стоимость транспортировки
                distance = random.randint(1, 100)  # рандомное значение для дистанции
                transport_cost = sum([quantity * distance * product.price for product, quantity in client.items()])
                # вычисляем стоимость хранения на складе
                storage_cost = sum([quantity * product.get_price(warehouse) for product, quantity in client.items()])
                # проверяем, что эта опция - самая удобная
                if optimal_convenience is None or len(warehouse.get_products()) < len(optimal_convenience.get_products()):
                    optimal_convenience = warehouse
                # если нашли несколько опций с минимальным количеством складов, выбираем оптимальную по цене
                elif len(warehouse.get_products()) == len(optimal_convenience.get_products()) and storage_cost + transport_cost < optimal_convenience.get_total_cost(client):
                    optimal_convenience = warehouse
                # проверяем, что эта опция - самая дешевая
                if optimal_price is None or storage_cost + transport_cost < optimal_price.get_total_cost(client):
                    optimal_price = warehouse
            # выводим результаты для текущего клиента
            print(f"Клиент {client}")
            print(f"Оптимальный вариант - самый удобный: {optimal_convenience}")
            print(f"Оптимальный вариант - самый дешевый: {optimal_price}")
            # обновляем лимиты товаров на выбранных складах
            for product, quantity in client.items():
                optimal_convenience.update_product_quantity(product, quantity)
                optimal_price.update_product_quantity(product, quantity)
            # обновляем общий лимит на выбранных складах
            optimal_convenience.update_total_quantity(sum(client.values()))
            optimal_price.update_total_quantity(sum(client.values()))
