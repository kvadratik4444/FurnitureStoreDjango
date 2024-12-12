from django.contrib import admin
from baskets.models import Basket


class BasketTabAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    search_fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'product', 'quantity', 'created_timestamp')
    search_fields = ('user__username',)
    list_filter = ('created_timestamp', 'product')

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
