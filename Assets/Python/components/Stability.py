# Rhye's and Fall of Civilization: Europe - Stability

from CvPythonExtensions import *
from CivilizationsData import CIVILIZATIONS
from LocationsData import CIV_GROUPS
import PyHelpers

# import cPickle as pickle
import Consts
import XMLConsts as xml
import RFCUtils
import RFCEMaps
import RiseAndFall
import ProvinceManager

utils = RFCUtils.RFCUtils()
rnf = RiseAndFall.RiseAndFall()
pm = ProvinceManager.ProvinceManager()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

tStabilityPenalty = (-5, -2, 0, 0, 0)  # province type: unstable, border, potential, historic, core


class Stability:
    def setup(self):  # Sets starting stability
        for iPlayer in range(Consts.iNumMajorPlayers):
            pPlayer = gc.getPlayer(iPlayer)
            for iCath in range(4):
                pPlayer.changeStabilityBase(iCath, -pPlayer.getStabilityBase(iCath))
                pPlayer.setStabilityVary(iCath, 0)
            pPlayer.setStabilitySwing(0)
        # Absinthe: bonus stability for the human player based on difficulty level
        iHandicap = gc.getGame().getHandicapType()
        if iHandicap == 0:
            gc.getPlayer(utils.getHumanID()).changeStabilityBase(Consts.iCathegoryExpansion, 6)
        elif iHandicap == 1:
            gc.getPlayer(utils.getHumanID()).changeStabilityBase(Consts.iCathegoryExpansion, 2)

        # Absinthe: Stability is accounted properly for stuff preplaced in the scenario file - from RFCE++
        for iPlayer in range(Consts.iNumMajorPlayers):
            pPlayer = gc.getPlayer(iPlayer)
            teamPlayer = gc.getTeam(pPlayer.getTeam())
            iCounter = 0
            for pCity in utils.getCityList(iPlayer):
                iCounter += 1
                iOldStab = pPlayer.getStability()

                # Province stability
                iProv = RFCEMaps.tProvinceMap[pCity.getY()][pCity.getX()]
                iProvinceType = pPlayer.getProvinceType(iProv)
                if iProvinceType == Consts.iProvinceCore:
                    pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
                elif not gc.hasUP(
                    iPlayer, Consts.iUP_StabilitySettler
                ):  # no instability with the Settler UP
                    if iProvinceType == Consts.iProvinceOuter:
                        pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -1)
                    elif iProvinceType == Consts.iProvinceNone:
                        pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -2)

                # Building stability: only a chance for these, as all the permanent negative stability modifiers are missing up to the start
                if (
                    pCity.hasBuilding(utils.getUniqueBuilding(iPlayer, xml.iManorHouse))
                    and gc.getGame().getSorenRandNum(10, "build stab chance") < 7
                ):
                    pPlayer.changeStabilityBase(Consts.iCathegoryEconomy, 1)
                if (
                    pCity.hasBuilding(utils.getUniqueBuilding(iPlayer, xml.iCastle))
                    and gc.getGame().getSorenRandNum(10, "build stab chance") < 7
                ):
                    pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
                if (
                    pCity.hasBuilding(utils.getUniqueBuilding(iPlayer, xml.iNightWatch))
                    and gc.getGame().getSorenRandNum(10, "build stab chance") < 7
                ):
                    pPlayer.changeStabilityBase(Consts.iCathegoryCivics, 1)
                if (
                    pCity.hasBuilding(utils.getUniqueBuilding(iPlayer, xml.iCourthouse))
                    and gc.getGame().getSorenRandNum(10, "build stab chance") < 7
                ):
                    pPlayer.changeStabilityBase(Consts.iCathegoryCities, 1)

                print(
                    pCity.getName()
                    + " contributes "
                    + str(pPlayer.getStability() - iOldStab)
                    + " stability."
                )

            # Small boost for small civs
            if iCounter < 6:  # instead of the additional boost for the first few cities
                pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, (6 - iCounter) / 2 + 1)

            # Known techs which otherwise give instability should also give the penalty here
            for iTech in [
                xml.iFeudalism,
                xml.iGuilds,
                xml.iGunpowder,
                xml.iProfessionalArmy,
                xml.iNationalism,
                xml.iCivilService,
                xml.iEconomics,
                xml.iMachinery,
                xml.iAristocracy,
            ]:
                if teamPlayer.isHasTech(iTech):
                    gc.getPlayer(iPlayer).changeStabilityBase(Consts.iCathegoryEconomy, -1)

            print("Player " + str(iPlayer) + " initial stability: " + str(pPlayer.getStability()))

            # Absinthe: update all potential provinces at the start for all living players (needed for the scenario)
            if pPlayer.isAlive():
                pm.updatePotential(iPlayer)

        # Absinthe: AI stability bonus - for civs that have a hard time at the beginning
        # 			for example France, Arabia, Bulgaria, Cordoba, Ottomans
        for iPlayer in range(Consts.iNumMajorPlayers - 1):  # no Pope, Indies, or Barbs
            pPlayer = gc.getPlayer(iPlayer)
            if iPlayer != utils.getHumanID():
                pPlayer.changeStabilityBase(
                    Consts.iCathegoryExpansion, Consts.tStabilityBonusAI[iPlayer]
                )
                if Consts.tStabilityBonusAI[iPlayer] != 0:
                    print(
                        "AI bonus stability:",
                        pPlayer.getCivilizationDescription(0),
                        Consts.tStabilityBonusAI[iPlayer],
                    )

        # Absinthe: update Byzantine stability on the start of the game
        if utils.getScenario() == Consts.i500ADScenario:
            # small stability boost for the human player for the first UHV
            if Consts.iByzantium == utils.getHumanID():
                pByzantium = gc.getPlayer(Consts.iByzantium)
                pByzantium.changeStabilityBase(Consts.iCathegoryExpansion, 4)
            self.recalcEpansion(Consts.iByzantium)

    def checkTurn(self, iGameTurn):
        # print("3Miro NewStability Check Turn")
        # 3Miro: hidden modifier based upon the group/continent
        # if (iGameTurn % 21 == 0):
        # 	self.continentsNormalization(iGameTurn)
        # if (iGameTurn % 6 == 0): #3 is too short to detect any change; must be a multiple of 3 anyway
        # gc.calcLastOwned() # Compute the RFC arrays (getlOwnedPlots,getlOwnedCities) in C instead
        # for iLoopCiv in range(iNumPlayers):
        # if ( gc.hasUP(iLoopCiv, Consts.iUP_LandStability) ): #French UP
        # self.setOwnedPlotsLastTurn(iLoopCiv, 0)
        # else:
        # self.setOwnedPlotsLastTurn(iLoopCiv, gc.getlOwnedPlots(iLoopCiv))
        # self.setOwnedCitiesLastTurn(iLoopCiv, gc.getlOwnedCities(iLoopCiv))

        ##Display up/down arrows
        # if (iGameTurn % 3 == 0 and gc.getActivePlayer().getNumCities() > 0):  #numcities required to test autoplay with minor civs
        # iHuman = utils.getHumanID()
        # self.setLastRecordedStabilityStuff(0, self.getStability(iHuman))
        # self.setLastRecordedStabilityStuff(1, utils.getParCities(iHuman))
        # self.setLastRecordedStabilityStuff(2, utils.getParCivics(iHuman))
        # self.setLastRecordedStabilityStuff(3, utils.getParEconomy(iHuman))
        # self.setLastRecordedStabilityStuff(4, utils.getParExpansion(iHuman))
        # self.setLastRecordedStabilityStuff(5, utils.getParDiplomacy(iHuman))

        # Absinthe: logging AI stability levels
        if iGameTurn % 9 == 2:
            for iPlayer in range(Consts.iNumMajorPlayers - 1):
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.getStability() != 0:
                    print(
                        "AI stability check:",
                        pPlayer.getCivilizationDescription(0),
                        pPlayer.getStability(),
                    )

    def updateBaseStability(
        self, iGameTurn, iPlayer
    ):  # Base stability is temporary (i.e. turn-based) stability
        # 3Miro: this is called for every player
        # print("3Miro NewStability Update Base")

        pPlayer = gc.getPlayer(iPlayer)
        teamPlayer = gc.getTeam(pPlayer.getTeam())

        # Swing stability converges to zero very fast
        iStabilitySwing = pPlayer.getStabilitySwing()
        if iStabilitySwing < -3 or iStabilitySwing > 3:
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() / 2)
        elif iStabilitySwing < 0:
            pPlayer.setStabilitySwing(min(0, pPlayer.getStabilitySwing() + 2))
        elif iStabilitySwing > 0:
            pPlayer.setStabilitySwing(max(0, pPlayer.getStabilitySwing() - 2))

        # Absinthe: Anarchy swing stability gets halved every turn
        iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
        if iStabSwingAnarchy > 1:
            pPlayer.setStabSwingAnarchy(pPlayer.getStabSwingAnarchy() / 2)
        elif iStabSwingAnarchy == 1:
            pPlayer.setStabSwingAnarchy(0)

        # Absinthe: anarchy timer refreshes later in the turn, so it should be reduced by 1 if we want to have it on the correct turns (if nothing else then for the human player)
        # 			but this also means that all 1st turn instability has to be added directly on the revolution / converting - CvPlayer::revolution and CvPlayer::convert
        if pPlayer.getAnarchyTurns() - 1 > 0:
            print("at least 2nd anarchy turn for:", iPlayer)
            self.recalcCivicCombos(iPlayer)
            self.recalcEpansion(iPlayer)
            iNumCities = pPlayer.getNumCities()

            if iPlayer != Consts.iPrussia:  # Absinthe: Prussian UP
                if pPlayer.isHuman():
                    # Absinthe: anarchy base instability
                    pPlayer.changeStabilityBase(
                        Consts.iCathegoryCivics, min(0, max(-2, (-iNumCities + 4) / 7))
                    )  # 0 with 1-4 cities, -1 with 5-11 cities, -2 with at least 12 cities

                    # Absinthe: more constant swing instability during anarchy, instead of ever-increasing instability from it
                    iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
                    if (
                        iStabSwingAnarchy > 0
                    ):  # half of it is already included in the swing, we only add the other half
                        pPlayer.setStabSwingAnarchy(4)
                    else:  # safety net (should be positive, as we add it before the first check)
                        pPlayer.setStabSwingAnarchy(8)
                    pPlayer.setStabilitySwing(
                        pPlayer.getStabilitySwing() - pPlayer.getStabSwingAnarchy()
                    )

                else:
                    # Absinthe: anarchy base instability
                    pPlayer.changeStabilityBase(
                        Consts.iCathegoryCivics, min(0, max(-1, (-iNumCities + 6) / 7))
                    )  # Absinthe: reduced for the AI: 0 with 1-6 cities, -1 with at least 7

                    # Absinthe: more constant swing instability during anarchy, instead of ever-increasing instability from it
                    iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
                    if (
                        iStabSwingAnarchy > 0
                    ):  # half of it is already included in the swing, we only add the other half
                        pPlayer.setStabSwingAnarchy(2)
                    else:  # safety net (should be positive, as we add it before the first check)
                        pPlayer.setStabSwingAnarchy(4)
                    pPlayer.setStabilitySwing(
                        pPlayer.getStabilitySwing() - pPlayer.getStabSwingAnarchy()
                    )

        if (
            pPlayer.getWarPeaceChange() == -1
        ):  # Whenever your nation switches from peace to the state of war (with a major nation)
            gc.getPlayer(iPlayer).changeStabilityBase(
                Consts.iCathegoryCities, -1
            )  # 1 permanent stability loss, since your people won't appreciate leaving the state of peace
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 3)

        if (iGameTurn + iPlayer) % 3 == 0:  # Economy Check every 3 turns
            self.recalcEconomy(iPlayer)

        self.recalcCity(iPlayer)  # update city stability

        # Absinthe: Collapse dates for AI nations
        if (
            iGameTurn > Consts.tCollapse[iPlayer]
            and iPlayer != utils.getHumanID()
            and pPlayer.isAlive()
        ):
            # Absinthe: -1 stability every 4 turns up to a total of -15 stability
            if iGameTurn % 4 == 0 and iGameTurn <= Consts.tCollapse[iPlayer] + 60:
                pPlayer.changeStabilityBase(Consts.iCathegoryCities, -1)

    def refreshBaseStability(
        self, iPlayer
    ):  # Base stability is temporary (i.e. turn-based) stability
        # Absinthe: this is called upon entering the stability/finance screen (F2)

        pPlayer = gc.getPlayer(iPlayer)

        self.recalcCivicCombos(iPlayer)
        self.recalcEpansion(iPlayer)
        self.recalcEconomy(iPlayer)
        self.recalcCity(iPlayer)

    def continentsNormalization(self, iGameTurn):  # Sedna17
        pass
        # lContinentModifier = [-1, -1, 0, -2, 0, 0]
        # for civ in CIVILIZATIONS.get_majors():
        #     if gc.getPlayer(civ.id).isAlive():
        #         for group_key, group_civs in CIV_GROUPS.items():
        #             if civ.key in group_civs:
        #                 self.setParameter(civ.id, 12, True, lContinentModifier[group_key.value])
        #                 self.setStability(
        #                     civ.id,
        #                     (self.getStability(civ.id) + lContinentModifier[group_key.value]),
        #                 )

    def onCityBuilt(self, iPlayer, x, y):
        iProv = RFCEMaps.tProvinceMap[y][x]
        pPlayer = gc.getPlayer(iPlayer)
        # Absinthe: +1 for core, -1 for contested, -2 for foreign provinces
        iProvinceType = pPlayer.getProvinceType(iProv)
        if iProvinceType == Consts.iProvinceCore:
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
        elif not gc.hasUP(
            iPlayer, Consts.iUP_StabilitySettler
        ):  # no instability with the Settler UP
            if iProvinceType == Consts.iProvinceOuter:
                pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -1)
            elif iProvinceType == Consts.iProvinceNone:
                pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -2)
        if pPlayer.getNumCities() < 5:  # early boost to small civs
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
        self.recalcEpansion(iPlayer)
        self.recalcCivicCombos(iPlayer)

    def onCityAcquired(self, iOwner, playerType, city, bConquest, bTrade):
        pOwner = gc.getPlayer(iOwner)
        pConq = gc.getPlayer(playerType)

        if city.hasBuilding(xml.iEscorial):
            pConq.setPicklefreeParameter(Consts.iIsHasEscorial, 1)
            pOwner.setPicklefreeParameter(Consts.iIsHasEscorial, 0)
        if city.hasBuilding(xml.iStephansdom):
            pConq.setPicklefreeParameter(Consts.iIsHasStephansdom, 1)
            pOwner.setPicklefreeParameter(Consts.iIsHasStephansdom, 0)
        if city.hasBuilding(xml.iShrineOfUppsala):
            pConq.setPicklefreeParameter(Consts.iIsHasUppsalaShrine, 1)
            pOwner.setPicklefreeParameter(Consts.iIsHasUppsalaShrine, 0)
        if city.hasBuilding(xml.iKoutoubiaMosque):
            pConq.setPicklefreeParameter(Consts.iIsHasKoutoubiaMosque, 1)
            pOwner.setPicklefreeParameter(Consts.iIsHasKoutoubiaMosque, 0)
        if city.hasBuilding(xml.iMagnaCarta):
            pConq.setPicklefreeParameter(Consts.iIsHasMagnaCarta, 1)
            pOwner.setPicklefreeParameter(Consts.iIsHasMagnaCarta, 0)

        self.recalcCivicCombos(playerType)
        self.recalcCivicCombos(iOwner)
        iProv = city.getProvince()
        iProvOwnerType = pOwner.getProvinceType(iProv)
        iProvConqType = pConq.getProvinceType(iProv)

        if iProvOwnerType >= Consts.iProvinceNatural:
            if iOwner == Consts.iScotland:  # Scotland UP part 2
                pOwner.changeStabilityBase(Consts.iCathegoryExpansion, -2)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 2)
            else:
                pOwner.changeStabilityBase(Consts.iCathegoryExpansion, -3)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 4)
        elif iProvOwnerType < Consts.iProvinceNatural:
            if iOwner == Consts.iScotland:  # Scotland UP part 2
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 1)
            else:
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 2)

        if iProvConqType >= Consts.iProvinceNatural:
            pConq.changeStabilityBase(Consts.iCathegoryExpansion, 1)
            pConq.setStabilitySwing(pConq.getStabilitySwing() + 3)

        if pConq.getCivics(5) == xml.iCivicOccupation:
            pConq.changeStabilityBase(Consts.iCathegoryExpansion, 1)

        if (
            iOwner < Consts.iNumPlayers
            and city.getX() == Consts.tCapitals[iOwner][0]
            and city.getY() == Consts.tCapitals[iOwner][1]
        ):
            if iOwner == Consts.iScotland:  # Scotland UP part 2
                pOwner.changeStabilityBase(Consts.iCathegoryExpansion, -5)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 5)
            elif gc.hasUP(
                iOwner, Consts.iUP_Emperor
            ):  # If Byzantium loses Constantinople, they should lose all non-core cities
                pOwner.changeStabilityBase(Consts.iCathegoryExpansion, -20)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 20)
            else:
                pOwner.changeStabilityBase(Consts.iCathegoryExpansion, -10)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 10)
        self.recalcEpansion(iOwner)
        self.recalcEpansion(playerType)

    def onCityRazed(self, iOwner, iPlayer, city):
        # Sedna17: Not sure what difference between iOwner and iPlayer is here
        # 3Miro: iOwner owns the city (victim) and I think iPlayer is the one razing the city
        # 		On second thought, if iOwner (the previous owner) doesn't have enough culture, then iOwner == playerType
        # AbsintheRed: iPlayer is the one razing city, iOwner is the previous owner of the city (right before iPlayer)
        pPlayer = gc.getPlayer(iPlayer)
        pOwner = gc.getPlayer(iOwner)
        if city.hasBuilding(xml.iEscorial):
            pPlayer.setPicklefreeParameter(Consts.iIsHasEscorial, 0)
            pOwner.setPicklefreeParameter(Consts.iIsHasEscorial, 0)
        if city.hasBuilding(xml.iStephansdom):
            pPlayer.setPicklefreeParameter(Consts.iIsHasStephansdom, 0)
            pOwner.setPicklefreeParameter(Consts.iIsHasStephansdom, 0)
        if city.hasBuilding(xml.iShrineOfUppsala):
            pPlayer.setPicklefreeParameter(Consts.iIsHasUppsalaShrine, 0)
            pOwner.setPicklefreeParameter(Consts.iIsHasUppsalaShrine, 0)
        if city.hasBuilding(xml.iKoutoubiaMosque):
            pPlayer.setPicklefreeParameter(Consts.iIsHasKoutoubiaMosque, 0)
            pOwner.setPicklefreeParameter(Consts.iIsHasKoutoubiaMosque, 0)
        if city.hasBuilding(xml.iMagnaCarta):
            pPlayer.setPicklefreeParameter(Consts.iIsHasMagnaCarta, 0)
            pOwner.setPicklefreeParameter(Consts.iIsHasMagnaCarta, 0)
        self.recalcCivicCombos(iPlayer)
        self.recalcCivicCombos(iOwner)

        # Absinthe: city razing penalty - permanent, based on city population
        # note that the city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size
        # so currently: 0 with 1-2 population, -1 with 3-5 population, -2 with 6-9 population, -3 with 10+ population
        iRazeStab = 0
        if city.getPopulation() >= 9:
            iRazeStab = 3
        elif city.getPopulation() >= 5:
            iRazeStab = 2
        elif city.getPopulation() >= 2:
            iRazeStab = 1
        # Absinthe: Norwegian UP - one less stability penalty
        if iPlayer == Consts.iNorway:
            iRazeStab -= 1
        if iRazeStab > 0:
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -iRazeStab)
        # temporary, 3 for everyone but Norway
        if iPlayer != Consts.iNorway:
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 3)
        self.recalcEpansion(iPlayer)

    def onImprovementDestroyed(self, owner):
        pPlayer = gc.getPlayer(owner)
        pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 2)

    def onTechAcquired(self, iTech, iPlayer):
        if iTech in [
            xml.iFeudalism,
            xml.iGuilds,
            xml.iGunpowder,
            xml.iProfessionalArmy,
            xml.iNationalism,
            xml.iCivilService,
            xml.iEconomics,
            xml.iMachinery,
            xml.iAristocracy,
        ]:
            gc.getPlayer(iPlayer).changeStabilityBase(Consts.iCathegoryEconomy, -1)
        pass

    def onBuildingBuilt(self, iPlayer, iBuilding):
        pPlayer = gc.getPlayer(iPlayer)
        if iBuilding == utils.getUniqueBuilding(iPlayer, xml.iManorHouse):
            pPlayer.changeStabilityBase(Consts.iCathegoryEconomy, 1)
            ## Naval base adds an additional stability point
            # if iBuilding == xml.iVeniceNavalBase:
            # 	pPlayer.changeStabilityBase( iCathegoryEconomy, 1 )
            self.recalcEconomy(iPlayer)
        elif iBuilding == utils.getUniqueBuilding(iPlayer, xml.iCastle):
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
            self.recalcEpansion(iPlayer)
        elif iBuilding == utils.getUniqueBuilding(iPlayer, xml.iNightWatch):
            pPlayer.changeStabilityBase(Consts.iCathegoryCivics, 1)
            self.recalcCivicCombos(iPlayer)
        elif iBuilding == utils.getUniqueBuilding(iPlayer, xml.iCourthouse):
            pPlayer.changeStabilityBase(Consts.iCathegoryCities, 1)
            self.recalcCity(iPlayer)
        elif iBuilding == xml.iEscorial:
            pPlayer.setPicklefreeParameter(Consts.iIsHasEscorial, 1)
        elif iBuilding == xml.iStephansdom:
            pPlayer.setPicklefreeParameter(Consts.iIsHasStephansdom, 1)
        elif iBuilding == xml.iShrineOfUppsala:
            pPlayer.setPicklefreeParameter(Consts.iIsHasUppsalaShrine, 1)
        elif iBuilding == xml.iKoutoubiaMosque:
            pPlayer.setPicklefreeParameter(Consts.iIsHasKoutoubiaMosque, 1)
        elif iBuilding == xml.iMagnaCarta:
            pPlayer.setPicklefreeParameter(Consts.iIsHasMagnaCarta, 1)
        elif iBuilding == xml.iPalace:
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, -2)
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 5)
            self.recalcEpansion(iPlayer)
        elif iBuilding == xml.iReliquary:
            pPlayer.changeStabilityBase(Consts.iCathegoryExpansion, 1)
            self.recalcEpansion(iPlayer)

    def onProjectBuilt(self, iPlayer, iProject):
        pPlayer = gc.getPlayer(iPlayer)
        iCivic5 = pPlayer.getCivics(5)
        if iProject >= xml.iNumNotColonies:
            pPlayer.changeStabilityBase(
                Consts.iCathegoryExpansion, -2
            )  # -2 stability for each colony
            if iCivic5 == xml.iCivicColonialism:
                pPlayer.changeStabilityBase(
                    Consts.iCathegoryExpansion, 1
                )  # one less stability penalty if civ is in Colonialism
        self.recalcEpansion(iPlayer)

    def onCombatResult(self, argsList):
        pass

    def onReligionFounded(self, iPlayer):
        pass

    def onReligionSpread(self, iReligion, iPlayer):
        pass
        # Sedna17: Religions seemed to be subtracted and re-inserted into cities, which makes this a bad idea.
        # if (iPlayer < iNumPlayers):
        # 	pPlayer = gc.getPlayer(iPlayer)
        # 	if (pPlayer.getStateReligion() != iReligion):
        # 		for iLoopCiv in range(iNumPlayers):
        # 			if (gc.getTeam(pPlayer.getTeam()).isAtWar(iLoopCiv)):
        # 				if (gc.getPlayer(iLoopCiv).getStateReligion() == iReligion):
        # 					self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
        # 					self.setParameter(iPlayer, iParCitiesE, True, -1)
        # 					print("Stability - onReligionSpread - Target = ", iPlayer, "Cause = ", iLoopCiv, "Religion = ",iReligion)
        # 					break

    def checkImplosion(self, iGameTurn):
        if iGameTurn > 14 and iGameTurn % 6 == 3:
            for iPlayer in range(Consts.iNumPlayers - 1):
                pPlayer = gc.getPlayer(iPlayer)
                # Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
                iRespawnTurn = utils.getLastRespawnTurn(iPlayer)
                if (
                    pPlayer.isAlive()
                    and iGameTurn >= Consts.tBirth[iPlayer] + 15
                    and iGameTurn >= iRespawnTurn + 10
                ):
                    iStability = pPlayer.getStability()
                    # Absinthe: human player with very bad stability should have a much bigger chance for collapse
                    if iStability < -14 and iPlayer == utils.getHumanID():
                        if (
                            gc.getGame().getSorenRandNum(100, "human collapse")
                            < 0 - 2 * iStability
                        ):  # 30 chance with -15, 50% with -25, 70% with -35, 100% with -50 or less
                            if not utils.collapseImmune(iPlayer):
                                self.collapseCivilWar(iPlayer, iStability)
                        else:  # when won't collapse, secession should always happen
                            rnf.revoltCity(iPlayer, False)
                    # Absinthe: if stability is less than -3, there is a chance that the secession/revolt or collapse mechanics start
                    # 			if more than 8 cities: high chance for secession mechanics, low chance for collapse
                    # 			elif more than 4 cities: medium chance for collapse mechanics, medium chance for secession
                    # 			otherwise big chance for collapse mechanics
                    # 			the actual chance for both secession/revolt and total collapse is increasing with lower stability
                    elif iStability < -3:
                        iRand1 = gc.getGame().getSorenRandNum(
                            10, "chance for city secession or civ collapse"
                        )
                        iRand2 = gc.getGame().getSorenRandNum(
                            10, "chance for city secession or civ collapse"
                        )
                        iRand3 = gc.getGame().getSorenRandNum(
                            10, "chance for city secession or civ collapse"
                        )
                        if pPlayer.getNumCities() > 8:
                            if iRand1 < 8:  # 80 chance for secession start
                                if iRand2 < (
                                    -3 - iStability
                                ):  # 10% at -4, increasing by 10% with each point (100% with -13 or less)
                                    rnf.revoltCity(iPlayer, False)
                            elif (
                                iRand3 < 1
                                and iGameTurn >= Consts.tBirth[iPlayer] + 20
                                and not utils.collapseImmune(iPlayer)
                            ):  # 10 chance for collapse start
                                if iRand2 < (
                                    -1.5 - (iStability / 2)
                                ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                    self.collapseCivilWar(iPlayer, iStability)
                        elif pPlayer.getNumCities() > 4:
                            if iRand1 < 4:  # 40 chance for secession start
                                if iRand2 < (
                                    -3 - iStability
                                ):  # 10% at -4, increasing by 10% with each point (100% with -13 or less)
                                    rnf.revoltCity(iPlayer, False)
                            elif (
                                iRand3 < 4
                                and iGameTurn >= Consts.tBirth[iPlayer] + 20
                                and not utils.collapseImmune(iPlayer)
                            ):  # 40 chance for collapse start
                                if iRand2 < (
                                    -1.5 - (iStability / 2)
                                ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                    self.collapseCivilWar(iPlayer, iStability)
                        elif (
                            iRand1 < 7
                            and iGameTurn >= Consts.tBirth[iPlayer] + 20
                            and not utils.collapseImmune(iPlayer)
                        ):  # 70 chance for collapse start
                            if iRand2 < (
                                -1.5 - (iStability / 2)
                            ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                self.collapseCivilWar(iPlayer, iStability)

    def collapseCivilWar(self, iPlayer, iStability):
        pPlayer = gc.getPlayer(iPlayer)
        iHuman = utils.getHumanID()
        print("COLLAPSE: CIVIL WAR", pPlayer.getCivilizationAdjective(0), "Stability:", iStability)
        if iPlayer != iHuman:
            if gc.getPlayer(iHuman).canContact(iPlayer):
                CyInterface().addMessage(
                    iHuman,
                    False,
                    Consts.iDuration,
                    pPlayer.getCivilizationDescription(0)
                    + " "
                    + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_STABILITY", ()),
                    "",
                    0,
                    "",
                    ColorTypes(Consts.iRed),
                    -1,
                    -1,
                    True,
                    True,
                )
            utils.killAndFragmentCiv(iPlayer, False, False)
        elif pPlayer.getNumCities() > 1:
            CyInterface().addMessage(
                iPlayer,
                True,
                Consts.iDuration,
                CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_STABILITY_HUMAN", ()),
                "",
                0,
                "",
                ColorTypes(Consts.iRed),
                -1,
                -1,
                True,
                True,
            )
            utils.killAndFragmentCiv(iPlayer, False, True)
            self.zeroStability(iPlayer)

    def printStability(self, iGameTurn, iPlayer):
        cyPlayer = PyHelpers.PyPlayer(iPlayer)
        pPlayer = gc.getPlayer(iPlayer)
        print(" Turn: ", iGameTurn)
        print(" ---------------- New Stability For " + cyPlayer.getCivilizationShortDescription())
        print("                  Stability : ", pPlayer.getStability())
        print(
            "                  Cities    : ",
            pPlayer.getStabilityBase(Consts.iCathegoryCities)
            + pPlayer.getStabilityVary(Consts.iCathegoryCities),
        )
        print(
            "                  Civics    : ",
            pPlayer.getStabilityBase(Consts.iCathegoryCivics)
            + pPlayer.getStabilityVary(Consts.iCathegoryCivics),
        )
        print(
            "                  Economy   : ",
            pPlayer.getStabilityBase(Consts.iCathegoryEconomy)
            + pPlayer.getStabilityVary(Consts.iCathegoryEconomy),
        )
        print(
            "                  Expansion : ",
            pPlayer.getStabilityBase(Consts.iCathegoryExpansion)
            + pPlayer.getStabilityVary(Consts.iCathegoryExpansion),
        )
        print("                  Swing     : ", pPlayer.getStabilitySwing())

    def zeroStability(self, iPlayer):  # Called by Stability.CheckImplosion
        pPlayer = gc.getPlayer(iPlayer)
        pPlayer.changeStabilityBase(
            Consts.iCathegoryCities, -pPlayer.getStabilityBase(Consts.iCathegoryCities)
        )
        pPlayer.changeStabilityBase(
            Consts.iCathegoryCivics, -pPlayer.getStabilityBase(Consts.iCathegoryCivics)
        )
        pPlayer.changeStabilityBase(
            Consts.iCathegoryEconomy, -pPlayer.getStabilityBase(Consts.iCathegoryEconomy)
        )
        pPlayer.changeStabilityBase(
            Consts.iCathegoryExpansion, -pPlayer.getStabilityBase(Consts.iCathegoryExpansion)
        )
        pPlayer.setStabilityVary(Consts.iCathegoryCities, 0)
        pPlayer.setStabilityVary(Consts.iCathegoryCivics, 0)
        pPlayer.setStabilityVary(Consts.iCathegoryEconomy, 0)
        pPlayer.setStabilityVary(Consts.iCathegoryExpansion, 0)
        pPlayer.setStabilitySwing(0)

    def recalcCity(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iCivic4 = pPlayer.getCivics(4)
        iCivic5 = pPlayer.getCivics(5)
        iTotalHappy = (
            pPlayer.calculateTotalCityHappiness() - pPlayer.calculateTotalCityUnhappiness()
        )
        iCityStability = 0
        if pPlayer.getNumCities() == 0:
            iHappyStability = 0
        else:
            iHappyStability = (
                iTotalHappy / pPlayer.getNumCities()
            )  # +k stability for an average city happiness of at least k
        iCivHealthStability = 0
        iHealthStability = 0
        iHurryStability = 0
        iMilitaryStability = 0
        iWarWStability = 0
        iReligionStability = 0
        iCivicReligionInstability = 0
        iCultureStability = 0

        for pCity in utils.getCityList(iPlayer):
            # Absinthe: if your civ is healthy, bonus stability
            # 			if one of your is cities is unhealthy, -1 stability
            iCivHealthStability += pCity.goodHealth()
            iCivHealthStability -= pCity.badHealth(False)
            if pCity.goodHealth() - pCity.badHealth(False) < 0:
                iHealthStability -= 1
            if pCity.angryPopulation(0) > 0:
                iHappyStability -= 2

            # Absinthe: This is the "We desire religious freedom!" unhappiness, from civics - currently from the Religious Law civic
            # 			also it is a negative counter with the current civic setup, so getReligionBadHappiness() == -1 with one non-state religion in the city
            if pCity.getReligionBadHappiness() < 0:
                if not gc.hasUP(iPlayer, Consts.iUP_ReligiousTolerance):  # Polish UP
                    iCivicReligionInstability += 1
            if pCity.getHurryAngerModifier() > 0:
                iHurryStability -= 1
            if pCity.getNoMilitaryPercentAnger() > 0:
                iMilitaryStability -= 1
            # Absinthe: getWarWearinessPercentAnger is not a local variable for your cities, but a global one for your entire civ
            # 			it would results in 1 instability for each city if there is an ongoing war, thus I added some modifications below
            if pCity.getWarWearinessPercentAnger() > 10:
                iWarWStability -= 1

            bJewInstability = False
            if (
                iCivic4 != xml.iCivicFreeReligion
            ):  # Religious Tolerance negates stability penalties from non-state religions
                if not gc.hasUP(iPlayer, Consts.iUP_ReligiousTolerance):  # Polish UP
                    if pCity.getNumForeignReligions() > 0:
                        # only calculate if Judaism is not the State Religion
                        if pPlayer.getStateReligion() != xml.iJudaism:
                            bJewInstability = True
                        if iCivic4 == xml.iCivicPaganism:  # Pagans are a bit more tolerant
                            iReligionStability -= 1
                        elif (
                            iPlayer == Consts.iTurkey
                        ):  # Janissary UP - not necessarily a historical aspect of it, but important for gameplay
                            # elif ( gc.hasUP( iPlayer, Consts.iUP_Janissary )):
                            iReligionStability -= 1
                        else:
                            iReligionStability -= 2
                    if (
                        pCity.getNumForeignReligions() > 1
                    ):  # additional -1 stability for every further foreign religion
                        iReligionStability -= min(pCity.getNumForeignReligions() - 1, 3)

            # Absinthe: Jewish Quarter reduces religion instability if Judaism is present in the city
            if (
                bJewInstability
                and pCity.hasBuilding(xml.iJewishQuarter)
                and pCity.isHasReligion(xml.iJudaism)
            ):  # only if there are some religious penalties present in the city
                iReligionStability += 1

            # Absinthe: -1 stability if own culture is less than 40% of total culture in a city, -2 stability if less than 20%
            iTotalCulture = pCity.countTotalCultureTimes100()
            if (
                (iTotalCulture > 0)
                and ((pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 40)
                and not gc.hasUP(iPlayer, Consts.iUP_CulturalTolerance)
            ):
                # Absinthe: 1 less instability with the Vassalage Civic, so only -1 with less than 20%, 0 otherwise
                if iCivic5 != xml.iCivicSubjugation:
                    iCultureStability -= 1
                if (pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 20:
                    iCultureStability -= 1

        # Absinthe: if your civ is healthy, bonus stability
        if iCivHealthStability > 0:
            iCivHealthStability = (
                iCivHealthStability / pPlayer.getNumCities()
            )  # +k stability for an average city health of at least k
            iHealthStability += iCivHealthStability

        # Absinthe: reduced value for getReligionBadHappiness, shouldn't add -1 for each city if almost all of them has multiple religions
        # 			switching in and out of the civic won't result in that much fluctuation
        iCivicReligionInstability = min(pPlayer.getNumCities() / 2, iCivicReligionInstability)

        # Absinthe: persecution counter - cooldown is handled in Religions.checkTurn
        # 			1-3 means 1 instability, 4-6 means 2 instability, 7-9 means 3 instability, etc...
        iProsecutionCount = pPlayer.getProsecutionCount()
        if iProsecutionCount > 0:
            iReligionStability -= (iProsecutionCount + 2) / 3

        # Humans are far more competent then the AI, so the AI won't get all the penalties
        if pPlayer.isHuman():
            iCityStability += (
                iHappyStability
                + iHealthStability
                + iReligionStability
                - iCivicReligionInstability
                + iHurryStability
                + iCultureStability
                + iMilitaryStability
            )
            iCityStability += max(
                iWarWStability / 3 - 1, -10
            )  # max 10 instability from war weariness
            iCityStability = min(
                iCityStability, 8
            )  # max 8 extra stability from cities - don't want to add too many bonuses for runaway civs
        else:
            iCityStability += max(iHappyStability, -5) + max(
                iHealthStability, -5
            )  # AI keeps very unhappy cities
            iCityStability += max(
                iReligionStability - iCivicReligionInstability + iHurryStability, -7
            ) + max(iCultureStability, -5)
            iCityStability += max(
                iMilitaryStability + iWarWStability / 3, -3
            )  # AI is also bad at handling war weariness
            iCityStability = min(max(iCityStability, -10), 8)
        iCityStability += pPlayer.getFaithBenefit(Consts.iFP_Stability)
        print(
            " City Stability for: ",
            iPlayer,
            " Categories: ",
            iHappyStability,
            iHealthStability,
            iHurryStability,
            iMilitaryStability,
            iWarWStability,
            iReligionStability,
            iCultureStability,
        )
        if pPlayer.getGoldenAgeTurns() > 0:
            iCityStability += 8
        # Absinthe: Westminster Abbey faith-stability effect
        if pPlayer.countNumBuildings(xml.iWestminster) > 0:
            # would be better, if the stability bonus was also only applied for Divine Monarchy?
            # if pPlayer.getCivics(0) == xml.iCivicDivineMonarchy:
            iFaith = pPlayer.getFaith()
            iCityStability += iFaith / 20

        pPlayer.setStabilityVary(Consts.iCathegoryCities, iCityStability)

    def recalcCivicCombos(self, iPlayer):
        # Note: this is more or less the only place where Civics are referenced, yet referring them by number makes this hard to read
        pPlayer = gc.getPlayer(iPlayer)
        iCivicGovernment = pPlayer.getCivics(0)
        iCivicLegal = pPlayer.getCivics(1)
        iCivicLabor = pPlayer.getCivics(2)
        iCivicEconomy = pPlayer.getCivics(3)
        iCivicReligion = pPlayer.getCivics(4)
        iCivicExpansion = pPlayer.getCivics(5)

        lCivics = [
            iCivicGovernment,
            iCivicLegal,
            iCivicLabor,
            iCivicEconomy,
            iCivicReligion,
            iCivicExpansion,
        ]
        lCombinations = [
            (iCivic1, iCivic2) for iCivic1 in lCivics for iCivic2 in lCivics if iCivic1 < iCivic2
        ]

        iCivicCombo = 0
        # Calculate the combinations
        for lCombination in lCombinations:
            iComboValue = self.getCivicCombinationStability(lCombination[0], lCombination[1])
            if iComboValue < 0 and pPlayer.getPicklefreeParameter(Consts.iIsHasMagnaCarta) == 1:
                iComboValue = 0
            iCivicCombo += iComboValue

        if pPlayer.getPicklefreeParameter(Consts.iIsHasStephansdom) == 1:
            if iCivicGovernment in [
                xml.iCivicFeudalMonarchy,
                xml.iCivicDivineMonarchy,
                xml.iCivicLimitedMonarchy,
            ]:
                iCivicCombo += 2

        if pPlayer.getPicklefreeParameter(Consts.iIsHasUppsalaShrine) == 1:
            if iCivicReligion == xml.iCivicPaganism:
                iCivicCombo += 3

        if pPlayer.getPicklefreeParameter(Consts.iIsHasKoutoubiaMosque) == 1:
            if iCivicLegal == xml.iCivicReligiousLaw:
                iCivicCombo += 4

        if iCivicLegal == xml.iCivicBureaucracy:  # Bureaucracy city cap
            if (
                iPlayer == Consts.iNovgorod and pPlayer.getNumCities() > 6
            ):  # the penalties are halved for Novgorod
                iBureaucracyCap = (6 - pPlayer.getNumCities()) / 2
            else:
                iBureaucracyCap = 6 - pPlayer.getNumCities()
            if not pPlayer.isHuman():  # max -5 penalty for the AI
                iBureaucracyCap = max(-5, iBureaucracyCap)
            iCivicCombo += iBureaucracyCap

        if iCivicGovernment == xml.iCivicMerchantRepublic:  # Merchant Republic city cap
            if (
                iPlayer == Consts.iVenecia and pPlayer.getNumCities() > 5
            ):  # the penalties are halved for Venice
                iMerchantRepublicCap = (5 - pPlayer.getNumCities()) / 2
            else:
                iMerchantRepublicCap = 5 - pPlayer.getNumCities()
            if not pPlayer.isHuman():  # max -5 penalty for the AI
                iMerchantRepublicCap = max(-5, iMerchantRepublicCap)
            iCivicCombo += iMerchantRepublicCap

        pPlayer.setStabilityVary(Consts.iCathegoryCivics, iCivicCombo)

    def getCivicCombinationStability(self, iCivic0, iCivic1):
        lCivics = set([iCivic0, iCivic1])

        if xml.iCivicFeudalMonarchy in lCivics:
            if xml.iCivicFeudalLaw in lCivics:
                return 3

        if (
            xml.iCivicDivineMonarchy in lCivics
        ):  # Divine Monarchy should have an appropriate religious civic
            if xml.iCivicReligiousLaw in lCivics:
                return 2
            if xml.iCivicPaganism in lCivics:
                return -4
            if xml.iCivicStateReligion in lCivics:
                return 2
            if xml.iCivicTheocracy in lCivics:
                return 3
            if xml.iCivicOrganizedReligion in lCivics:
                return 4
            if xml.iCivicFreeReligion in lCivics:
                return -3

        if (
            xml.iCivicLimitedMonarchy in lCivics
        ):  # Constitutional Monarchy and Republic both like enlightened civics
            if xml.iCivicCommonLaw in lCivics:
                return 3
            if xml.iCivicFreePeasantry in lCivics:
                return 2
            if xml.iCivicFreeLabor in lCivics:
                return 2

        if (
            xml.iCivicMerchantRepublic in lCivics
        ):  # Constitutional Monarchy and Republic both like enlightened civics
            if xml.iCivicFeudalLaw in lCivics:
                return -3
            if xml.iCivicCommonLaw in lCivics:
                return 3
            if xml.iCivicFreePeasantry in lCivics:
                return 2
            if xml.iCivicFreeLabor in lCivics:
                return 2
            if xml.iCivicTradeEconomy in lCivics:
                return 4
            if xml.iCivicMercantilism in lCivics:
                return -4
            if xml.iCivicImperialism in lCivics:
                return -2

        if xml.iCivicFeudalLaw in lCivics:
            if xml.iCivicSerfdom in lCivics:
                return 3
            if xml.iCivicFreePeasantry in lCivics:
                return -4
            if xml.iCivicManorialism in lCivics:
                return 2
            if xml.iCivicVassalage in lCivics:
                return 2

        if xml.iCivicReligiousLaw in lCivics:
            if xml.iCivicPaganism in lCivics:
                return -5
            if xml.iCivicTheocracy in lCivics:
                return 5
            if xml.iCivicFreeReligion in lCivics:
                return -3

        if xml.iCivicCommonLaw in lCivics:
            if xml.iCivicSerfdom in lCivics:
                return -3
            if xml.iCivicFreeLabor in lCivics:
                return 3
            if xml.iCivicTheocracy in lCivics:
                return -4

        if xml.iCivicSerfdom in lCivics:
            if xml.iCivicManorialism in lCivics:
                return 2
            if xml.iCivicTradeEconomy in lCivics:
                return -3

        if xml.iCivicApprenticeship in lCivics:
            if xml.iCivicGuilds in lCivics:
                return 3

        return 0

    def recalcEconomy(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iPopNum = pPlayer.getTotalPopulation()
        iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
        iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
        # Absinthe: removed - why was Cordoba penalized in the first place?
        # if iPlayer == Consts.iCordoba:
        # 	iImports /= 2
        # 	iExports /= 2

        iFinances = pPlayer.getFinancialPower()
        iInflation = pPlayer.calculateInflatedCosts()
        iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
        # Absinthe: removed - Venice no longer has that weak production
        # if iPlayer == Consts.iVenecia:
        # 	iProduction += iPopNum # offset their weak production
        iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)

        iLargeCities = 0
        for pCity in utils.getCityList(iPlayer):
            # Absinthe: production penalty removed - was a mistake to add a city-based modifier to the financial stability which is based on average per population
            # if pCity.isProductionUnit():
            # 	iUnit = pCity.getProductionUnit()
            # 	if iUnit < xml.iWorker or iUnit > xml.iIslamicMissionary:
            # 		iProductionPenalty -= 1
            # elif pCity.isProductionBuilding():
            # 	iBuilding = pCity.getProductionBuilding()
            # 	if utils.isWonder(iBuilding):
            # 		iProductionPenalty -= 2
            # else:
            # 	iProductionPenalty -= 2
            iCityPop = pCity.getPopulation()
            if (
                iCityPop > 10
            ):  # large cities should have production bonus buildings, drop by 10 percent
                iProduction -= pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION) / 10
                iLargeCities += 1

        iNumCities = pPlayer.getNumCities()
        if iNumCities > 0:
            iIndustrialStability = min(
                max(2 * (2 * iAgriculture + iProduction) / iPopNum - 14, -3), 3
            )  # this is 0 if the average yield per population is a little more than 2 food and 2 production (with bonuses)
            if (
                pPlayer.getPicklefreeParameter(Consts.iIsHasEscorial) == 1
            ):  # El Escorial no economic instability effect
                iIndustrialStability = max(iIndustrialStability, 0)
            iFinances = (
                iFinances * (100 - 20 * iLargeCities / iNumCities) / 100
            )  # between 80% and 100%, based on the number of large cities
            iFinancialStability = min(
                max((iFinances - iInflation + iImports + iExports) / iPopNum - 6, -4), 4
            )  # this is 0 if the average financial power per population is around 6
            # iFinancialPowerPerCity = ( iFinances - iInflation + iImports + iExports ) / iNumCities
            if (
                pPlayer.getPicklefreeParameter(Consts.iIsHasEscorial) == 1
            ):  # El Escorial no economic instability effect
                iFinancialStability = max(iFinancialStability, 0)
            pPlayer.setStabilityVary(
                Consts.iCathegoryEconomy, iFinancialStability + iIndustrialStability
            )
        else:
            pPlayer.setStabilityVary(Consts.iCathegoryEconomy, 0)

    def recalcEpansion(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iExpStability = 0
        iCivic5 = pPlayer.getCivics(5)
        bIsUPLandStability = gc.hasUP(iPlayer, Consts.iUP_LandStability)
        iCivicBonus = 0
        iUPBonus = 0
        for pCity in utils.getCityList(iPlayer):
            iProvType = pPlayer.getProvinceType(pCity.getProvince())
            iProvNum = pCity.getProvince()
            CityName = pCity.getNameKey()
            if not (0 <= iProvType < len(tStabilityPenalty)):
                print("ProvinceType issue, iProvType:", iProvType)
                print("ProvinceType issue, iProvNum:", iProvNum)
                print("ProvinceType issue, CityName:", CityName)
            assert 0 <= iProvType < len(tStabilityPenalty), (
                "Bad ProvinceType value for CityName (%s)" % CityName
            )

            iExpStability += tStabilityPenalty[iProvType]
            if iProvType <= Consts.iProvinceOuter:
                if iCivic5 == xml.iCivicImperialism:  # Imperialism
                    iCivicBonus += 1
                if bIsUPLandStability:  # French UP
                    iUPBonus += 1
        iExpStability += iCivicBonus  # Imperialism
        iExpStability += iUPBonus  # French UP
        if pPlayer.getCivics(5) != xml.iCivicOccupation:
            iExpStability -= 3 * pPlayer.getForeignCitiesInMyProvinceType(
                Consts.iProvinceCore
            )  # -3 stability for each foreign/enemy city in your core provinces, without the Militarism civic
            iExpStability -= 1 * pPlayer.getForeignCitiesInMyProvinceType(
                Consts.iProvinceNatural
            )  # -1 stability for each foreign/enemy city in your natural provinces, without the Militarism civic
        if pPlayer.getMaster() > -1:
            iExpStability += 8
        if iCivic5 == xml.iCivicVassalage:
            iExpStability += 3 * pPlayer.countVassals()
        else:
            iExpStability += pPlayer.countVassals()
        iNumCities = pPlayer.getNumCities()
        if iPlayer in [Consts.iTurkey, Consts.iMoscow]:  # five free cities for those two
            iNumCities = max(0, iNumCities - 5)
        iExpStability -= iNumCities * iNumCities / 40
        # 	if ( pPlayer.getID() == Consts.iTurkey and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1570AD ): # boost Turkey before the battle of Lepanto
        # 		if ( not pPlayer.isHuman() ):
        # 			iExpStability += min( 3 - pPlayer.getStability(), 6 )
        # 	if ( pPlayer.getID() == Consts.iVenecia and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1204AD ): # Venice has trouble early on due to its civics
        # 		if ( not pPlayer.isHuman() ):
        # 			iExpStability += 4
        pPlayer.setStabilityVary(Consts.iCathegoryExpansion, iExpStability)
