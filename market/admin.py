from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from market.models import Consumer, Product, Supplier


@admin.action(description="Обнулить задолженность перед поставщиком")
def reset_debt_to_supplier(self, request, queryset):
    queryset.update(debt_to_supplier=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "release_date")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "create_at",
        "product",
    )
    list_filter = ("city",)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "create_at",
        "product",
        "supplier_link",
        "debt_to_supplier",
        "level",
    )
    list_filter = ("city",)
    actions = [reset_debt_to_supplier]

    def supplier_link(self, obj):
        if obj.supplier:
            # Формируем URL на страницу редактирования поставщика в админке
            url = reverse("admin:market_supplier_change", args=[obj.supplier.id])
            display_text = f"{obj.supplier.get_level_display()}: {obj.supplier.name}"
            # Создаем гиперссылку
            return format_html('<a href="{}">{}</a>', url, display_text)
        return "-"

    supplier_link.short_description = "Поставщик"
