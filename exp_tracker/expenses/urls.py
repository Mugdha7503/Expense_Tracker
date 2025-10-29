from django.urls import path
from expenses import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transactions_list, name='transactions-list'),
    path("transactions/create/", views.create_transaction, name='create-transaction'),
    path("transactions/<int:pk>/update/", views.update_transaction, name='update-transaction'),
    path("transactions/<int:pk>/delete/", views.delete_transaction, name='delete-transaction'),
    path("transactions/charts/", views.transactions_charts, name='transactions-charts'),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)