from CvPythonExtensions import CyArtFileMgr, CyGlobalContext, InterfaceMessageTypes
from Consts import MessageData
from Core import human, message, player, show, team, text, turns, year
from CoreTypes import Building, Civ, Wonder
from Events import handler
import Mercenaries

ArtFileMgr = CyArtFileMgr()
gc = CyGlobalContext()


@handler("cityAcquiredAndKept")
def announce_wonder_captered_when_city_acquired_and_kept(iPlayer, city):
    if city.getNumWorldWonders() > 0:
        ConquerPlayer = gc.getPlayer(city.getOwner())
        ConquerTeam = ConquerPlayer.getTeam()
        if city.getPreviousOwner() != -1:
            PreviousPlayer = gc.getPlayer(city.getPreviousOwner())
            PreviousTeam = PreviousPlayer.getTeam()
        HumanTeam = team()
        if ConquerPlayer.isHuman() or (
            player().isExisting()
            and (HumanTeam.isHasMet(ConquerTeam) or HumanTeam.isHasMet(PreviousTeam))
        ):
            # Absinthe: collect all wonders, including shrines
            lAllWonders = [w for w in Wonder] + [
                Building.CATHOLIC_SHRINE,
                Building.ORTHODOX_SHRINE,
                Building.ISLAMIC_SHRINE,
                Building.PROTESTANT_SHRINE,
            ]
            for iWonder in lAllWonders:
                if city.getNumBuilding(iWonder) > 0:
                    sWonderName = gc.getBuildingInfo(iWonder).getDescription()
                    if ConquerPlayer.isHuman():
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_CAPTURED_1", sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.BLUE,
                            location=city,
                        )
                    elif HumanTeam.isHasMet(ConquerTeam):
                        ConquerName = ConquerPlayer.getCivilizationDescriptionKey()
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_CAPTURED_2", ConquerName, sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.CYAN,
                            location=city,
                        )
                    elif HumanTeam.isHasMet(PreviousTeam):
                        PreviousName = PreviousPlayer.getCivilizationDescriptionKey()
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_CAPTURED_3", PreviousName, sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.CYAN,
                            location=city,
                        )


@handler("cityRazed")
def announce_wonder_destroyed_when_city_razed(city, iPlayer):
    if city.getNumWorldWonders() > 0:
        ConquerPlayer = gc.getPlayer(city.getOwner())
        ConquerTeam = ConquerPlayer.getTeam()
        if city.getPreviousOwner() != -1:
            PreviousPlayer = gc.getPlayer(city.getPreviousOwner())
            PreviousTeam = PreviousPlayer.getTeam()
        HumanTeam = team()
        if ConquerPlayer.isHuman() or (
            player().isExisting()
            and (HumanTeam.isHasMet(ConquerTeam) or HumanTeam.isHasMet(PreviousTeam))
        ):
            # Absinthe: collect all wonders, including shrines (even though cities with shrines can't be destroyed in the mod)
            lAllWonders = [w for w in Wonder]
            for iWonder in [
                Building.CATHOLIC_SHRINE,
                Building.ORTHODOX_SHRINE,
                Building.ISLAMIC_SHRINE,
                Building.PROTESTANT_SHRINE,
            ]:
                lAllWonders.append(iWonder)
            for iWonder in lAllWonders:
                if city.getNumBuilding(iWonder) > 0:
                    sWonderName = gc.getBuildingInfo(iWonder).getDescription()
                    if ConquerPlayer.isHuman():
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_DESTROYED_1", sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.LIGHT_RED,
                            location=city,
                        )
                    elif HumanTeam.isHasMet(ConquerTeam):
                        ConquerName = ConquerPlayer.getCivilizationDescriptionKey()
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_DESTROYED_2", ConquerName, sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.LIGHT_RED,
                            location=city,
                        )
                    elif HumanTeam.isHasMet(PreviousTeam):
                        PreviousName = PreviousPlayer.getCivilizationDescriptionKey()
                        message(
                            human(),
                            text("TXT_KEY_MISC_WONDER_DESTROYED_3", PreviousName, sWonderName),
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBuildingInfo(iWonder).getButton(),
                            color=MessageData.LIGHT_RED,
                            location=city,
                        )


@handler("cityAcquired")
def announce_last_conquered_city(owner, player_id, city, is_conquest, is_trade):
    # Absinthe: Message for the human player, if the last city of a known civ is conquered
    # all collapses operate with flips, so if the last city was conquered,
    # we are good to go (this message won't come after a collapse message)
    previous_owner = player(owner)
    if (
        not previous_owner.isHuman()
        and previous_owner.getNumCities() == 0
        and is_conquest
        and player().canContact(owner)
    ):
        message(
            human(),
            previous_owner.getCivilizationDescription(0)
            + " "
            + text("TXT_KEY_STABILITY_CONQUEST_LAST_CITY"),
            color=MessageData.RED,
        )


@handler("cityAcquiredAndKept")
def announce_available_mercs_in_new_city(iCiv, pCity):
    # Absinthe: if there are mercs available in the new city's province,
    # interface message about it to the human player
    iProvince = pCity.getProvince()
    Mercenaries.getMercLists()  # load the current mercenary pool
    for lMerc in Mercenaries.lGlobalPool:
        if lMerc[4] == iProvince:
            if iCiv == human():
                message(
                    iCiv,
                    text("TXT_KEY_MERC_AVAILABLE_NEAR_NEW_CITY", pCity.getName()),
                    button=ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARY_ICON").getPath(),
                    color=MessageData.LIME,
                    location=pCity,
                )
                break


@handler("BeginGameTurn")
def announce_schism(iGameTurn):
    # Absinthe: Message for the human player about the Schism
    if iGameTurn == year(1053):
        if player().isExisting():
            sText = text("TXT_KEY_GREAT_SCHISM")
            message(human(), sText, color=MessageData.DARK_PINK)


@handler("BeginPlayerTurn")
def announce_invaders(iGameTurn, iPlayer):
    if iPlayer == human():
        # Seljuks
        if iGameTurn == year(1064) - turns(7):
            if iPlayer == Civ.BYZANTIUM:
                show(("TXT_KEY_EVENT_BARBARIAN_INVASION_START"))
        elif iGameTurn == year(1094) + 1:
            if iPlayer == Civ.BYZANTIUM:
                sText = "Seljuk"
                show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))
        # Mongols
        elif iGameTurn == year(1236) - turns(7):
            if iPlayer in [
                Civ.KIEV,
                Civ.HUNGARY,
                Civ.POLAND,
                Civ.BULGARIA,
            ]:
                show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_START"))
        elif iGameTurn == year(1288) + turns(1):
            if iPlayer in [
                Civ.KIEV,
                Civ.HUNGARY,
                Civ.POLAND,
                Civ.BULGARIA,
            ]:
                sText = "Tatar"
                show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))
        # Timurids
        elif iGameTurn == year(1380) - turns(7):
            if iPlayer in [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM]:
                show(text("TXT_KEY_EVENT_TIMURID_INVASION_START"))
        elif iGameTurn == year(1431) + turns(1):
            if iPlayer in [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM]:
                sText = "Timurid"
                show(text("TXT_KEY_EVENT_BARBARIAN_INVASION_END", sText))
