from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class TransactionQuerySet(models.QuerySet):
    def get_expenses(self):
        return self.filter(type='expense')
    
    def get_income(self):
        return self.filter(type='income')
    
    def get_total_expenses(self):
        return self.get_expenses().aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def get_total_income(self):
        return self.get_income().aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    objects = TransactionQuerySet.as_manager()
    
    def __str__(self):
        return f"{self.type}: {self.amount} on {self.date} by {self.user}"
    
    class Meta:
        ordering = ['-date']
    
   

