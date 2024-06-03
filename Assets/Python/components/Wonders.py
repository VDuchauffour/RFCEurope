from CoreFunctions import city
from CoreTypes import Specialist
from PyUtils import rand


def leaning_tower_effect():
    iGP = rand(7)
    pFlorentia = city(54, 32)
    iSpecialist = Specialist.GREAT_PROPHET + iGP
    pFlorentia.setFreeSpecialistCount(iSpecialist, 1)
