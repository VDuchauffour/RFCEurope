from CvPythonExtensions import CyArtFileMgr
from Consts import MessageData
from Core import human, message, player, text, year
from Events import handler
import Mercenaries

ArtFileMgr = CyArtFileMgr()


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
