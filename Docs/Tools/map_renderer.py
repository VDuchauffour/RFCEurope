from __future__ import annotations
from itertools import chain
import numpy as np
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from random import randint

from PIL import Image, ImageOps
from CoreData import civilizations

from LocationsData import CIV_CORE_AREA, CIV_BROADER_AREA, CIV_NORMAL_AREA
from CoreTypes import Civ, Province, ProvinceType
from MapsData import PROVINCES_MAP

PROVINCES_MAP = np.asarray(PROVINCES_MAP)
DEFAULT_COLORS = {
    "base": (175, 175, 175),  # (0, 128, 0),
    "peak": (34, 34, 34),
    "hill": (70, 70, 34),  # (163, 125, 34),
    "ocean": (50, 100, 100),  # (0, 0, 128),
    "coast": (50, 100, 100),  # (0, 0, 255),
    "river": (0, 140, 255),
    "grass": (0, 155, 55),
    "desert": (255, 255, 168),
    "ice": (255, 255, 255),
    "tundra": (192, 192, 192),
    "plains": (128, 128, 0),
    "forest": (0, 128, 128),
    "dense_forest": (0, 61, 61),
    "jungle": (19, 175, 0),
    "oasis": (192, 255, 255),
    "flood_plains": (192, 255, 0),
    "fallout": (32, 64, 0),
}
PROVINCES_COLORS = {
    "core": (41, 249, 255),  # (0, 100, 0),
    "historical": (8, 179, 69),  # (0, 255, 0),
    "potential": (253, 184, 51),  # (255, 255, 0),
    "contested": (255, 82, 82),
}


@dataclass
class Plot:
    x: int
    y: int
    plot_type: int
    river_direction: int | None
    terrain: str | None
    feature: str | None
    bonus: str | None

    @property
    def is_peak(self):
        return True if self.plot_type == 0 else False

    @property
    def is_hill(self):
        return True if self.plot_type == 1 else False

    @property
    def has_river(self):
        return True if self.river_direction is not None else False


@dataclass
class CivIVMap:
    width: int
    height: int
    plots: list[Plot]

    @property
    def all_features(self):
        return list(filter(lambda x: x is not None, set(plot.feature for plot in self.plots)))

    @property
    def all_terrains(self):
        return list(filter(lambda x: x is not None, set(plot.terrain for plot in self.plots)))

    @property
    def all_bonuses(self):
        return list(filter(lambda x: x is not None, set(plot.bonus for plot in self.plots)))


@dataclass
class ElementColor:
    element_name: str
    color_value: tuple[int, int, int]


class ColorsPicker:
    def __init__(self, map: CivIVMap):
        self.items = map.all_features + map.all_terrains + map.all_bonuses
        self.items += ["peak", "hill", "river", "base"]
        self.colors = self.init_colors()

    @staticmethod
    def generate_color():
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def init_colors(self):
        colors = {}
        for item in self.items:
            colors[item] = DEFAULT_COLORS.get(item, ColorsPicker.generate_color())
        return colors


class WBSaveParser:
    @staticmethod
    def parse_size(data: str):
        width = re.search(r"(?<=grid width=)\d+", data)
        height = re.search(r"(?<=grid height=)\d+", data)
        if width is not None and height is not None:
            width = int(width.group())
            height = int(height.group())
            return (width, height)
        else:
            raise ValueError("Error while parsing!")

    @staticmethod
    def parse_plots(plot: str):
        x = re.search(r"(?<=x=)\d+", plot)
        if x:
            x = int(x.group())
        y = re.search(r"(?<=y=)\d+", plot)
        if y:
            y = int(y.group())
        plot_type = re.search(r"(?<=PlotType=)\d+", plot)
        if plot_type:
            plot_type = int(plot_type.group())
        river_direction = re.search(r"(?<=River..Direction=)\d+", plot)
        if river_direction:
            river_direction = int(river_direction.group())
        terrain = re.search(r"(?<=TerrainType=TERRAIN_)\w+", plot)
        if terrain:
            terrain = terrain.group().lower()
        feature = re.search(r"(?<=FeatureType=FEATURE_)\w+", plot)
        if feature:
            feature = feature.group().lower()
        bonus = re.search(r"(?<=BonusType=BONUS_)\w+", plot)
        if bonus:
            bonus = bonus.group().lower()
        return Plot(x, y, plot_type, river_direction, terrain, feature, bonus)

    def parse(self, filename: str):
        data = Path(filename).read_text()
        width, height = self.parse_size(data)
        raw_plots = re.findall("BeginPlot(.*?)EndPlot", data, re.S)
        plots = list(map(WBSaveParser.parse_plots, raw_plots))
        return CivIVMap(width, height, plots)


