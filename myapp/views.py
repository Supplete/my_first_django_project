
from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import SparePart
from .forms import SparePartForm
from django.core.mail import send_mail
from .models import Customer, Vehicle, Booking
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from .models import Booking
from reportlab.lib.pagesizes import A4
from django.http import HttpResponseForbidden
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import user_passes_test
from .models import ContactMessage
from django.contrib import messages as django_messages
from .models import ContactMessage, MessageReply
from .forms import ReplyForm
from django.core.mail import send_mail
from django.conf import settings




# Create your views here.


def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def customers(request):
    return render(request, 'customers.html')

def spareparts(request):
    return render(request, 'spareparts.html')
def contact(request):
    return render(request, 'contact.html')


# Bookings page view
def bookings(request):
    if request.method == 'POST':
        # CUSTOMER INFO
        name = request.POST['customerName']
        email = request.POST['customerEmail']
        phone = request.POST['customerPhone']
        location = request.POST['customerLocation']
        customer, created = Customer.objects.get_or_create(email=email, defaults={'name': name, 'phone': phone, 'location': location})

        # VEHICLE INFO
        make_model = request.POST['vehicleMake']
        registration = request.POST['vehicleReg']
        vehicle_photo = request.FILES['vehiclePhoto']
        vehicle = Vehicle.objects.create(owner=customer, make_model=make_model, registration=registration, photo=vehicle_photo)

        # BOOKING INFO
        service_type = request.POST['serviceType']
        preferred_date = request.POST['serviceDate']
        preferred_time = request.POST['serviceTime']
        Booking.objects.create(customer=customer, vehicle=vehicle, service_type=service_type, preferred_date=preferred_date, preferred_time=preferred_time)

        return redirect('/bookings/')  # redirect after submission

    return render(request, 'bookings.html')


# VEHICLES PAGE
def vehicles(request):
    vehicles_list = Vehicle.objects.all().order_by('-last_service')
    return render(request, 'vehicles.html', {'vehicles': vehicles_list})



# Decorator to allow only staff
staff_required = user_passes_test(lambda u: u.is_staff)

# -------------------- USER VIEW --------------------
def spareparts_catalog(request):
    # Only show in-stock spare parts to customers
    spareparts = SparePart.objects.filter(in_stock=True)
    return render(request, 'spareparts.html', {'spareparts': spareparts})

# -------------------- ADMIN VIEW --------------------
@staff_required
def spareparts_admin(request):
    # Admin sees all spare parts
    spareparts = SparePart.objects.all()
    return render(request, 'spareparts_admin.html', {'spareparts': spareparts})

# -------------------- ADMIN CRUD --------------------
@staff_required
def add_sparepart(request):
    if request.method == 'POST':
        form = SparePartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('spareparts_admin')
    else:
        form = SparePartForm()
    return render(request, 'sparepart_form.html', {'form': form, 'title': 'Add Spare Part'})

@staff_required
def edit_sparepart(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        form = SparePartForm(request.POST, request.FILES, instance=part)
        if form.is_valid():
            form.save()
            return redirect('spareparts_admin')
    else:
        form = SparePartForm(instance=part)
    return render(request, 'sparepart_form.html', {'form': form, 'title': 'Edit Spare Part'})

@staff_required
def delete_sparepart(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        part.delete()
        return redirect('spareparts_admin')
    return render(request, 'sparepart_confirm_delete.html', {'part': part})


def admin_inbox(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed here")

    messages = ContactMessage.objects.order_by('-sent_at')

    return render(request, 'admin_inbox.html', {
        'messages': messages
    })


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )
            django_messages.success(request, "Your message has been sent!")
            return redirect('contact')
        else:
            django_messages.error(request, "Please fill all fields.")

    return render(request, 'contact.html')




@user_passes_test(lambda u: u.is_staff)
def admin_inbox(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_inbox.html', {'messages_list': messages_list})

@user_passes_test(lambda u: u.is_staff)
def delete_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    django_messages.success(request, "Message deleted successfully.")
    return redirect('admin_inbox')

@user_passes_test(lambda u: u.is_staff)
def reply_message(request, pk):
    contact_msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.contact_message = contact_msg
            reply.admin = request.user
            reply.save()

            # optional: send email to user
            send_mail(
                  subject="Reply to your message",
                  message=reply_text, # type: ignore
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[contact_msg.email],
                  fail_silently=False,
               )


            contact_msg.is_read = True
            contact_msg.save()

            django_messages.success(request, "Reply sent successfully.")
            return redirect('admin_inbox')
    else:
        form = ReplyForm()

    return render(request, 'reply_message.html', {
        'form': form,
        'contact_msg': contact_msg,
    })


def customers_page(request):
    search_query = request.GET.get('search', '').strip()

    # Get all bookings
    bookings = Booking.objects.all()

    # Filter by search query if provided
    if search_query:
        bookings = bookings.filter(
            customer__user__first_name__icontains=search_query
        ) | bookings.filter(
            customer__user__last_name__icontains=search_query
        ) | bookings.filter(
            customer__user__email__icontains=search_query
        )

    # Build unique customers list
    customers = {}
    for b in bookings:
        key = b.customer.user.id
        if key not in customers:
            customers[key] = {
                "id": key,
                "name": b.customer.user.get_full_name(),
                "email": b.customer.user.email,
                "phone": b.customer.phone,
                "address": b.customer.address,
                "bookings_count": 1
            }
        else:
            customers[key]["bookings_count"] += 1

    customers_list = list(customers.values())

    # Pagination: 10 customers per page
    paginator = Paginator(customers_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "customers.html", {
        "page_obj": page_obj,
        "search_query": search_query
    })
def customer_bookings(request, customer_id):
    # Get all bookings of this customer
    bookings = Booking.objects.filter(customer__user__id=customer_id)

    customer_name = bookings.first().customer.user.get_full_name() if bookings else "Unknown Customer"

    return render(request, "customer_bookings.html", {
        "bookings": bookings,
        "customer_name": customer_name
    })

