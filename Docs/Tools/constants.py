# Copy of Assets/Python/Consts.py
name_civ = [
    "Byzantium",
    "Franks",
    "Arabs",
    "Bulgaria",
    "Cordoba",
    "Venice",
    "Burgundy",
    "Germany",
    "Novgorod",
    "Norway",
    "Kiev,",
    "Hungary",
    "Spain",
    "Denmark",
    "Scotland",
    "Poland",
    "Genoa",
    "Morocco",
    "England",
    "Portugal",
    "Aragon",
    "Sweden",
    "Prussia",
    "Lithuania",
    "Austria",
    "Ottomans",
    "Moscow",
    "Netherlands",
    "Pope",
]

capitals = (  # for RiseAndFall
    (81, 24),  # Constantinople, Byzantium
    (44, 46),  # Paris, France
    (97, 10),  # Damascus, Arabia
    (78, 29),  # Preslav, Bulgaria
    (30, 23),  # Cordoba, Cordoba
    (56, 35),  # Venice, Venezia
    (47, 41),  # Dijon, Burgundy
    (53, 46),  # Frankfurt, Germany
    (80, 62),  # Novgorod, Novgorod
    (57, 65),  # Tonsberg, Norway
    (83, 45),  # Kiev, Kiev
    (66, 37),  # Buda, Hungary
    (27, 32),  # Leon, Spain
    (59, 57),  # Roskilde, Denmark
    (37, 63),  # Edinburgh, Scotland
    (65, 49),  # Poznan, Poland
    (50, 34),  # Genoa, Genoa
    (24, 7),  # Marrakesh, Morocco
    (41, 52),  # London, England
    (21, 25),  # Lisboa, Portugal
    (36, 29),  # Zaragoza, Aragon
    (66, 64),  # Stockholm, Sweden
    (69, 53),  # Königsberg, Prussia
    (75, 53),  # Vilnius, Lithuania
    (62, 40),  # Wien, Austria
    (78, 22),  # Gallipoli, Ottomans
    (91, 56),  # Moscow, Moscow
    (49, 52),  # Amsterdam, Dutch
    (56, 27),  # Rome, Pope
)

