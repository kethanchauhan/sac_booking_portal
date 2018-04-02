from django.views.generic import View
from django.shortcuts import render, redirect
from .models import InstituteBody, SacRoom, Booking
import datetime
import dateutil.parser
import requests
import json


TOKEN_URL = "https://gymkhana.iitb.ac.in/sso/oauth/token/"
USER_DATA_URL = "https://gymkhana.iitb.ac.in/sso/user/api/user/?fields=first_name,last_name,roll_number,insti_address"

client_id = "enqQGWG4g57DbnsZTfbJcvC6rTttmYfXfuKT7xEk"
client_secret = "xltPR806eJhBoRUx8XBW8MqGQXir9jlcl0Ewa3uxOuf4kKAbCvWAI1JjUw45L4i1qqkpuMUTjGPWwVeOSwVNazbX885j6zMD2eta5mLj8ZOSPOPKy2oZ2yi4agoaINRi"

base64_value = "ZW5xUUdXRzRnNTdEYm5zWlRmYkpjdkM2clR0dG1ZZlhmdUtUN3hFazp4bHRQUjgwNmVKaEJvUlV4OFhCVzhNcUdRWGlyOWpsY2wwRXdhM3V4T3VmNGtLQWJDdldBSTFKalV3NDVMNGkxcXFrcHVNVVRqR1BXd1ZlT1N3Vk5hemJYODg1ajZ6TUQyZXRhNW1MajhaT1NQT1BLeTJvWjJ5aTRhZ29hSU5SaQ=="



class Home(View):
    def get(self, request):
        if not "user_id" in request.session:
            return redirect('/login')
        return redirect('/booking/room_book/')


class Login(View):
    def get(self, request):
        context = {}
        print("request_data", request.body)
        if "user_id" in request.session:
            return redirect('/booking/room_book/')

        if "access_token" in request.GET:
            response = request.GET
            if 'user_id' in request.session:
                print("user_id", request.session['user_id'])
            else:
                user = InstituteBody(
                    access_token=response['access_token']
                )
                auth_token = "Bearer " + user.access_token
                headers = {"Authorization": auth_token}

                r = requests.get(USER_DATA_URL, headers=headers, verify=False)
                print(r.content)
                data = json.loads(r.content.decode('utf-8'))
                print("sso_data", data)
                if InstituteBody.objects.filter(roll_number=data['roll_number']).exists():
                    new_user = InstituteBody.objects.get(roll_number=data['roll_number'])
                    new_user.access_token = user.access_token
                    new_user.save()
                    user = new_user

                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.roll_number = data['roll_number']
                user.hostel_name = data["insti_address"]["hostel_name"]
                user.room_no = data["insti_address"]["room"]
                user.save()
                request.session['user_id'] = user.pk
                return redirect('/booking/room_book/')

        return render(request, 'login.html', context)


class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect('/')


class Register(View):
    def get(self, request):
        context = {}
        if not "user_id" in request.session:
            return redirect('/')
        context["verification_emails"] = ['kethan88@gmail.com', 'sysadh06@iitb.ac.in']
        return render(request, 'registration.html', context)

    def post(self, request):
        if not "user_id" in request.session:
            return redirect('/')
        response = request.POST
        context = {}
        institute_body = InstituteBody.objects.get(pk = request.session["user_id"])
        if institute_body.registered == False:
            institute_body.body_name = response.get("institute_body")
            institute_body.contact_number = response.get("contact_number")
            institute_body.verification_email = response.get("verification_email")
            institute_body.registered = True
            institute_body.save()
            context["message"] = "you have been registered, wait for the verification"
        else:
            context["message"] = "you have already registered"
        context["verification_emails"] = ['kethan88@gmail.com', 'sysadh06@iitb.ac.in']
        return render(request, 'registration.html', context)


class RoomBook(View):
    def get(self, request):
        context = {}
        if not "user_id" in request.session:
            return redirect('/')
        context["sac_rooms"] = SacRoom.objects.all()
        return render(request, 'room_book.html', context)

    def post(self, request):
        if not "user_id" in request.session:
            return redirect('/')
        institute_body = InstituteBody.objects.get(pk=request.session["user_id"])
        if institute_body.verified:
            response = request.POST
            sac_room = SacRoom.objects.get(name=response["sac_room"])
            bookings = Booking.objects.filter(sac_room=sac_room)
            start_date = dateutil.parser.parse(response.get("start_date")).date()
            end_date = dateutil.parser.parse(response.get("end_date")).date()
            if start_date <= end_date and start_date >= datetime.datetime.now().date():
                for booking in bookings:
                    if start_date > booking.end_date:
                        print("enter_start_if")
                        pass
                    elif end_date < booking.start_date:
                        print("enter_end_if")
                        pass
                    else:
                        print("enter_else")
                        context = {}
                        context["message"] = "Conflicts Occured"
                        context["sac_rooms"] = SacRoom.objects.all()
                        return render(request, 'room_book.html', context)
            else:
                print("enter_outer_else")
                context = {}
                context["message"] = "Conflicts Occured"
                context["sac_rooms"] = SacRoom.objects.all()
                return render(request, 'room_book.html', context)
            institute_body = InstituteBody.objects.get(pk=request.session["user_id"])
            booking = Booking(
                sac_room=sac_room,
                booked_by=institute_body,
                start_date=response.get("start_date"),
                end_date=response.get("end_date")
            )
            booking.save()
        else:
            context = {}
            context["sac_rooms"] = SacRoom.objects.all()
            context["message"] = "the account must be verified by Gsecs in order to continue"
            return render(request, 'room_book.html', context)
        return redirect('/booking/my_bookings/')


class MyBookings(View):
    def get(self, request):
        context = {}
        if not "user_id" in request.session:
            return redirect('/')
        institute_body = InstituteBody.objects.get(pk=request.session["user_id"])
        context["bookings"] = Booking.objects.filter(booked_by=institute_body).order_by('-start_date')
        print(context["bookings"])
        return render(request, 'my_bookings.html', context)


class CheckAvailability(View):
    def get(self, request):
        if not "user_id" in request.session:
            return redirect('/')
        sac_rooms = SacRoom.objects.all()
        context = {}
        context["sac_rooms"] = sac_rooms
        return render(request, 'check_availabilty.html', context)
    def post(self, request):
        if not "user_id" in request.session:
            return redirect('/')
        response = request.POST
        sac_room = SacRoom.objects.get(name= response.get("sac_room"))
        context = {}
        context["bookings"] = Booking.objects.filter(sac_room = sac_room).filter(start_date__gte=datetime.datetime.now().date())
        sac_rooms = SacRoom.objects.all()
        context["sac_rooms"] = sac_rooms
        return render(request, 'check_availabilty.html', context)