class MapRenderer:
    def __init__(
        self,
        map: CivIVMap,
        output_format: str,
        upscale_factor: int = 15,
    ):
        self.map = map
        self.colors = ColorsPicker(map).colors
        self.output_format = output_format
        self.upscale_factor = upscale_factor
        self.base_img = Image.new(
            "RGB", (self.map.width, self.map.height), self.get_colors("base")
        )

    @staticmethod
    def draw(img: Image.Image, plots: list[Plot], color: tuple[int, int, int]) -> Image.Image:
        for plot in plots:
            img.putpixel((plot.x, plot.y), color)
        return img

    def get_colors(self, pattern: str) -> tuple[int, int, int]:
        return self.colors[pattern]

    def draw_plot_properties(self, img: Image.Image, properties: str) -> Image.Image:
        plots = [plot for plot in self.map.plots if getattr(plot, properties)]
        img = MapRenderer.draw(img, plots, self.get_colors(properties.split("_")[1]))
        return img

    def draw_patterns_with_condition(
        self, img: Image.Image, condition: str, patterns: list[str]
    ) -> Image.Image:
        for pattern in patterns:
            plots = [plot for plot in self.map.plots if getattr(plot, condition) == pattern]
            img = MapRenderer.draw(img, plots, self.get_colors(pattern))
        return img

    def apply_water(self, img: Image.Image) -> Image.Image:
        return self.draw_patterns_with_condition(img, "terrain", ["ocean", "coast"])

    def elevate(self, img: Image.Image) -> Image.Image:
        img = self.draw_plot_properties(img, "is_hill")
        img = self.draw_plot_properties(img, "is_peak")
        return img

    def upscale_map(self, img: Image.Image) -> Image.Image:
        img = ImageOps.flip(img)
        img = img.resize(
            (
                self.map.width * self.upscale_factor,
                self.map.height * self.upscale_factor,
            ),
            resample=Image.Resampling.NEAREST,
        )
        return img

    def save_drawing(self, img: Image.Image, output_path: str, name_map: str) -> None:
        _output_path = Path(output_path)
        if not _output_path.exists():
            _output_path.mkdir(parents=True, exist_ok=True)
        img.save(f"{_output_path.as_posix()}/{name_map}.{self.output_format}")

    def draw_base_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.elevate(img)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "base")

    def draw_rivers_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_plot_properties(img, "has_river")
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "rivers")

    def draw_features_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "feature", self.map.all_features)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "features")

    def draw_terrains_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "terrain", self.map.all_terrains)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "terrains")

    def draw_bonuses_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "bonus", self.map.all_bonuses)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "bonuses")

    def _extract_provinces(self, province):
        plots = []
        indices = np.where(PROVINCES_MAP == province.value)
        for y, x in zip(indices[0], indices[1]):
            plots.append(Plot(x, y, "", "", "", "", ""))
        return plots

    def extract_provinces(self, provinces):
        plots = []
        for province in provinces:
            plots.append(self._extract_provinces(province))
        plots = chain.from_iterable(plots)
        return plots

    def draw_provinces_map(self, output_path: str):
        for province in Province:
            img = self.base_img.copy()
            img = self.draw(
                img,
                self._extract_provinces(province),
                PROVINCES_COLORS["potential"],
            )

            img = self.apply_water(img)
            img = self.draw_plot_properties(img, "is_peak")
            img = self.upscale_map(img)
            self.save_drawing(img, output_path + "/provinces", f"{province.name}")

    def draw_provinces_stability_map(self, output_path: str):
        for civ in civilizations().main():
            img = self.base_img.copy()
            img = self.draw(
                img,
                self.extract_provinces(civ.location.provinces[ProvinceType.CORE]),
                PROVINCES_COLORS["core"],
            )
            img = self.draw(
                img,
                self.extract_provinces(civ.location.provinces[ProvinceType.HISTORICAL]),
                PROVINCES_COLORS["historical"],
            )
            img = self.draw(
                img,
                self.extract_provinces(civ.location.provinces[ProvinceType.POTENTIAL]),
                PROVINCES_COLORS["potential"],
            )
            img = self.draw(
                img,
                self.extract_provinces(civ.location.provinces[ProvinceType.CONTESTED]),
                PROVINCES_COLORS["contested"],
            )
            img = self.apply_water(img)
            img = self.draw_plot_properties(img, "is_peak")
            img = self.upscale_map(img)
            self.save_drawing(img, output_path + "/provinces_stability", f"{civ.key.name}")

    def normalize_plot(self, plots):
        _plots = []
        for plot in plots:
            _plots.append(Plot(plot.x, self.map.height - plot.y - 1, "", "", "", "", ""))
        return _plots

    def run(
        self,
        output_path: str,
        rivers: bool,
        features: bool,
        terrains: bool,
        bonuses: bool,
        provinces: bool,
        provinces_stability: bool,
    ) -> None:
        self.draw_base_map(output_path)
        if rivers:
            self.draw_rivers_map(output_path)
        if features:
            self.draw_features_map(output_path)
        if terrains:
            self.draw_terrains_map(output_path)
        if bonuses:
            self.draw_bonuses_map(output_path)
        if provinces:
            self.draw_provinces_map(output_path)
        if provinces_stability:
            self.draw_provinces_stability_map(output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store", type=str, help="WBSave to convert.")
    parser.add_argument(
        "-d", "--destination", action="store", type=str, help="Destination folder."
    )
    parser.add_argument(
        "--format",
        action="store",
        type=str,
        default="png",
        choices=["bmp", "png"],
        dest="output_format",
        help="File saving format, ie. bmp or png. Default to png",
    )
    parser.add_argument(
        "--rivers",
        action="store_true",
        default=False,
        help="Draw rivers map. Default to False.",
    )
    parser.add_argument(
        "--features",
        action="store_true",
        default=False,
        help="Draw features map. Default to False.",
    )
    parser.add_argument(
        "--terrains",
        action="store_true",
        default=False,
        help="Draw terrains map. Default to False.",
    )
    parser.add_argument(
        "--bonuses",
        action="store_true",
        default=False,
        help="Draw bonuses map. Default to False.",
    )
    parser.add_argument(
        "--provinces",
        action="store_true",
        default=False,
        help="Draw provinces map. Default to False",
    )
    parser.add_argument(
        "--provinces-stability",
        action="store_true",
        default=True,
        help="Draw provinces stability map. Default to True",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Draw all maps. Default to False.",
    )

    args = parser.parse_args()
    if args.all:
        args.rivers = True
        args.features = True
        args.terrains = True
        args.bonuses = True
        args.provinces = True
        args.provinces_stability = True

    parser = WBSaveParser()
    map = parser.parse(args.file)
    renderer = MapRenderer(map, args.output_format)
    renderer.run(
        args.destination,
        args.rivers,
        args.features,
        args.terrains,
        args.bonuses,
        args.provinces,
        args.provinces_stability,
    )


if __name__ == "__main__":
    main()
