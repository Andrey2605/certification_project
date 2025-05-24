from django.db import models
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(
        auto_now_add=True, verbose_name="Дата выхода продукта"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    LEVEL_CHOISE = (
        (0, "Завод"),
        (1, "Розничная сеть"),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    email = models.EmailField(max_length=100, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=100, verbose_name="Номер дома")
    create_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    level = models.IntegerField(choices=LEVEL_CHOISE, default=0, verbose_name="Объект")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"


class Consumer(models.Model):
    LEVEL_CHOISE = (
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    email = models.EmailField(max_length=100, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=100, verbose_name="Номер дома")
    create_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, verbose_name="Поставщик"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    level = models.IntegerField(
        choices=LEVEL_CHOISE, verbose_name="Объект", null=True, blank=True
    )
    debt_to_supplier = models.DecimalField(
        verbose_name="Задолженность перед поставщиком",
        max_digits=12,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Потребитель"
        verbose_name_plural = "Потребители"

    def __str__(self):
        return self.name

    def clean(self):
        # Проверка логики уровней
        if self.supplier:
            # Уровень потребителя не может быть меньше уровня поставщика
            if self.level is None:
                raise ValidationError({"level": "Укажите уровень объекта"})
            if self.level <= self.supplier.level:
                raise ValidationError(
                    {"level": "Потребитель не может быть младше или равен поставщику"}
                )
            # Поставщик не может себе поставлять товары
            if self.supplier == self:
                raise ValidationError(
                    {"supplier": "Поставщик не может быть себе поставщиком"}
                )
