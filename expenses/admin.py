from django.contrib import admin
from utils.utils import ReadOnlyModelAdmin
from .models import (
    ExpenseCategory, Expenses, ExpenseAllocations, Invoices,
    InvoiceItem, Payment, InvoicePenalty
)



@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'name', 'allocation_type']
    list_filter = ['allocation_type']
    search_fields = ['name']


@admin.register(Expenses)
class ExpensesAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'title', 'building_id', 'category_id', 'payer_target', 'amount', 'expense_date']
    list_filter = ['payer_target', 'category_id', 'building_id']
    search_fields = ['title', 'description']


@admin.register(ExpenseAllocations)
class ExpenseAllocationsAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'expenses_id', 'unit_id', 'calculation_basis', 'allocated_amount']
    list_filter = ['expenses_id']
    search_fields = ['unit_id__postal_code']


@admin.register(Invoices)
class InvoicesAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'unit_id', 'user', 'period_start', 'period_end', 'due_date', 'total_amount', 'status']
    list_filter = ['status', 'due_date']
    search_fields = ['user__phone_number', 'unit_id__postal_code']


@admin.register(InvoiceItem)
class InvoiceItemAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'invoice', 'title', 'expense_id', 'facility_booking', 'amount']
    search_fields = ['title']


@admin.register(Payment)
class PaymentAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'user_id', 'unit_id', 'invoice_id', 'amount', 'payment_method', 'status', 'paid_at']
    list_filter = ['status', 'payment_method', 'paid_at']
    search_fields = ['user_id__phone_number', 'tracking_code', 'reference_id', 'authority']


@admin.register(InvoicePenalty)
class InvoicePenaltyAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'invoice', 'month_number', 'amount', 'created_at']
    list_filter = ['month_number', 'created_at']
