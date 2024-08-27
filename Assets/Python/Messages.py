from Consts import MessageData
from Core import human, message, player, text
from Events import handler


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
