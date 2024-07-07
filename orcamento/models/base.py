from django.db import models
from django.utils import timezone
from registry.models import Registry
from orcamento.utils import get_expired_dates_util, next_expiracy_date

class Periodicity(models.Choices):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    WEEKLY = "weekly"

class AbstractItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    done = models.BooleanField(default=False)

    is_fixed = models.BooleanField(default=False)

    budget = models.ForeignKey("budget.Budget", on_delete=models.CASCADE, blank=True, null=True)

    expiring_date = models.DateField()
    expire_work_day = models.BooleanField(default=False)
    is_next_work_day = models.BooleanField(default=True)

    periodicity = models.CharField(max_length=10, choices=Periodicity.choices, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_income(self):
        return self.price > 0
    
    def is_expired(self):
        return self.expiring_date < timezone.now().date()
    
    def __create_registry(self):
        return Registry.objects.create(item=self)
    
    def next_work_day(self, date):
        if date.weekday() == 5:
            return date + timezone.timedelta(days=2)
        if date.weekday() == 6:
            return date + timezone.timedelta(days=1)
        return date
    
    def previous_work_day(self, date):
        if date.weekday() == 0:
            return date - timezone.timedelta(days=2)
        if date.weekday() == 6:
            return date - timezone.timedelta(days=1)
        return date
    
    def pay(self):
        self.done = True
        self.save()
        self.__create_registry()

    def __str__(self):
        str_return = "(revenue)" if self.is_income() else "(spent)"
        str_return += f" {self.name}: {self.price}"
        str_return += f" - {self.expiring_date}"
        return str_return


class AbstractFixedItem(AbstractItem):
    class Meta:
        proxy=True

    is_fixed = True

    def __next_expiracy_date(self, date=timezone.now()):
        return next_expiracy_date(self, date)

    def is_expired(self):
        if self.periodicity is None:
            raise ValueError("Periodicity must be set for FixedItem")

        last_registry = Registry.objects.filter(item=self).last()
        if not last_registry:
            return True
        
        return last_registry.created_at.date() < self.__next_expiracy_date()
    
    def get_expired_dates(self):
        return get_expired_dates_util(self.id)

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
