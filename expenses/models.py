from django.db import models
from buildings.models import Building, Unit
from django.conf import settings


class ExpenseCategory(models.Model):

    class AllocationType(models.TextChoices):
        FIXED_EQUAL = 'fixed_equal'
        BY_PERSON_COUNT = 'by_person_count'
        BY_AREA_SQM = 'by_area_sqm'
        CUSTOM = 'custom'

    name = models.CharField(max_length=100)
    allocation_type = models.CharField(max_length=20, choices=AllocationType.choices)

    def __str__(self):
        return self.name


class Expenses(models.Model):

    class PayerTarget(models.TextChoices):
        ANY = 'any'
        TENANT_ONLY = 'tenant_only'
        OWNER_ONLY = 'owner_only'

    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    payer_target = models.CharField(max_length=30, choices=PayerTarget.choices)
    title = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.FloatField()
    expense_date = models.DateTimeField()

    def __str__(self):
        return self.title


class ExpenseAllocations(models.Model):

    expenses_id = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    calculation_basis = models.DecimalField(max_digits=12, decimal_places=2)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)


class Invoices(models.Model):

    class StatusType(models.TextChoices):
        UNPAID = 'unpaid'
        PARTIALLY_PAID = 'partially_paid'
        PAID = 'paid'
        OVERDUE = 'overdue'


    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,)
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=StatusType.choices, default=StatusType.UNPAID)


    def __str__(self):
        return f"{self.unit} - {self.period_start} | {self.period_end}"


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    expense_id = models.ForeignKey(Expenses, on_delete=models.SET_NULL, null=True, blank=True,)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice} - {self.title}"


class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        ONLINE_GATEWAY = 'online_gateway'
        POS = 'pos'
        CASH = 'cash'
        CARD_TO_CARD = 'card_to_card'

    class Status(models.TextChoices):
        PENDING_APPROVAL = 'pending_approval'
        SUCCESSFUL = 'successful'
        FAILED = 'failed'

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoices, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    receipt_attachment = models.URLField()
    tracking_code = models.CharField(max_length=100)
    reference_id = models.CharField(max_length=100)
    paid_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_APPROVAL)

    def __str__(self):
        return f"{self.user_id} - {self.amount}"