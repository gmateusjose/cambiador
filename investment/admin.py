from django.contrib import admin

from investment.models import Etf, Dividend, Purchase, Exchange, ExchangeHistory


@admin.register(Etf)
class EtfAdmin(admin.ModelAdmin):
    list_display = [
        'ticker',
        'expense_ratio',
        'annual_yield',
        'sharpe_ratio_3yr',
        'morningstar_rating',
        'average_usd_cost',
    ]
    list_filter = ['morningstar_rating']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'etf', 'purchased_at', 'usd_price']
    list_filter = ['etf', 'purchased_at']


@admin.register(Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ['id', 'received_at', 'raw_amount', 'net_amount', 'concluded']
    list_filter = ['received_at']

    def concluded(self, obj):
        return f"{obj.net_amount/400 * 100:.2f}%" # Goal 400 USD


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'finished_at',
        'origin',
        'origin_amount',
        'destination',
        'destination_amount',
    ]
    list_filter = ['finished_at', 'origin', 'destination']


@admin.register(ExchangeHistory)
class ExchangeHistoryAdmin(admin.ModelAdmin):
    list_display = ['origin', 'destination', 'average_amount']

    def has_add_permission(self, *args):
        return False

    def has_change_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False