core_areas_tl = (
    (66, 14),  # Byzantium
    (42, 43),  # Franks
    (92, 0),  # Arabs
    (74, 27),  # Bulgaria
    (24, 19),  # Cordoba
    (55, 33),  # Venice
    (44, 32),  # Burgundy
    (51, 40),  # Germany
    (79, 59),  # Novgorod
    (53, 63),  # Norway
    (79, 42),  # Kiev
    (64, 33),  # Hungary
    (25, 30),  # Spain
    (54, 55),  # Denmark
    (35, 62),  # Scotland
    (64, 43),  # Poland
    (49, 27),  # Genoa
    (18, 3),  # Morocco
    (37, 48),  # England
    (21, 24),  # Portugal
    (35, 26),  # Aragon
    (61, 60),  # Sweden
    (70, 52),  # Prussia
    (72, 51),  # Lithuania
    (59, 37),  # Austria
    (76, 16),  # Ottomans
    (84, 53),  # Moscow
    (46, 50),  # Netherlands
    (54, 25),  # Pope
)
core_areas_br = (
    (84, 26),  # Byzantium
    (46, 48),  # Franks
    (99, 12),  # Arabs
    (80, 30),  # Bulgaria
    (37, 28),  # Cordoba
    (59, 36),  # Venice
    (48, 42),  # Burgundy
    (58, 50),  # Germany
    (82, 69),  # Novgorod
    (59, 72),  # Norway
    (88, 50),  # Kiev
    (73, 39),  # Hungary
    (32, 36),  # Spain
    (64, 61),  # Denmark
    (39, 68),  # Scotland
    (70, 50),  # Poland
    (52, 35),  # Genoa
    (31, 16),  # Morocco
    (43, 60),  # England
    (24, 32),  # Portugal
    (42, 31),  # Aragon
    (65, 70),  # Sweden
    (71, 58),  # Prussia
    (80, 56),  # Lithuania
    (62, 44),  # Austria
    (84, 22),  # Ottomans
    (97, 59),  # Moscow
    (52, 55),  # Netherlands
    (58, 29),  # Pope
)
# extra_plots for core area
extra_plots = [
    [],  # Byzantium
    [],  # Frankia
    [],  # Arabia
    [],  # Bulgaria
    [
        (26, 15),
        (26, 16),
        (26, 17),
        (26, 18),
        (27, 15),
        (27, 16),
        (27, 17),
        (27, 18),
        (28, 15),
        (28, 16),
        (28, 17),
        (28, 18),
        (29, 15),
        (29, 16),
        (29, 17),
        (29, 18),
    ],  # Cordoba
    [(60, 33), (60, 34), (60, 35)],  # Venice
    [(49, 39), (49, 40), (49, 41), (49, 42)],  # Burgundy
    [],  # Germany
    [(78, 59), (78, 60)],  # Novgorod
    [],  # Norway
    [],  # Kiev
    [],  # Hungary
    [],  # Spain
    [],  # Denmark
    [(37, 69), (38, 69)],  # Scotland
    [(63, 46), (63, 47), (63, 48), (63, 49), (63, 50)],  # Poland
    [],  # Genoa
    [],  # Morocco
    [
        (37, 46),
        (37, 47),
        (38, 46),
        (38, 47),
        (39, 46),
        (39, 47),
        (40, 46),
        (40, 47),
        (41, 46),
        (41, 47),
        (42, 47),
    ],  # England		3Miro: Calais shouldn't flip to them on spawn
    [(25, 27), (25, 28), (25, 29), (25, 30), (25, 31)],  # Portugal
    [(40, 23), (42, 23), (42, 24), (44, 24)],  # Aragon
    [
        (60, 61),
        (60, 62),
        (60, 63),
        (61, 71),
        (62, 71),
        (62, 72),
        (63, 71),
        (63, 72),
        (64, 71),
        (64, 72),
        (65, 71),
        (65, 72),
        (66, 64),
        (66, 65),
        (66, 66),
        (66, 72),
        (68, 65),
        (70, 67),
        (70, 68),
        (71, 66),
        (71, 67),
        (71, 68),
        (72, 65),
        (72, 66),
        (72, 67),
    ],  # Sweden
    [
        (68, 51),
        (68, 52),
        (68, 53),
        (69, 51),
        (69, 52),
        (69, 53),
        (70, 51),
        (71, 59),
        (72, 57),
        (72, 58),
        (73, 57),
        (73, 58),
        (74, 57),
        (74, 58),
        (74, 59),
        (74, 60),
        (75, 57),
        (75, 58),
        (75, 59),
        (75, 60),
        (76, 58),
        (76, 59),
        (76, 60),
    ],  # Prussia
    [(76, 57), (77, 57), (78, 57), (79, 57), (80, 57)],  # Lithuania
    [(60, 36), (61, 36)],  # Austria
    [(76, 23), (77, 23), (78, 23), (79, 23)],  # Ottomans
    [
        (83, 53),
        (83, 54),
        (83, 55),
        (83, 56),
        (83, 57),
        (87, 60),
        (88, 60),
        (89, 60),
        (90, 60),
        (91, 60),
        (92, 60),
        (93, 60),
        (94, 60),
        (95, 60),
        (96, 60),
        (97, 60),
        (88, 61),
        (89, 61),
        (90, 61),
        (91, 61),
        (92, 61),
        (93, 61),
        (94, 61),
        (95, 61),
        (96, 61),
        (97, 61),
        (88, 62),
        (89, 62),
        (90, 62),
        (91, 62),
        (92, 62),
        (93, 62),
        (94, 62),
        (95, 62),
        (96, 62),
        (97, 62),
        (88, 63),
        (89, 63),
        (90, 63),
        (91, 63),
        (92, 63),
        (93, 63),
        (94, 63),
        (95, 63),
        (96, 63),
        (97, 63),
    ],  # Moscow
    [(46, 49), (47, 49), (48, 49), (49, 49), (50, 49)],  # Dutch
    [],  # Pope
]
# NormalAreas: Normal Area is typically used for resurrection.
normal_areas_tl = (
    (66, 13),  # Byzantium
    (33, 32),  # Franks
    (53, 0),  # Arabs
    (72, 27),  # Bulgaria
    (43, 8),  # Cordoba
    (54, 32),  # Venice
    (45, 32),  # Burgundy
    (51, 43),  # Germany
    (77, 59),  # Novgorod
    (53, 63),  # Norway
    (78, 41),  # Kiev
    (63, 32),  # Hungary
    (25, 26),  # Spain
    (54, 55),  # Denmark
    (34, 63),  # Scotland
    (63, 43),  # Poland
    (49, 22),  # Genoa
    (18, 3),  # Morocco
    (32, 50),  # England
    (21, 21),  # Portugal
    (54, 16),  # Aragon
    (60, 59),  # Sweden
    (59, 48),  # Prussia
    (70, 51),  # Lithuania
    (57, 36),  # Austria
    (76, 14),  # Turks
    (83, 51),  # Moscow
    (47, 50),  # Netherlands
    (54, 25),  # Pope
)

