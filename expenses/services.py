from django.conf import settings
import requests
from typing import Any
from datetime import date, timedelta
from buildings.models import FacilityBookings, Unit
from django.db.models import Sum
from django.db import models
from .models import (
    ExpenseCategory,
    Expenses,
    ExpenseAllocations,
    Invoices,
    InvoiceItem,
    Payment, InvoicePenalty
)
from .selectors import invoice_by_unit_and_period, facility_booking_invoice_item, facility_booking_invoice_item_exists, \
    booking_payment_exists, invoice_has_successful_payment, invoices_by_unit, successful_payments_by_invoice, \
    penalties_by_invoice


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


from decimal import Decimal
from .models import InvoicePenalty, Invoices, Payment


def invoice_is_settled(invoice):
    if invoice.status == Invoices.StatusType.PAID:
        return True

    paid_amount = Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    return paid_amount >= invoice.total_amount


def save_invoice_penalties(invoice, late_months):
    if invoice_is_settled(invoice):
        return

    if late_months <= 0:
        return

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

    amount = Decimal(str(booking.fee_amount or 0))

    invoice_item = facility_booking_invoice_item(booking)

    if invoice_item:
        invoice = invoice_item.invoice

        if invoice_item.amount == amount:
            return invoice

        if invoice_has_successful_payment(invoice):
            raise ValueError(
                'این فاکتور پرداخت موفق دارد؛ '
                'ابتدا باید وضعیت مالی آن مشخص شود.'
            )

        difference = amount - invoice_item.amount

        invoice_item.amount = amount
        invoice_item.save()

        invoice.total_amount = max(
            Decimal('0.00'),
            invoice.total_amount + difference
        )
        invoice.save()

        return invoice

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

    InvoiceItem.objects.create(
        invoice=invoice,
        facility_booking=booking,
        title=f'هزینه رزرو {booking.facility_id}',
        amount=amount
    )

    invoice.total_amount += amount
    invoice.save()

    return invoice

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

    if invoice_has_successful_payment(invoice):
        raise ValueError(
            'این فاکتور پرداخت موفق دارد؛ ابتدا باید وضعیت مالی آن مشخص شود.'
        )

    invoice.total_amount = max(
        Decimal('0.00'),
        invoice.total_amount - invoice_item.amount
    )
    invoice.save(update_fields=['total_amount'])

    invoice_item.delete()

    update_invoice_status(invoice)


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


def update_invoice_status(invoice: Invoices) -> None:
    successful_payments = Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    )

    paid_amount = successful_payments.aggregate(
        total=models.Sum('amount')
    )['total'] or Decimal('0.00')

    if invoice.total_amount <= Decimal('0.00'):
        invoice.status = Invoices.StatusType.UNPAID

    elif paid_amount >= invoice.total_amount:
        invoice.status = Invoices.StatusType.PAID

    elif paid_amount > Decimal('0.00'):
        invoice.status = Invoices.StatusType.PARTIALLY_PAID

    elif invoice.due_date < timezone.localdate():
        invoice.status = Invoices.StatusType.OVERDUE

    else:
        invoice.status = Invoices.StatusType.UNPAID

    invoice.save(update_fields=['status'])


