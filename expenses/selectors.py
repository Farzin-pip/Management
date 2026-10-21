from django.db.models import QuerySet
from django.db.models import Sum
from datetime import date
from decimal import Decimal
from buildings.models import Unit, FacilityBookings
from .models import (
    ExpenseCategory,
    Expenses,
    ExpenseAllocations,
    Invoices,
    InvoiceItem,
    Payment, InvoicePenalty
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


def invoice_by_unit_and_period(
    unit: Unit,
    period_start: date,
    period_end: date
) -> Invoices | None:
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


def facility_booking_invoice_item(booking: FacilityBookings) -> InvoiceItem | None:
    return InvoiceItem.objects.filter(
        facility_booking=booking
    ).select_related('invoice').first()


def facility_booking_invoice_item_exists(booking: FacilityBookings) -> bool:
    return InvoiceItem.objects.filter(
        facility_booking=booking
    ).exists()


def booking_payment_exists(booking: FacilityBookings) -> bool:
    return Payment.objects.filter(
        facility_booking=booking,
        status__in=[
            Payment.Status.PENDING,
            Payment.Status.SUCCESSFUL
        ]
    ).exists()


def invoice_is_settled(invoice: Invoices) -> bool:
    if invoice.status == Invoices.StatusType.PAID:
        return True

    paid_amount = Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    ).aggregate(total=Sum('amount'))['total'] or 0

    return paid_amount >= invoice.total_amount


def successful_payments_total(invoice: Invoices) -> Decimal:
    return Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')


def successful_booking_payment(booking: FacilityBookings) -> Payment | None:
    return Payment.objects.filter(
        facility_booking=booking,
        status=Payment.Status.SUCCESSFUL
    ).first()


def invoice_has_successful_payment(invoice: Invoices) -> bool:
    return Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    ).exists()


def payment_by_authority(authority: str) -> Payment | None:
    return Payment.objects.filter(authority=authority).first()


def invoices_by_unit(unit: Unit) -> QuerySet[Invoices]:
    return Invoices.objects.filter(
        unit_id=unit
    ).prefetch_related(
        'invoiceitem_set'
    ).order_by('due_date')


def successful_payments_by_invoice(invoice: Invoices) -> QuerySet[Payment]:
    return Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    )


def penalties_by_invoice(invoice: Invoices) -> QuerySet[InvoicePenalty]:
    return InvoicePenalty.objects.filter(invoice=invoice)