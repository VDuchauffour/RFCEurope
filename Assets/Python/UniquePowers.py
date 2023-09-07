# Rhye's and Fall of Civilization: Europe - Unique Powers (only a couple of them is here, most are handled in the .dll)

from CvPythonExtensions import *
import PyHelpers

# import cPickle as pickle
import Consts as con
import XMLConsts as xml
import Religions
import RFCUtils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
religion = Religions.Religions()

iJanissaryPoints = con.iJanissaryPoints


class UniquePowers:
    def checkTurn(self, iGameTurn):
        pass

    # Absinthe: Arabian UP
    def faithUP(self, iPlayer, city):
        pFaithful = gc.getPlayer(iPlayer)
        iStateReligion = pFaithful.getStateReligion()
        iTemple = 0
        # Absinthe: shouldn't work on minor religions, to avoid exploit with spreading Judaism this way
        if 0 <= iStateReligion <= 3:
            if not city.isHasReligion(iStateReligion):
                city.setHasReligion(iStateReligion, True, True, False)
                pFaithful.changeFaith(1)

            if iStateReligion == 0:
                iTemple = xml.iProtestantTemple
            elif iStateReligion == 1:
                iTemple = xml.iIslamicTemple
            elif iStateReligion == 2:
                iTemple = xml.iCatholicTemple
            elif iStateReligion == 3:
                iTemple = xml.iOrthodoxTemple
            if not city.hasBuilding(iTemple):
                city.setHasRealBuilding(iTemple, True)
                pFaithful.changeFaith(1)

    # Absinthe: Ottoman UP
    def janissaryDraftUP(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iStateReligion = pPlayer.getStateReligion()

        iNewPoints = 0
        for city in utils.getCityList(iPlayer):
            for iReligion in range(xml.iNumReligions):
                if iReligion != iStateReligion and city.isHasReligion(iReligion):
                    iNewPoints += city.getPopulation()
                    break

        iOldPoints = pPlayer.getPicklefreeParameter(iJanissaryPoints)

        iNextJanissary = 200
        if pPlayer.isHuman():
            iNextJanissary = 300

        iTotalPoints = iOldPoints + iNewPoints
        while iTotalPoints >= iNextJanissary:
            # tCity = religion.selectRandomCityCiv(iPlayer)
            # utils.makeUnit( xml.iJanissary, iPlayer, tCity, 1 )
            pCity = utils.getRandomCity(
                iPlayer
            )  # The Janissary unit appears in a random city - should it be the capital instead?
            if pCity != -1:
                iX = pCity.getX()
                iY = pCity.getY()
                utils.makeUnit(xml.iJanissary, iPlayer, (iX, iY), 1)
                # interface message for the human player
                if iPlayer == utils.getHumanID():
                    CyInterface().addMessage(
                        iPlayer,
                        False,
                        con.iDuration,
                        CyTranslator().getText("TXT_KEY_UNIT_NEW_JANISSARY", ())
                        + " "
                        + pCity.getName()
                        + "!",
                        "AS2D_UNIT_BUILD_UNIQUE_UNIT",
                        0,
                        gc.getUnitInfo(xml.iJanissary).getButton(),
                        ColorTypes(con.iGreen),
                        iX,
                        iY,
                        True,
                        True,
                    )
                print(" New Janissary in ", pCity.getName())
                iTotalPoints -= iNextJanissary

        pPlayer.setPicklefreeParameter(iJanissaryPoints, iTotalPoints)

    def janissaryNewCityUP(self, iPlayer, city, bConquest):
        pPlayer = gc.getPlayer(iPlayer)
        iStateReligion = pPlayer.getStateReligion()
        for iReligion in range(xml.iNumReligions):
            if iReligion != iStateReligion and city.isHasReligion(iReligion):
                iCityPopulation = city.getPopulation()
                # more janissary points on conquest, less on flip and trade
                if bConquest:
                    iJanissaryPoint = iCityPopulation * 9
                else:
                    iJanissaryPoint = iCityPopulation * 4
                iOldPoints = pPlayer.getPicklefreeParameter(iJanissaryPoints)
                pPlayer.setPicklefreeParameter(iJanissaryPoints, iOldPoints + iJanissaryPoint)
                break

        # removed free janissary, probably too powerful to add a new janissary unit right on conquest
        iIsHasForeignReligion = 0
        if iIsHasForeignReligion:
            iX = city.getX()
            iY = city.getY()
            utils.makeUnit(xml.iJanissary, iPlayer, (iX, iY), 1)
            if iPlayer == utils.getHumanID():
                CyInterface().addMessage(
                    iPlayer,
                    False,
                    con.iDuration,
                    CyTranslator().getText("TXT_KEY_UNIT_NEW_JANISSARY", ())
                    + " "
                    + city.getName()
                    + "!",
                    "AS2D_UNIT_BUILD_UNIQUE_UNIT",
                    0,
                    gc.getUnitInfo(xml.iJanissary).getButton(),
                    ColorTypes(con.iGreen),
                    iX,
                    iY,
                    True,
                    True,
                )
                print(" New Janissary in ", city.getName())

    # Absinthe: Danish UP
    def soundUP(self, iPlayer):
        print("Sound dues")
        lSoundCoords = [(60, 57), (60, 58)]

        # Check if we control the Sound
        bControlsSound = False
        for tCoord in lSoundCoords:
            pPlot = gc.getMap().plot(tCoord[0], tCoord[1])
            if pPlot.calculateCulturalOwner() == iPlayer:
                bControlsSound = True
                break
        if not bControlsSound:
            print("No sound dues, sound not controlled")
            return

        iCities = self.getNumForeignCitiesOnBaltic(iPlayer)

        iGold = iCities * 2
        print("We got %d gold." % iGold)
        gc.getPlayer(iPlayer).changeGold(iGold)

        CyInterface().addMessage(
            iPlayer,
            False,
            con.iDuration / 2,
            CyTranslator().getText("TXT_KEY_UP_SOUND_TOLL", (iGold,)),
            "",
            0,
            "",
            ColorTypes(con.iGreen),
            -1,
            -1,
            True,
            True,
        )

    def getNumForeignCitiesOnBaltic(self, iPlayer, bVassal=False):
        lBalticRects = [
            ((56, 52), (70, 57)),
            ((62, 58), (74, 62)),
            ((64, 63), (79, 66)),
            ((64, 67), (71, 72)),
        ]

        # Count foreign coastal cities
        iCities = 0
        for tRect in lBalticRects:
            for (iX, iY) in utils.getPlotList(tRect[0], tRect[1]):
                # print(iX,iY)
                pPlot = gc.getMap().plot(iX, iY)
                if pPlot.isCity():
                    pCity = pPlot.getPlotCity()
                    # print(pCity.getName() + " is a city.")
                    if pCity.isCoastal(5):
                        if not bVassal:
                            if pCity.getOwner() != iPlayer:
                                # print(pCity.getName() + " is a foreign coastal city on the Baltic.")
                                iCities += 1
                        else:
                            iOwner = pCity.getOwner()
                            if iOwner != iPlayer and iOwner != utils.getMaster(iOwner) != iPlayer:
                                iCities += 1
        return iCities

    # Absinthe: Aragonese UP
    def confederationUP(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        capital = pPlayer.getCapitalCity()
        iCapitalX = capital.getX()
        iCapitalY = capital.getY()

        # Collect all provinces
        cityProvinces = []
        for city in utils.getCityList(iPlayer):
            pProvince = city.getProvince()
            cityProvinces.append(pProvince)
        # Calculate unique provinces
        uniqueProvinces = set(cityProvinces)
        iProvinces = len(uniqueProvinces)

        # Note that Aragon do not use any of its UHV counters, so we can safely use them here
        # Do not recalculate if we have the same number of provinces as in the last check, and the capital has not changed
        if (
            iProvinces == pPlayer.getUHVCounter(1)
            and pPlayer.getUHVCounter(2) == 100 * iCapitalX + iCapitalY
        ):
            return

        # Store the province number for the next check
        pPlayer.setUHVCounter(1, iProvinces)

        # On capital change, reset yield for the previous capital's tile, also reset the commerce counter
        if pPlayer.getUHVCounter(2) != 100 * iCapitalX + iCapitalY:
            iOldCapitalX = pPlayer.getUHVCounter(2) / 100
            iOldCapitalY = pPlayer.getUHVCounter(2) % 100
            iProvinceCommerceLastBonus = pPlayer.getUHVCounter(0)
            gc.getGame().setPlotExtraYield(
                iOldCapitalX, iOldCapitalY, 2, -iProvinceCommerceLastBonus
            )
            # If there was a capital change, the discount should be 0 for the new capital's tile
            pPlayer.setUHVCounter(0, 0)
            # New capital's coordinates are stored for the next check
            pPlayer.setUHVCounter(2, 100 * iCapitalX + iCapitalY)

        # Update tile yield for the capital's plot
        iProvinceCommerceLastBonus = pPlayer.getUHVCounter(0)
        gc.getGame().setPlotExtraYield(iCapitalX, iCapitalY, 2, -iProvinceCommerceLastBonus)
        # print("Capital commerce reduced by", iProvinceCommerceLastBonus)
        iProvinceCommerceNextBonus = (
            iProvinces * 2
        )  # <- This number is the amount of extra commerce per province
        gc.getGame().setPlotExtraYield(iCapitalX, iCapitalY, 2, iProvinceCommerceNextBonus)
        # print("Capital commerce increased by", iProvinceCommerceNextBonus)
        # Tile yield is stored for the next check
        pPlayer.setUHVCounter(0, iProvinceCommerceNextBonus)

    # Absinthe: Scottish UP
    def defianceUP(self, iPlayer):
        print("Defiance called")
        pPlayer = gc.getPlayer(iPlayer)

        # One ranged/gun class
        RangedClass = utils.getUniqueUnit(iPlayer, xml.iArcher)
        lRangedList = [
            xml.iLineInfantry,
            xml.iMusketman,
            xml.iLongbowman,
            xml.iArbalest,
            xml.iCrossbowman,
            xml.iArcher,
        ]
        for iUnit in lRangedList:
            if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
                RangedClass = utils.getUniqueUnit(iPlayer, iUnit)
                break

        # One polearm class
        PolearmClass = utils.getUniqueUnit(iPlayer, xml.iSpearman)
        lPolearmList = [xml.iLineInfantry, xml.iPikeman, xml.iGuisarme]
        for iUnit in lPolearmList:
            if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
                PolearmClass = utils.getUniqueUnit(iPlayer, iUnit)
                break

        print("Making ", RangedClass, " and ", PolearmClass)
        for city in utils.getCityList(iPlayer):
            # only in cities with at least 20% Scottish culture
            iTotalCulture = city.countTotalCultureTimes100()
            if iTotalCulture == 0 or (city.getCulture(iPlayer) * 10000) / iTotalCulture > 20:
                iX = city.getX()
                iY = city.getY()
                tPlot = (iX, iY)
                if gc.getGame().getSorenRandNum(2, "DefiancyType") == 1:
                    utils.makeUnit(RangedClass, iPlayer, tPlot, 1)
                else:
                    utils.makeUnit(PolearmClass, iPlayer, tPlot, 1)
                print("In city: ", tPlot)
                # interface message for the human player
                if iPlayer == utils.getHumanID():
                    CyInterface().addMessage(
                        iPlayer,
                        False,
                        con.iDuration,
                        CyTranslator().getText("TXT_KEY_UNIT_NEW_DEFENDER", ())
                        + " "
                        + city.getName()
                        + "!",
                        "AS2D_UNIT_BUILD_UNIQUE_UNIT",
                        0,
                        "",
                        ColorTypes(con.iGreen),
                        iX,
                        iY,
                        True,
                        True,
                    )
