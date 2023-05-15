import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from home.models import Hotel, HotelBooking

@pytest.fixture
def user_data():
    # Créer un utilisateur pour les tests
    return {
        'username': 'john',
        'password': 'password',
    }

@pytest.fixture
def hotel_data():
    # Créer un hôtel pour les tests
    return {
        'hotel_name': 'Test Hotel',
        'room_count': 10,
        'hotel_price':10000
        # ... Ajoutez d'autres champs d'hôtel si nécessaire
    }

@pytest.fixture
def authenticated_client(user_data):
    # Créer un utilisateur et l'authentifier
    # user = User.objects.create_user(**user_data)
    client = Client()
    client.login(**user_data)
    return client

@pytest.fixture
def hotel_booking_data(hotel_data, user_data):
    # Créer une réservation d'hôtel pour les tests
    start_date = date.today() + timedelta(days=7)
    end_date = start_date + timedelta(days=7)
    hotel = Hotel.objects.create(**hotel_data)
    user = User.objects.create_user(**user_data)
    return {
        'hotel': hotel,
        'user': user,
        'start_date': start_date,
        'end_date': end_date,
        'booking_type': 'Pre Paid',
    }

@pytest.mark.django_db
def test_hotel_detail_view(authenticated_client, hotel_booking_data):
    # Appeler la vue de détails de l'hôtel avec une demande GET
    response = authenticated_client.get(reverse('hotel_detail', args=[hotel_booking_data['hotel'].uid]))

    # Vérifier que la réponse est réussie et contient les détails de l'hôtel
    assert response.status_code == 200
    assert hotel_booking_data['hotel'].hotel_name in response.content.decode()

    # Envoyer une demande POST pour créer une réservation
    checkin = hotel_booking_data['start_date'].strftime('%Y-%m-%d')
    checkout = hotel_booking_data['end_date'].strftime('%Y-%m-%d')
    response = authenticated_client.post(reverse('hotel_detail', args=[hotel_booking_data['hotel'].uid]), {
        'checkin': checkin,
        'checkout': checkout,
    })

    # Vérifier que la réservation a été créée avec succès
    assert response.status_code == 302
    assert HotelBooking.objects.filter(hotel=hotel_booking_data['hotel'], user=hotel_booking_data['user']).exists()
    