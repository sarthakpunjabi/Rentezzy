"""This holds the handler for every request to the rentezzy application."""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from palladium.settings import EMAIL_HOST_USER
from .forms import RoomForm
from . import callback, observable, models, factory, decorators, singleton

logger = singleton.Logger().get_logger()

target_class = callback
call_backs = [callback.notify_user, callback.update_price]
o = observable.Observable()
for cb in call_backs:
    o.subscribe(cb)


def search_rooms(request):
    '''
    Search rooms function
    '''
    if request.method == 'POST':
        logger.info("Searching for room")
        county = request.POST.get("county")
        room_obj = models.Rooms.objects.get_available_rooms(county)
        if room_obj:
            return render(request, 'home/search.html', {"rooms": room_obj})
        else:
            room_obj = models.Rooms.objects.all()
            return render(request, 'home/search.html', {"rooms": room_obj})
      
@login_required
def detail_room(request, room_id):
    """
    Details page with dynamic url
    """
    if request.method == 'GET':
        logger.info("Searching for room")
        room = models.Rooms.objects.get(id=room_id)
        images = [room.img1.url,room.img2.url,room.img3.url]
        return render(request,'home/detailroom.html',{"room":room,"images":images})
    return HttpResponseRedirect("search_room")

@login_required
@decorators.validate_user(user=["CUSTOMER"], redirect_url="search_room")
def delete_room(request):
    """
    It deletes the room, added by the owner / agent.
    The user of this request should not be a Customer.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Owner / Agent.
    Request Type - POST
    """
    if request.method == "POST":
        logger.info("Deleting a room")
        room_id = request.POST.get("id")
        models.Rooms.objects.update_room_status(room_id, "DELETED")
        return HttpResponseRedirect("search_room")
    return HttpResponseRedirect("search_room")


@login_required
@decorators.validate_user(user=["CUSTOMER"], redirect_url="search_room")
def add_room(request):
    """
    Only Agent and Owner can add the room, with the current user default is of Customer Type.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Agent / Owner.
    Request Type - POST
    """
    if request.method == "POST":
        logger.info("Adding a room")
        request_details = {
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
            "eir_code": request.POST.get("eir_code"),
            "address": request.POST.get("address"),
            "county": request.POST.get("county"),
            "contract_details":request.POST.get("contract_details"),
            "monthly_rent_amount": request.POST.get("monthly_rent_amount"),
            "deposit_amount": request.POST.get("deposit_amount"),
            "image_url":request.POST.get("image_url"),
            "img1":request.POST.get("img1"),
            "img2":request.POST.get("img2"),
            "img3":request.POST.get("img3"),
            "status": request.POST.get("status"),
            "property_age": request.POST.get("property_age"),
        }

        if not factory.ValidatorFactory().validate(request_details):
            logger.error("Error in add_room data validation")
            return HttpResponse("Failed")

        models.Rooms.objects.add_room(request_details, request.user)
        return HttpResponseRedirect("search_room")
    else:
        forms = RoomForm()
        return render(request,"roles/add.html",{"form":forms})

@login_required
@decorators.validate_user(user=["AGENT", "OWNER"], redirect_url="search_room")
def book_room(request):
    """
    It books the room for the customer.
    The user should only be of type CUSTOMER, and not of type Agent / Owner.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Customer.
    Request Type - POST
    """
    if request.method == "POST":
        logger.info("Booking a room")
        # Mark room as Booked
        room_id = request.POST.get("id")
        room_obj = models.Rooms.objects.update_room_status(room_id, "BOOKED")
        logger.info("Successfully Updated the status of the room")

        # Payment for Booking Room
        # Taking dummy data for payment.
        payment_method = request.POST.get("payment")
        payment_details = {
            "type": payment_method,
            "user": request.user,
            "price": room_obj.deposit_amount,
            "amount": room_obj.deposit_amount,
            "currency": "EURO",
        }
        payment_obj = factory.PaymentFactory()
        # dummy_flag in pay func determines the response from payment gateway,
        # it is by default success.
        resp = payment_obj.choose_operator(payment_details).pay()
        # resp = payment_obj.choose_operator(payment_details).pay(False)

        payment = models.Payments.objects.create_payment(resp)
        if resp.get("status") == "success":
            logger.info("Successfully made the payment for booking room")
            # Update Booking Model, for time being, update with dummy data.
            models.Rooms.objects.subtract_amount(resp.get("amt_received"), room_obj)
            models.Booking.objects.create_booking(payment, room_obj, request.user)
        else:
            # Revert Status of Rooms
            logger.info("Failed to make the payment reverting the status of the room")
            models.Rooms.objects.update_room_status(room_id, "AVAILABLE")
            logger.info("Successfully reverted the status of the room")
        return JsonResponse(resp, safe=False)