def create_zarinpal_payment(payment: Payment) -> str:
    if not settings.ZARINPAL_MERCHANT_ID:
        raise ValueError('Zarinpal Merchant ID is not configured.')

    amount = int(payment.amount * 10)

    if amount <= 0:
        raise ValueError('Payment amount must be greater than zero.')

    if payment.status == Payment.Status.SUCCESSFUL:
        raise ValueError('This payment has already been completed.')

    if payment.authority:
        raise ValueError('A payment request has already been created.')

    url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'

    if not settings.ZARINPAL_SANDBOX:
        url = 'https://payment.zarinpal.com/pg/v4/payment/request.json'

    data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': amount,
        'callback_url': settings.ZARINPAL_CALLBACK_URL,
        'description': f'Facility booking payment {payment.facility_booking_id}',
        'metadata': {
            'mobile': payment.user_id.phone_number,
        },
    }

    try:
        response = requests.post(url, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        raise ValueError('Could not connect to Zarinpal.') from e

    if result.get('data', {}).get('code') != 100:
        raise ValueError(
            f"Zarinpal payment request failed: {result.get('errors', result.get('data'))}"
        )

    payment.authority = result['data']['authority']
    payment.status = Payment.Status.PENDING
    payment.save(update_fields=['authority', 'status'])

    base_url = 'https://sandbox.zarinpal.com/pg/StartPay/'

    if not settings.ZARINPAL_SANDBOX:
        base_url = 'https://payment.zarinpal.com/pg/StartPay/'

    return f"{base_url}{payment.authority}"


def verify_zarinpal_payment(payment: Payment) -> dict:
    if not settings.ZARINPAL_MERCHANT_ID:
        raise ValueError('Zarinpal Merchant ID is not configured.')

    if not payment.authority:
        raise ValueError('Payment authority not found.')

    if payment.status == Payment.Status.SUCCESSFUL:
        return {
            'success': True,
            'reference_id': payment.reference_id,
            'message': 'This payment has already been verified.'
        }

    url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'

    if not settings.ZARINPAL_SANDBOX:
        url = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'

    data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': int(payment.amount * 10),
        'authority': payment.authority,
    }

    try:
        response = requests.post(url, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        raise ValueError('Could not connect to Zarinpal.') from e

    result_data = result.get('data', {})
    code = result_data.get('code')

    if code in [100, 101]:
        payment.status = Payment.Status.SUCCESSFUL
        payment.reference_id = str(result_data.get('ref_id', ''))
        payment.paid_at = timezone.now()
        payment.save(update_fields=['status', 'reference_id', 'paid_at'])

        return {
            'success': True,
            'reference_id': payment.reference_id,
            'message': 'Payment verified successfully.'
        }

    payment.status = Payment.Status.FAILED
    payment.save(update_fields=['status'])

    return {
        'success': False,
        'message': 'Payment verification failed.',
        'details': result.get('errors', result_data)
    }


def unit_debt_detail(unit: Unit) -> dict:
    today = date.today()
    invoices_data = []
    total_debt = Decimal('0.00')
    total_penalty = Decimal('0.00')

    for invoice in invoices_by_unit(unit):
        payments = successful_payments_by_invoice(invoice)

        paid_amount = payments.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

        remaining_amount = max(
            Decimal('0.00'),
            invoice.total_amount - paid_amount
        )

        if invoice.due_date and invoice.due_date < today and remaining_amount > 0:
            late_months = (
                (today.year - invoice.due_date.year) * 12
                + today.month - invoice.due_date.month
            )

            if today.day < invoice.due_date.day:
                late_months -= 1

            save_invoice_penalties(invoice, max(0, late_months))

        penalty = penalties_by_invoice(invoice).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

        items = [
            {
                'id': item.id,
                'description': item.title,
                'amount': item.amount
            }
            for item in invoice.invoiceitem_set.all()
        ]

        payment_data = [
            {
                'id': payment.id,
                'amount': payment.amount,
                'status': payment.status,
                'paid_at': payment.paid_at,
                'reference_id': payment.reference_id
            }
            for payment in payments
        ]

        invoices_data.append({
            'invoice_id': invoice.id,
            'status': invoice.status,
            'period_start': invoice.period_start,
            'period_end': invoice.period_end,
            'due_date': invoice.due_date,
            'total_amount': invoice.total_amount,
            'paid_amount': paid_amount,
            'remaining_amount': remaining_amount,
            'penalty': penalty,
            'items': items,
            'payments': payment_data
        })

        total_debt += remaining_amount
        total_penalty += penalty

    return {
        'unit_id': unit.id,
        'unit_number': unit.number,
        'invoices': invoices_data,
        'total_debt': total_debt,
        'total_penalty': total_penalty,
        'total_due': total_debt + total_penalty
    }