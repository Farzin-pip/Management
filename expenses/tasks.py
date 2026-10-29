from celery import shared_task
from django.utils import timezone
from expenses.models import Invoices
from expenses.selectors import successful_payments_total
from expenses.services import save_invoice_penalties


@shared_task
def test_celery():
    print("Celery is working!")


@shared_task
def apply_overdue_invoice_penalties():
    today = timezone.localdate()
    invoices = Invoices.objects.filter(
        due_date__lt=today,
        status__in=[
            Invoices.StatusType.UNPAID,
            Invoices.StatusType.PARTIALLY_PAID,
            Invoices.StatusType.OVERDUE
        ]
    )

    processed = 0

    for invoice in invoices.iterator():
        paid_amount = successful_payments_total(invoice)
        remaining_amount = invoice.total_amount - paid_amount

        if remaining_amount <= 0:
            continue

        late_months = (
            (today.year - invoice.due_date.year) * 12
            + today.month - invoice.due_date.month
        )

        if today.day < invoice.due_date.day:
            late_months -= 1

        if late_months > 0:
            save_invoice_penalties(invoice, late_months)
            processed += 1

    return f"Processed penalties for {processed} invoices."