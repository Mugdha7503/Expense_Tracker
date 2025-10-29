from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from expenses.models import Transaction
from expenses.filters import TransactionFilter
from expenses.forms import TransactionForm
from django_htmx.http import retarget
from django.db.models import Sum
from django.db.models import Sum
from django.utils.timezone import now
from expenses.models import Transaction


def index(request):
    return render(request, 'expenses/index.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    total_income = transaction_filter.qs.get_total_income()
    total_expense = transaction_filter.qs.get_total_expenses()
    net_income=total_income - total_expense
    context= {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': net_income,
}
    if request.htmx:
        return render(request, 'expenses/partial/transactions-container.html', context)
    return render(request, 'expenses/transactions-list.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': "Transaction was added successfully!"}
            return render(request, 'expenses/partial/transaction-success.html', context)
        else:
            context = {'form': form}
            response= render(request, 'expenses/partial/create-transaction.html', context)
            return retarget(response, '#transaction-block')

    context = {'form': TransactionForm()}
    return render(request, 'expenses/partial/create-transaction.html', context)


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction,pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            context = {'message': "Transaction was updated successfully!"}
            return render(request, 'expenses/partial/transaction-success.html', context)
        else:
            context = {'form': form}
            response= render(request, 'expenses/partial/update-transaction.html', context)
            return retarget(response, '#transaction-block')

    form = TransactionForm(instance=transaction)
    context = {'form': form,
               'transaction': transaction
            }
    return render(request, 'expenses/partial/update-transaction.html', context)


@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {
            'message': f"Transaction of {transaction.amount} on {transaction.date} was deleted successfully!"
    }
    return render(request, 'expenses/partial/transaction-success.html', context)

@login_required
def transactions_charts(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    transactions = transaction_filter.qs

    
    today = now().date()
    month_start = today.replace(day=1)
    current_month_expenses = transactions.filter(date__gte=month_start, type='expense')

    category_data = (
        current_month_expenses
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('category__name')
    )

    pie_labels = [entry['category__name'] for entry in category_data]
    pie_values = [float(entry['total']) for entry in category_data]

   
    expense_over_time = (
        transactions.filter(type='expense')
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    line_labels = [entry['date'].strftime('%Y-%m-%d') for entry in expense_over_time]
    line_values = [float(entry['total']) for entry in expense_over_time]

    context = {
        'filter': transaction_filter,
        'pie_labels': pie_labels,
        'pie_values': pie_values,
        'line_labels': line_labels,
        'line_values': line_values,
    }
    if request.htmx:
        return render(request, 'expenses/partial/charts-container.html', context)
    return render(request, 'expenses/charts.html', context)