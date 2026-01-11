from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('bookings/', views.bookings, name='bookings'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('customers/', views.customers, name='customers'),
    path('spareparts/', views.spareparts_catalog, name='spareparts_catalog'),  # Customer view
    path('dashboard/inbox/reply/<int:pk>/', views.reply_message, name='reply_message'),
     path('contact/', views.contact, name='contact'),
    path('dashboard/inbox/', views.admin_inbox, name='admin_inbox'),
    path('dashboard/inbox/delete/<int:pk>/', views.delete_message, name='delete_message'),
    path("customers/<int:customer_id>/bookings/", views.customer_bookings, name="customer_bookings"),


 # Admin spare parts CRUD
    path('dashboard/spareparts/', views.spareparts_admin, name='spareparts_admin'),
    path('dashboard/spareparts/add/', views.add_sparepart, name='add_sparepart'),
    path('dashboard/spareparts/edit/<int:pk>/', views.edit_sparepart, name='edit_sparepart'),
    path('dashboard/spareparts/delete/<int:pk>/', views.delete_sparepart, name='delete_sparepart'),



]

# Serve static & media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
