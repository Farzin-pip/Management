from django.db.models import QuerySet
from .models import (
    ExpenseCategory,
    Expenses,
    ExpenseAllocations,
    Invoices,
    InvoiceItem,
    Payment
)


def expense_category_list() -> QuerySet[ExpenseCategory]:
    return ExpenseCategory.objects.all()


def expense_category_by_id(pk: int) -> ExpenseCategory:
    return ExpenseCategory.objects.get(pk=pk)


def expenses_list() -> QuerySet[Expenses]:
    return Expenses.objects.all()


def expenses_by_id(pk: int) -> Expenses:
    return Expenses.objects.get(pk=pk)


def expense_allocations_list() -> QuerySet[ExpenseAllocations]:
    return ExpenseAllocations.objects.all()


def expense_allocations_by_id(pk: int) -> ExpenseAllocations:
    return ExpenseAllocations.objects.get(pk=pk)


def invoices_list() -> QuerySet[Invoices]:
    return Invoices.objects.all()


def invoices_by_id(pk: int) -> Invoices:
    return Invoices.objects.get(pk=pk)


def invoice_items_list() -> QuerySet[InvoiceItem]:
    return InvoiceItem.objects.all()


def invoice_item_by_id(pk: int) -> InvoiceItem:
    return InvoiceItem.objects.get(pk=pk)


def payments_list() -> QuerySet[Payment]:
    return Payment.objects.all()


def payment_by_id(pk: int) -> Payment:
    return Payment.objects.get(pk=pk)


def overdue_invoices_list() -> QuerySet[Invoices]:
    return Invoices.objects.filter(status=Invoices.StatusType.OVERDUE).select_related('user', 'unit_id')


def overdue_invoice_by_id(pk: int) -> Invoices:
    return Invoices.objects.select_related('user', 'unit_id').get(pk=pk, status=Invoices.StatusType.OVERDUE)


def invoice_by_unit_and_period(unit, period_start, period_end):
    return Invoices.objects.filter(
        unit_id=unit,
        period_start=period_start,
        period_end=period_end,
        status__in=[
            Invoices.StatusType.UNPAID,
            Invoices.StatusType.PARTIALLY_PAID,
            Invoices.StatusType.OVERDUE
        ]
    ).first()


def facility_booking_invoice_item(booking):
    return InvoiceItem.objects.filter(
        facility_booking=booking
    ).select_related('invoice').first()


def facility_booking_invoice_item_exists(booking):
    return InvoiceItem.objects.filter(
        facility_booking=booking
    ).exists()


def booking_payment_exists(booking):
    return Payment.objects.filter(
        facility_booking=booking,
        status__in=[
            Payment.Status.PENDING,
            Payment.Status.SUCCESSFUL
        ]
    ).exists()