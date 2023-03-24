from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='WarehouseProduct')
    limit = models.IntegerField()
    tariff = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class WarehouseProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    limit = models.IntegerField()

    def __str__(self):
        return f"{self.warehouse} - {self.product} - {self.limit}"


class Client(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='ClientProduct')

    def __str__(self):
        return self.name


class ClientProduct(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.client} - {self.product} - {self.quantity}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return (
            f"{self.client} - {self.warehouse} - {self.product} - {self.quantity}"
            )
