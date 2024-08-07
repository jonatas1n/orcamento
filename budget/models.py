from django.db import models
from orcamento.models import Transaction

class Budget(models.Model):
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

    def items(self):
        return Transaction.objects.filter(budget=self)
    
    def revenues(self):
        return self.items().filter(done=False)
    
    def spents(self):
        return self.items().filter(done=True)
    
    def total(self):
        return sum([item.price for item in self.items().all()])
    
    def total_spent(self):
        return sum(list(self.spents().values_list("price", flat=True)))
    
    def total_revenue(self):
        return sum(list(self.revenues().values_list("price", flat=True)))

    def __str__(self):
        return f"{self.owner.username}'s budget"
