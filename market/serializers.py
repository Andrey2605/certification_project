from rest_framework import serializers
from rest_framework.reverse import reverse

from market.apps import MarketConfig
from market.models import Consumer, Product, Supplier


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ConsumerSerializer(serializers.ModelSerializer):
    supplier_link = serializers.SerializerMethodField()

    def get_supplier_link(self, obj):
        request = self.context.get("request")
        url = reverse(
            f"{MarketConfig.name}:supplier-detail", kwargs={"pk": obj.supplier.pk}
        )
        return request.build_absolute_uri(url)

    class Meta:
        model = Consumer
        fields = (
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "create_at",
            "product",
            "supplier",
            "supplier_link",
            "debt_to_supplier",
            "level",
        )
        read_only_fields = (
            "debt_to_supplier",
        )  # запретить обновление этого поля через API

    def validate(self, data):
        supplier = data.get("supplier")
        level = data.get("level")
        # Получить текущий экземпляр, если он есть (при обновлении)
        instance = getattr(self, "instance", None)

        # Проверка логики уровней
        if supplier:
            # Если уровень не указан
            if level is None:
                raise serializers.ValidationError({"level": "Укажите уровень объекта"})
            # Проверка уровня поставщика
            supplier_level = supplier.level
            if level <= supplier_level:
                raise serializers.ValidationError(
                    {"level": "Потребитель не может быть младше или равен поставщику"}
                )
            # Поставщик не может быть себе поставщиком
            if instance and supplier == instance:
                raise serializers.ValidationError(
                    {"supplier": "Поставщик не может быть себе поставщиком"}
                )

        return data