normal_areas_br = (
    (75, 24),  # Byzantium
    (44, 46),  # Franks
    (99, 11),  # Arabs
    (80, 31),  # Bulgaria
    (52, 19),  # Cordoba
    (60, 37),  # Venice
    (49, 43),  # Burgundy
    (61, 54),  # Germany
    (88, 72),  # Novgorod
    (58, 72),  # Norway
    (91, 50),  # Kiev
    (77, 41),  # Hungary
    (34, 36),  # Spain
    (59, 61),  # Denmark
    (39, 69),  # Scotland
    (77, 50),  # Poland
    (52, 36),  # Genoa
    (27, 13),  # Morocco
    (43, 62),  # England
    (25, 32),  # Portugal
    (64, 26),  # Aragon
    (75, 72),  # Sweden
    (71, 55),  # Prussia
    (77, 63),  # Lithuania
    (63, 42),  # Austria
    (98, 27),  # Turks
    (98, 63),  # Moscow
    (52, 54),  # Netherlands
    (58, 29),  # Pope
)

# These plots are subtracted from the tNormalAreasTL+tNormalAreasBR rectangles.
normal_areas_substract = (
    (),  # Byzantium
    (
        (33, 32),
        (33, 33),
        (33, 34),
        (33, 35),
        (33, 36),
        (34, 32),
        (34, 33),
        (34, 34),
        (34, 35),
        (35, 32),
        (35, 33),
        (35, 34),
        (36, 32),
        (36, 33),
        (37, 32),
        (38, 32),
    ),  # Frankia
    (
        (73, 10),
        (74, 10),
        (75, 10),
        (76, 10),
        (87, 10),
        (87, 11),
        (88, 10),
        (88, 11),
        (89, 11),
    ),  # Arabia
    (),  # Bulgaria
    (),  # Cordoba
    (
        (54, 32),
        (54, 33),
        (54, 34),
        (55, 32),
        (55, 33),
        (55, 34),
        (56, 32),
        (56, 33),
        (56, 34),
        (57, 32),
        (57, 33),
        (58, 32),
        (59, 37),
        (60, 36),
        (60, 37),
    ),  # Venice
    ((49, 32), (49, 33), (49, 34), (49, 35), (49, 36)),  # Burgundy
    (
        (52, 51),
        (52, 52),
        (52, 53),
        (52, 54),
        (51, 51),
        (51, 52),
        (51, 53),
        (51, 54),
        (59, 48),
        (59, 49),
        (59, 50),
        (59, 51),
        (59, 52),
        (59, 53),
        (59, 54),
        (60, 48),
        (60, 49),
        (60, 50),
        (60, 51),
        (60, 52),
        (60, 53),
        (60, 54),
        (61, 48),
        (61, 49),
        (61, 50),
        (61, 51),
        (61, 52),
        (61, 53),
        (61, 54),
    ),  # Germany
    (
        (84, 59),
        (84, 60),
        (85, 59),
        (85, 60),
        (85, 61),
        (86, 59),
        (86, 60),
        (86, 61),
        (86, 62),
        (87, 59),
        (87, 60),
        (87, 61),
        (87, 62),
        (88, 59),
        (88, 60),
        (88, 61),
        (88, 62),
    ),  # Novgorod
    (),  # Norway
    ((87, 41), (88, 41), (89, 41), (90, 41), (91, 41)),  # Kiev
    (
        (63, 32),
        (63, 39),
        (63, 40),
        (63, 41),
        (64, 41),
        (72, 32),
        (73, 32),
        (74, 32),
        (75, 32),
        (75, 41),
        (76, 32),
        (76, 40),
        (76, 41),
        (77, 32),
        (77, 39),
        (77, 40),
        (77, 41),
    ),  # Hungary
    ((25, 26), (25, 27), (25, 28), (25, 29), (25, 30), (25, 31), (34, 36)),  # Spain
    (),  # Denmark
    ((34, 69),),  # Scotland
    ((63, 43), (63, 44), (63, 45), (64, 43), (64, 44), (65, 43)),  # Poland
    (),  # Genoa
    (),  # Morocco
    (
        (32, 55),
        (32, 56),
        (32, 57),
        (32, 58),
        (32, 59),
        (32, 60),
        (32, 61),
        (32, 62),
        (33, 56),
        (33, 57),
        (33, 58),
        (33, 59),
        (33, 60),
        (33, 61),
        (33, 62),
    ),  # England
    ((25, 21), (25, 22), (25, 23), (25, 24), (25, 25), (25, 26), (25, 32)),  # Portugal
    (),  # Aragon
    (
        (60, 59),
        (60, 60),
        (60, 61),
        (60, 70),
        (60, 71),
        (60, 72),
        (61, 59),
        (61, 60),
        (61, 72),
        (70, 59),
        (70, 60),
        (70, 61),
        (71, 59),
        (71, 60),
        (71, 61),
        (72, 59),
        (72, 60),
        (72, 61),
        (73, 59),
        (73, 60),
        (73, 61),
        (73, 62),
        (74, 59),
        (74, 60),
        (74, 61),
        (74, 62),
        (74, 63),
        (75, 59),
        (75, 60),
        (75, 61),
        (75, 62),
        (75, 63),
    ),  # Sweden
    (
        (59, 55),
        (60, 55),
        (61, 55),
        (63, 48),
        (63, 49),
        (63, 50),
        (64, 48),
        (64, 49),
        (64, 50),
        (65, 48),
        (65, 49),
        (65, 50),
        (66, 48),
        (66, 49),
        (66, 50),
        (67, 48),
        (67, 49),
        (67, 50),
        (68, 48),
        (68, 49),
        (68, 50),
        (69, 48),
        (69, 49),
        (69, 50),
        (70, 48),
        (70, 49),
        (70, 50),
        (71, 48),
        (71, 49),
        (71, 50),
        (71, 55),
    ),  # Prussia
    (
        (70, 51),
        (70, 52),
        (70, 53),
        (70, 54),
        (70, 55),
        (70, 59),
        (70, 60),
        (70, 61),
        (70, 62),
        (70, 63),
        (71, 51),
        (71, 52),
        (71, 53),
        (71, 54),
        (71, 60),
        (71, 61),
        (71, 62),
        (71, 63),
        (72, 51),
        (72, 60),
        (72, 61),
        (72, 62),
        (72, 63),
        (73, 63),
        (77, 59),
        (77, 60),
        (77, 61),
        (77, 62),
        (77, 63),
    ),  # Lithuania
    (
        (57, 36),
        (57, 37),
        (58, 36),
        (58, 37),
        (59, 36),
        (63, 36),
        (63, 37),
        (63, 38),
    ),  # Austria
    ((76, 27), (77, 27), (78, 27), (79, 27), (80, 27)),  # Turkey
    (
        (83, 59),
        (83, 60),
        (83, 61),
        (83, 62),
        (83, 63),
        (84, 61),
        (84, 62),
        (84, 63),
        (85, 62),
        (85, 63),
        (86, 63),
        (87, 63),
        (88, 63),
    ),  # Moscow
    ((51, 50), (52, 50)),  # Dutch
    (),
)