@login_required
def contact_room(request,room_id):
    """
    Contacting agent and owner
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        forroom = models.Rooms.objects.get(id=room_id)

        try:
            mail = EmailMessage(forroom.address, description,
             EMAIL_HOST_USER,
             [forroom.room_details.enquiry_email]
            )
            mail.send()
            con = models.Contact(full_name=name,
            email=email,
            phone_number=phone,
            Description=description
            )
            con.save()
            return redirect('/')
        except:
            return HttpResponse("done")
    else:
        return render(request,'home/enquire.html')

   


@login_required
@decorators.validate_user(user=["AGENT", "OWNER"], redirect_url="search_room")
def cancel_booking(request):
    """
    It cancels the room booked by the CUSTOMER.
    Preconditions - 1. The start date of the room should not have elasped the current date.
    Only Customer can cancel the booking of the room.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Customer.
    Request Type - POST
    """
    if request.method == "POST":
        logger.info("Cancel a room")

        room_id = request.POST.get("id")

        # Do a validation Check
        if not factory.ValidatorFactory().validate_cancel_booking(room_id):
            logger.error("Error in add_room data validation")
            return HttpResponse("Failed")

        # Mark room as Cancelled or Available Again
        room_obj = models.Rooms.objects.update_room_status(room_id, "AVAILABLE")
        if not room_obj:
            logger.error("Error updating room status")
            return HttpResponse("Failed")
        logger.info("Successfully Updated the status of the room")

        # Add cancellation date in booking
        booking_obj = models.Booking.objects.cancel_booking(room_obj)
        if not booking_obj:
            logger.error("Error in cancellation of booking")
            return HttpResponse("Failed")

        # Revert Room total_amount
        # We could have reverted the payment status from booking itself,
        # but since we are mocking the payment flow, so kept it as a different method.
        models.Rooms.objects.subtract_amount(-room_obj.total_amount, room_obj)

        # Revert Payment Status to Returned
        models.Payments.objects.update_payment_status(booking_obj.payments.orderId, "Returned")
        return HttpResponse("success")
    return HttpResponseRedirect("search_room")


@login_required
@decorators.validate_user(user=["AGENT", "OWNER"], redirect_url="search_room")
def get_booked_room(request):
    """
    It fetches the list of booked room by the user.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Customer.
    Request Type - GET
    """
    if request.method == "GET":
        logger.info("In Fetching Booked Room")
        booked_rooms = models.Booking.objects.fetch_bookings(request.user)
        return render(request, 'home/index.html', {"booked_rooms": booked_rooms})
    return HttpResponseRedirect("search_room")


@login_required
@decorators.validate_user(user=["CUSTOMER", "OWNER"], redirect_url="search_room")
def get_agent_commission(request):
    """
    It calculates the agent commission for their sales.
    Only agent can make this request.
    PreConditions - 1. User should be logged In.
                    2. User should be of type Agent.
    Request Type - POST
    """
    if request.method == "GET":
        rooms = models.Rooms.objects.get_agent_bookings(request.user)
        total_commission = factory.AgentCommissionFactory(). \
            calculate_commission(request.user.level, rooms)
        return JsonResponse(total_commission, safe=False)
    return HttpResponseRedirect("search_room")


def add_discount(request):
    """
    It's a batch job running for adding the discounts.
    On rooms not rented for long time.
    """
    observer = observable.Observable()
    observer.notify()
    return HttpResponse("Success")
