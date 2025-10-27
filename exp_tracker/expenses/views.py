from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction
# Create your views here.
def index(request):
    return render(request, 'expenses/index.html')


@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context= {'transactions': transactions}
    return render(request, 'expenses/transactions_list.html', context)

