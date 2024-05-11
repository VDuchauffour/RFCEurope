from CoreStructures import make_units
from CoreTypes import Unit


def ottoman_invasion(iCiv, tPlot):
    # Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
    make_units(iCiv, Unit.LONGBOWMAN, tPlot, 2)
    make_units(iCiv, Unit.MACEMAN, tPlot, 2)
    make_units(iCiv, Unit.KNIGHT, tPlot, 3)
    make_units(iCiv, Unit.TURKEY_GREAT_BOMBARD, tPlot, 2)
    make_units(iCiv, Unit.ISLAMIC_MISSIONARY, tPlot, 2)
