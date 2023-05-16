from django.urls import path
from .views import check_booking
from .views import home
from .views import login_page
from .views import register_page
from .views import logout_view
from .views import hotel_detail
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_booking/', check_booking),
    path('', home, name='home'),
    path('hotel-detail/<uid>/', hotel_detail, name="hotel_detail"),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_view, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
