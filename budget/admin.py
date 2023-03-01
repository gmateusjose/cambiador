from django.contrib import admin

from budget.models import Budget, BudgetExpense


class BudgetExpenseInline(admin.TabularInline):
    model = BudgetExpense
    extra = 0


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['description', 'total']
    search_fields = ['description']
    inlines = [BudgetExpenseInline]