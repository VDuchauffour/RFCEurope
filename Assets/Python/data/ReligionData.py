from BaseStructures import EnumDataMapper
from CoreTypes import Building, Religion, Wonder


RELIGION_PERSECUTION_ORDER = EnumDataMapper(
    {
        Religion.PROTESTANTISM: [
            Religion.CATHOLICISM,
            Religion.ISLAM,
            Religion.ORTHODOXY,
            Religion.JUDAISM,
        ],
        Religion.ISLAM: [
            Religion.CATHOLICISM,
            Religion.ORTHODOXY,
            Religion.PROTESTANTISM,
            Religion.JUDAISM,
        ],
        Religion.CATHOLICISM: [
            Religion.ISLAM,
            Religion.PROTESTANTISM,
            Religion.JUDAISM,
            Religion.ORTHODOXY,
        ],
        Religion.ORTHODOXY: [
            Religion.ISLAM,
            Religion.JUDAISM,
            Religion.CATHOLICISM,
            Religion.PROTESTANTISM,
        ],
        Religion.JUDAISM: [
            Religion.ISLAM,
            Religion.PROTESTANTISM,
            Religion.ORTHODOXY,
            Religion.CATHOLICISM,
        ],
    }
)
RELIGIOUS_BUILDINGS = EnumDataMapper(
    {
        Religion.PROTESTANTISM: [
            Building.PROTESTANT_TEMPLE,
            Building.PROTESTANT_SCHOOL,
            Building.PROTESTANT_CATHEDRAL,
        ],
        Religion.ISLAM: [
            Building.ISLAMIC_TEMPLE,
            Building.ISLAMIC_CATHEDRAL,
            Building.ISLAMIC_MADRASSA,
        ],
        Religion.CATHOLICISM: [
            Building.CATHOLIC_TEMPLE,
            Building.CATHOLIC_MONASTERY,
            Building.CATHOLIC_CATHEDRAL,
        ],
        Religion.ORTHODOXY: [
            Building.ORTHODOX_TEMPLE,
            Building.ORTHODOX_MONASTERY,
            Building.ORTHODOX_CATHEDRAL,
        ],
        Religion.JUDAISM: [
            Building.JEWISH_QUARTER,
            Wonder.KAZIMIERZ,
        ],
    }
)
RELIGIOUS_WONDERS = [
    Wonder.MONASTERY_OF_CLUNY,
    Wonder.WESTMINSTER,
    Wonder.KRAK_DES_CHEVALIERS,
    Wonder.NOTRE_DAME,
    Wonder.PALAIS_DES_PAPES,
    Wonder.ST_BASIL,
    Wonder.SOPHIA_KIEV,
    Wonder.ST_CATHERINE_MONASTERY,
    Wonder.SISTINE_CHAPEL,
    Wonder.JASNA_GORA,
    Wonder.MONT_SAINT_MICHEL,
    Wonder.BOYANA_CHURCH,
    Wonder.FLORENCE_DUOMO,
    Wonder.BORGUND_STAVE_CHURCH,
    Wonder.DOME_ROCK,
    Wonder.THOMASKIRCHE,
    Wonder.BLUE_MOSQUE,
    Wonder.SELIMIYE_MOSQUE,
    Wonder.MOSQUE_OF_KAIROUAN,
    Wonder.KOUTOUBIA_MOSQUE,
    Wonder.LA_MEZQUITA,
    Wonder.SAN_MARCO,
    Wonder.STEPHANSDOM,
    Wonder.ROUND_CHURCH,
]
