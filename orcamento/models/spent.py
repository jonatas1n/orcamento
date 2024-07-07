from orcamento.models import Transaction

class Spent(Transaction):
    class Meta:
        proxy = True
        verbose_name = "Spent"
        verbose_name_plural = "Spents"
