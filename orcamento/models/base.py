from django.db import models
from django.utils import timezone
from registry.models import Registry

class SimpleItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiring_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_income(self):
        return self.price > 0
    
    def is_expired(self):
        return self.expiring_date < timezone.now().date()
    
    def __create_registry(self):
        return Registry.objects.create(item=self)
    
    def pay(self):
        self.is_paid = True
        self.save()
        self.__create_registry()

    def __str__(self):
        str_return = "(revenue)" if self.is_income() else "(spent)"
        str_return += f" {self.name}: {self.price}"
        str_return += f" - {self.expiring_date}"
        return str_return

class PeriodicityFixedItem(models.Choices):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    WEEKLY = "weekly"

class FixedItem(SimpleItem):
    class Meta:
        proxy=True

    periodicity = models.CharField(max_length=10, choices=PeriodicityFixedItem.choices)

    def is_expired(self):
        last_registry = Registry.objects.filter(item=self).last()
        periodicity_map = {
            PeriodicityFixedItem.MONTHLY: last_registry.created_at.month != timezone.now().month,
            PeriodicityFixedItem.YEARLY: last_registry.created_at.year != timezone.now().year,
            PeriodicityFixedItem.WEEKLY: last_registry.created_at.week != timezone.now().week
        }
        return periodicity_map[self.periodicity]

    def pay(self):
        self.super().__create_registry()
        pass

    def __str__(self):
        str_return = super().__str__()
        str_return += " - "
        str_return += "monthly" if self.is_monthly else ""
        str_return += "yearly" if self.is_yearly else ""
        str_return += "daily" if self.is_daily else ""
        return str_return
