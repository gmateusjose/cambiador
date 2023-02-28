from django.contrib import admin

from investment.models import Etf, Dividend, Purchase


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