from decimal import Decimal
from typing import Any
from datetime import date, timedelta
from buildings.models import FacilityBookings
from .models import (
    ExpenseCategory,
    Expenses,
    ExpenseAllocations,
    Invoices,
    InvoiceItem,
    Payment, InvoicePenalty
)
from .selectors import invoice_by_unit_and_period, facility_booking_invoice_item, facility_booking_invoice_item_exists, \
    booking_payment_exists


def create_expense_category(data: dict[str, Any]) -> ExpenseCategory:
    return ExpenseCategory.objects.create(**data)


def update_expense_category(expense_category: ExpenseCategory, data: dict[str, Any]) -> ExpenseCategory:
    for key, value in data.items():
        setattr(expense_category, key, value)
    expense_category.save()
    return expense_category


def delete_expense_category(expense_category: ExpenseCategory) -> None:
    expense_category.delete()


def create_expenses(data: dict[str, Any]) -> Expenses:
    return Expenses.objects.create(**data)


def update_expenses(expenses: Expenses, data: dict[str, Any]) -> Expenses:
    for key, value in data.items():
        setattr(expenses, key, value)
    expenses.save()
    return expenses


def delete_expenses(expenses: Expenses) -> None:
    expenses.delete()


def create_expense_allocations( data: dict[str, Any]) -> ExpenseAllocations:
    return ExpenseAllocations.objects.create(**data)


def update_expense_allocations(expense_allocations: ExpenseAllocations, data: dict[str, Any]) -> ExpenseAllocations:
    for key, value in data.items():
        setattr(expense_allocations, key, value)
    expense_allocations.save()
    return expense_allocations


def delete_expense_allocations(expense_allocations: ExpenseAllocations) -> None:
    expense_allocations.delete()


def create_invoice(data: dict[str, Any]) -> Invoices:
    return Invoices.objects.create(**data)


def update_invoice(invoice: Invoices, data: dict[str, Any]) -> Invoices:
    for key, value in data.items():
        setattr(invoice, key, value)
    invoice.save()
    return invoice


def delete_invoice(invoice: Invoices) -> None:
    invoice.delete()


def create_invoice_item(data: dict[str, Any]) -> InvoiceItem:
    return InvoiceItem.objects.create(**data)


def update_invoice_item(invoice_item: InvoiceItem, data: dict[str, Any]) -> InvoiceItem:
    for key, value in data.items():
        setattr(invoice_item, key, value)
    invoice_item.save()
    return invoice_item


def delete_invoice_item(invoice_item: InvoiceItem) -> None:
    invoice_item.delete()


def create_payment(data: dict[str, Any]) -> Payment:
    return Payment.objects.create(**data)


def update_payment(payment: Payment, data: dict[str, Any]) -> Payment:
    for key, value in data.items():
        setattr(payment, key, value)
    payment.save()
    return payment


def delete_payment(payment: Payment) -> None:
    payment.delete()


def save_invoice_penalties(invoice, late_months):
    for month in range(1, late_months + 1):
        InvoicePenalty.objects.get_or_create(
            invoice=invoice,
            month_number=month,
            defaults={
                'amount': Decimal('100000.00')
            }
        )


def add_booking_fee_to_invoice(booking: FacilityBookings):
    if booking.payment_type != FacilityBookings.PaymentType.INVOICE:
        return None

    if booking.status != FacilityBookings.StatusType.APPROVED:
        return None

    if booking.is_paid:
        return None

    if facility_booking_invoice_item_exists(booking):
        return None

    today = date.today()
    period_start = today.replace(day=1)

    if today.month == 12:
        period_end = date(today.year, 12, 31)
        due_date = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
        period_end = next_month - timedelta(days=1)
        due_date = next_month

    invoice = invoice_by_unit_and_period(
        booking.unit_id,
        period_start,
        period_end
    )

    if not invoice:
        invoice = Invoices.objects.create(
            unit_id=booking.unit_id,
            user=booking.user_id,
            period_start=period_start,
            period_end=period_end,
            due_date=due_date,
            total_amount=Decimal('0.00'),
            status=Invoices.StatusType.UNPAID
        )

    amount = Decimal(str(booking.fee_amount or 0))

    InvoiceItem.objects.create(
        invoice=invoice,
        facility_booking=booking,
        title=f'هزینه رزرو {booking.facility_id}',
        amount=amount
    )

    invoice.total_amount += amount
    invoice.save()

    return invoice


def cancel_booking_invoice_item(booking: FacilityBookings) -> None:
    invoice_item = facility_booking_invoice_item(booking)

    if not invoice_item:
        return

    invoice = invoice_item.invoice

    invoice.total_amount = max(
        Decimal('0.00'),
        invoice.total_amount - invoice_item.amount
    )
    invoice.save()

    invoice_item.delete()


def create_booking_payment(booking: FacilityBookings):
    if booking.payment_type != FacilityBookings.PaymentType.INSTANT:
        raise ValueError('This booking is not set for instant payment!')

    if booking.status != FacilityBookings.StatusType.APPROVED:
        raise ValueError('Booking must be approved before payment!')

    if booking.is_paid:
        raise ValueError('This booking is already paid!')

    if booking_payment_exists(booking):
        raise ValueError('A payment already exists for this booking!')

    payment = Payment.objects.create(
        facility_booking=booking,
        user_id=booking.user_id,
        unit_id=booking.unit_id,
        amount=Decimal(str(booking.fee_amount or 0)),
        payment_method=Payment.PaymentMethod.ONLINE_GATEWAY,
        status=Payment.Status.PENDING
    )

    return payment


from django.utils import timezone


def confirm_booking_payment(payment, reference_id):
    if payment.status == Payment.Status.SUCCESSFUL:
        return payment

    if payment.status != Payment.Status.PENDING:
        raise ValueError('Payment is not pending!')

    booking = payment.facility_booking

    if not booking:
        raise ValueError('Booking not found!')

    if booking.status != FacilityBookings.StatusType.APPROVED:
        raise ValueError('Booking is not approved!')

    payment.status = Payment.Status.SUCCESSFUL
    payment.reference_id = reference_id
    payment.paid_at = timezone.now()
    payment.save()

    booking.is_paid = True
    booking.save()

    return payment