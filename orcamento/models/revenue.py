from orcamento.models import Transaction

class Revenue(Transaction):
    class Meta:
        proxy = True
        verbose_name = "Revenue"
        verbose_name_plural = "Revenues"