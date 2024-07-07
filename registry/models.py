from django.db import models

class Registry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.ForeignKey('orcamento.SimpleItem', on_delete=models.CASCADE)

    def __get_item_str(self):
        return str(self.item)

    def __str__(self):
        return f"Movement registry from {self.__get_item_str()}, at {self.created_at}"
