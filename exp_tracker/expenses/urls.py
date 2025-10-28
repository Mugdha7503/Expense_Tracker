from django.urls import path
from expenses import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transactions_list, name='transactions-list')
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)