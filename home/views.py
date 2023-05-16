
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (Amenities, Hotel, HotelBooking)
from django.db.models import Q
from django.contrib.auth import logout
from datetime import datetime


def check_booking(start_date, end_date, uid, room_count):
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid=uid,
    )
    if len(qs) >= room_count:
        return False
    return True


def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')

    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains=search) |
            Q(description__icontains=search)
        )

    if len(amenities):
        hotels_objs = hotels_objs.filter(
            amenities__amenity_name__in=amenities
        ).distinct()

    context = {
        'amenities_objs': amenities_objs,
        'hotels_objs': hotels_objs,
        'sort_by': sort_by,
        'search': search,
        'amenities': amenities
    }
    return render(request, 'home.html', context)


def hotel_detail(request, uid):
    hotel_obj = Hotel.objects.get(uid=uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')

        hotel = Hotel.objects.get(uid=uid)
        if not check_booking(checkin, checkout, uid, hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(
            hotel=hotel,
            user=request.user,
            start_date=checkin,
            end_date=checkout,
            booking_type='Pre Paid'
        )

        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'hotel_detail.html', {'hotel_obj': hotel_obj})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            messages.warning(request, 'Invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request, user_obj)
        return redirect('/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def recherche_hotels(request):
    check_in = request.GET.get('debut')  # date de début de la recherche
    check_out = request.GET.get('fin')  # date de fin de la recherche

    # Convertir les dates en objets datetime
    check_in = datetime.strptime(check_in, '%Y-%m-%d')
    check_out = datetime.strptime(check_out, '%Y-%m-%d')

    # Récupérer les hôtels qui sont ouverts pendant la période de recherche
    hotels = Hotel.objects.filter(
        date_ouverture__lte=check_out,
        date_fermeture__gte=check_in
    )
    # Rendre le template avec les hôtels trouvés
    context = {'hotels': hotels}
    return render(request, 'home.html', context)
