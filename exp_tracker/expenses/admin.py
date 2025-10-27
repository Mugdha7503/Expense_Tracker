from django.contrib import admin
from expenses.models import User, Category, Transaction

admin.site.register(User)
admin.site.register(Category)           
admin.site.register(Transaction)

