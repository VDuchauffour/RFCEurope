import Barbs
from Core import civilizations, location, player, plot
from CoreTypes import Building, Improvement
from Events import handler
from RFCUtils import getUniqueBuilding, spreadMajorCulture
import CvEventManager


@handler("cityBuilt")
def spread_culture(city):
    iOwner = city.getOwner()
    if iOwner < civilizations().majors().len():
        spreadMajorCulture(iOwner, city.getX(), city.getY())


@handler("cityBuilt")
def remove_minor_cultures(city):
    # Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
    for civ in civilizations().minors().ids():
        plot(city).setCulture(civ, 0, True)


@handler("cityBuilt")
def free_building_when_city_built_over_improvement(city):
    # Absinthe: Free buildings if city is built on a tile improvement
    # The problem is that the improvement is auto-destroyed before the city is founded, and totally separately from this function,
    # thus a workaround is needed
    # Solution: getting the coordinates of the last destroyed improvement from a different file in a global variable
    # If the last destroyed improvement in the game is a fort, and it was in the same place as the city, then it's good enough for me
    # (only problem might be if currently there is no improvement on the city-founding tile, but the last destroyed improvement in the game
    # was a fort on the exact same plot some turns ago - but IMO that's not much of a stress of reality, there was a fort there after all)
    # Note that CvEventManager.iImpBeforeCity needs to have some initial value if a city is founded before the first destroyed improvement
    # adding an improvement in the scenario map to one of the preplaced Byzantine cities won't work perfectly:
    # while the improvement will be autorazed on the beginning of the 1st players turn when starting in 500AD, does nothing if you load a saved game

    iOwner = city.getOwner()
    tCity = (city.getX(), city.getY())
    iImpBeforeCityType = (CvEventManager.iImpBeforeCity / 10000) % 100
    iImpBeforeCityX = (CvEventManager.iImpBeforeCity / 100) % 100
    iImpBeforeCityY = CvEventManager.iImpBeforeCity % 100
    # Absinthe: free walls if built on fort
    if iImpBeforeCityType == Improvement.FORT and (iImpBeforeCityX, iImpBeforeCityY) == tCity:
        city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.WALLS), True)
    # Absinthe: free granary if built on hamlet
    if iImpBeforeCityType == Improvement.HAMLET and (iImpBeforeCityX, iImpBeforeCityY) == tCity:
        city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.GRANARY), True)
    # Absinthe: free granary and +1 population if built on village or town
    if iImpBeforeCityType in [Improvement.TOWN, Improvement.VILLAGE]:
        if (iImpBeforeCityX, iImpBeforeCityY) == tCity:
            city.changePopulation(1)
            city.setHasRealBuilding(getUniqueBuilding(iOwner, Building.GRANARY), True)


@handler("cityBuilt")
def free_food_on_city_built(city):
    # Absinthe: Some initial food for all cities on foundation
    # So Leon and Roskilde for example don't lose a population in the first couple turns
    # Nor the indy cities on spawn (they start with zero-sized culture, so they shrink without some food reserves)
    # Currently 1/5 of the treshold of the next population growth
    city.setFood(city.growthThreshold() / 5)


@handler("unitPillage")
def spawn_barbs_when_pillage_cottage(pUnit, iImprovement, iRoute, iOwner):
    if plot(pUnit).countTotalCulture() == 0:
        if Improvement.COTTAGE <= iImprovement <= Improvement.TOWN:
            Barbs.onImprovementDestroyed(location(pUnit))


@handler("unitPillage")
def reduce_stability_with_pillage(pUnit, iImprovement, iRoute, iOwner):
    # TODO only when same religion?
    # TODO make announce?
    owner = pUnit.getOwner()
    if owner > -1 and owner < civilizations().majors().len():
        pPlayer = player(owner)
        pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 2)
