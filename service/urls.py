from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_job/', views.add_job, name='add_job'),
    path('view_job/<int:job_id>/', views.view_job, name='view_job'),
    path('download_pdf/<int:job_id>/', views.download_pdf, name='download_pdf'),
    path('register/', views.register, name='register'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)