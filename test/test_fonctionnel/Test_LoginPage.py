import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

@pytest.fixture
def user_data():
    # Créer un utilisateur pour les tests
    return {
        'username': 'john',
        'password': 'password',
    }

@pytest.fixture
def authenticated_client(user_data):
    # Créer un utilisateur et l'authentifier
    user = User.objects.create_user(**user_data)
    client = Client()
    client.login(**user_data)
    return client

@pytest.mark.django_db
def test_login_page(authenticated_client):
    # Envoyer une requête POST avec les données de connexion
    response = authenticated_client.post(reverse('login_page'), {
        'username': 'john',
        'password': 'password',
    })

    # Vérifier si l'utilisateur est authentifié et redirigé vers la page d'accueil
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert response.wsgi_request.user.is_authenticated
