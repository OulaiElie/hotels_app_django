
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (Amenities, Hotel, HotelBooking)
from django.db.models import Q
from django.contrib.auth import logout
from datetime import datetime


# Cette fonction vérifie si une réservation est possible pour les dates données
    # pour l'hôtel donné (représenté par son uid) et pour le nombre de chambres spécifié
    # en vérifiant si des réservations existent déjà pour ces dates

def check_booking(start_date  , end_date ,uid , room_count):

    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid,
       
        
        )
     # Si le nombre de réservations existantes est supérieur ou égal au nombre de chambres spécifié,
    # alors une nouvelle réservation n'est pas possible et la fonction retourne False.
    if len(qs) >= room_count:
        return False
     # Sinon, une nouvelle réservation est possible et la fonction retourne True.
    return True

 # Cette fonction affiche la page d'accueil avec tous les hôtels et leurs équipements
    # disponibles. Elle permet également de trier les hôtels par prix et de filtrer les résultats
    # en fonction d'une chaîne de recherche et/ou d'équipements spécifiques sélectionnés par l'utilisateur.
    
def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    # Si un tri est spécifié, les hôtels sont triés par prix croissant ou décroissant
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        # Si une chaîne de recherche est spécifiée, les hôtels sont filtrés pour correspondre
        # à la chaîne de recherche.
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
         # Si des équipements sont spécifiés, les hôtels sont filtrés pour correspondre à ces équipements.
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()


 # Les hôtels et les équipements sont transmis au template pour affichage.
    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities}
    return render(request , 'home.html' ,context)



def hotel_detail(request,uid):
     # Cette fonction affiche les détails de l'hôtel sélectionné (représenté par son uid)
    # et permet également de réserver une chambre pour une période de dates spécifiée.
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
         # Si la demande est une demande POST, cela signifie qu'un utilisateur a soumis un formulaire
        # pour réserver une chambre à l'hôtel sélectionné.
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        # La fonction check_booking() est appelée pour vérifier si la réservation est possible pour les
        # dates et le nombre de chambres spécifiés. Si
        hotel = Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('/')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def recherche_hotels(request):
    Check_in = request.GET.get('debut') # date de début de la recherche
    Check_out= request.GET.get('fin') # date de fin de la recherche
    

    # Convertir les dates en objets datetime
    Check_in = datetime.strptime(Check_in, '%Y-%m-%d')
    Check_out = datetime.strptime(Check_out, '%Y-%m-%d')

    # Récupérer les hôtels qui sont ouverts pendant la période de recherche
    hotels = Hotel.objects.filter(date_ouverture__lte=Check_out, date_fermeture__gte=Check_in)

    # Renderiser le template avec les hôtels trouvés
    context = {'hotels': hotels}
    return render(request, 'home.html', context)
