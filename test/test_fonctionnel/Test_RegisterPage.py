import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.test import Client
from django.contrib.auth.models import User
client = Client()

@pytest.mark.django_db
def test_register_with_good_data(client):
    form_data = {'username': 'Kevin', 'password': 'AZERTY05'}
    response = client.post(reverse('register_page'), data=form_data)
    assert response.status_code == 302
    assert response.url == reverse('home')



# Test de création d'un nouvel utilisateur avec un nom d'utilisateur déjà existant
@pytest.mark.django_db
def test_register_existing_username(client):
    # Créer un utilisateur avec le même nom d'utilisateur
    User.objects.create(username='Kevin')

    # Envoyer une requête POST avec les mêmes informations d'utilisateur
    form_data = {'username': 'Kevin', 'password': 'AZERTY05'}
    response = client.post(reverse('register_page'), data=form_data)

    # Vérifier que le message d'avertissement est affiché
    storage = get_messages(response.wsgi_request)
    messages = [m.message for m in storage]
    assert 'Username already exists' in messages



# # Test de création d'un nouvel utilisateur avec un mot de passe trop court
# @pytest.mark.django_db
# def test_register_short_password(client):
#     form_data = {'username': 'Kevin', 'password': 'abc'}
#     response = client.post(reverse('register_page'), data=form_data)
#     assert response.status_code == 302
    

