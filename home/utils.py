from datetime import date
from .models import Hotel

hotel1 = Hotel(
    nom="Hotel Villa",
    date_ouverture=date(2023, 5, 1),
    date_fermeture=date(2023, 10, 31)
)

hotel1.save()

hotel2 = Hotel(nom="Hotel room top",
               date_ouverture=date(2023, 6, 1),
               date_fermeture=date(2023, 9, 30))

hotel2.save()