# BroaderAreas: Used in civ birth only
broader_areas_tl = (
    (68, 14),  # Byzantium
    (39, 41),  # France
    (92, 7),  # Arabia
    (71, 28),  # Bulgaria
    (24, 23),  # Cordoba
    (52, 29),  # Venice
    (42, 36),  # Burgundy
    (49, 41),  # Germany
    (77, 59),  # Novgorod
    (53, 63),  # Norway
    (81, 37),  # Kiev
    (64, 27),  # Hungary
    (23, 31),  # Spain
    (55, 55),  # Denmark
    (31, 57),  # Scotland
    (64, 42),  # Poland
    (45, 29),  # Genoa
    (11, 2),  # Morocco
    (38, 49),  # England
    (17, 27),  # Portugal
    (33, 25),  # Aragon
    (60, 58),  # Sweden
    (59, 49),  # Prussia
    (68, 45),  # Lithuania
    (56, 35),  # Austria
    (83, 17),  # Turkey
    (83, 51),  # Moscow
    (44, 47),  # Dutch
    (54, 25),  # Pope
)

broader_areas_br = (
    (83, 27),  # Byzantium
    (49, 51),  # France
    (99, 15),  # Arabia
    (80, 31),  # Bulgaria
    (34, 33),  # Cordoba
    (62, 39),  # Venice
    (52, 46),  # Burgundy
    (58, 51),  # Germany
    (89, 72),  # Novgorod
    (61, 72),  # Norway
    (91, 47),  # Kiev
    (74, 37),  # Hungary
    (33, 41),  # Spain
    (59, 60),  # Denmark
    (45, 69),  # Scotland
    (74, 52),  # Poland
    (55, 39),  # Genoa
    (29, 27),  # Morocco
    (48, 59),  # England
    (27, 37),  # Portugal
    (43, 34),  # Aragon
    (77, 72),  # Sweden
    (72, 55),  # Prussia
    (82, 64),  # Lithuania
    (66, 45),  # Austria
    (93, 27),  # Turkey
    (93, 61),  # Moscow
    (54, 57),  # Dutch
    (58, 29),  # Pope
)
