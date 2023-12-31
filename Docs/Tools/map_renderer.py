import argparse
import re
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from random import randint

from PIL import Image, ImageOps

from constants import (
    broader_areas_br,
    broader_areas_tl,
    core_areas_br,
    core_areas_tl,
    extra_plots,
    name_civ,
    normal_areas_br,
    normal_areas_substract,
    normal_areas_tl,
)

DEFAULT_COLORS = {
    "peak": (84, 84, 84),
    "hill": (163, 125, 34),
    "ocean": (0, 0, 128),
    "coast": (0, 0, 255),
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
        return list(
            filter(lambda x: x is not None, set(plot.feature for plot in self.plots))
        )

    @property
    def all_terrains(self):
        return list(
            filter(lambda x: x is not None, set(plot.terrain for plot in self.plots))
        )

    @property
    def all_bonuses(self):
        return list(
            filter(lambda x: x is not None, set(plot.bonus for plot in self.plots))
        )


@dataclass
class ElementColor:
    element_name: str
    color_value: tuple[int, int, int]


class ColorsPicker:
    def __init__(self, map: CivIVMap):
        self.items = map.all_features + map.all_terrains + map.all_bonuses
        self.items += ["peak", "hill", "river"]
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
        self.base_img = Image.new("RGB", (self.map.width, self.map.height), (0, 128, 0))

    @staticmethod
    def draw(
        img: Image.Image, plots: list[Plot], color: tuple[int, int, int]
    ) -> Image.Image:
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
            plots = [
                plot for plot in self.map.plots if getattr(plot, condition) == pattern
            ]
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
        self.save_drawing(img, output_path, "base_map")

    def draw_rivers_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_plot_properties(img, "has_river")
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "rivers_map")

    def draw_features_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "feature", self.map.all_features)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "features_map")

    def draw_terrains_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "terrain", self.map.all_terrains)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "terrains_map")

    def draw_bonuses_map(self, output_path: str) -> None:
        img = self.base_img.copy()
        img = self.apply_water(img)
        img = self.draw_patterns_with_condition(img, "bonus", self.map.all_bonuses)
        img = self.upscale_map(img)
        self.save_drawing(img, output_path, "bonuses_map")

    def draw_spawning_map(self, output_path: str):
        assert (
            len(name_civ)
            == len(core_areas_tl)
            == len(core_areas_br)
            == len(extra_plots)
            == len(normal_areas_tl)
            == len(normal_areas_br)
            == len(broader_areas_tl)
            == len(broader_areas_br)
        )
        core_areas_ = [
            (bl[0], self.map.height - tr[1], tr[0], self.map.height - bl[1])
            for bl, tr in zip(core_areas_tl, core_areas_br)
        ]
        core_areas = []
        for i, country_area in enumerate(core_areas_):
            areas = list(
                product(
                    range(country_area[0], country_area[2]),
                    range(country_area[1], country_area[3]),
                )
            )
            core_areas.append(
                list(map(lambda p: Plot(p[0], p[1], "", "", "", "", ""), areas))
            )
            for plot in extra_plots[i]:
                try:
                    core_areas += Plot(plot[i][0], plot[i][1], "", "", "", "", "")
                except:
                    pass
        normal_areas_ = [
            (bl[0], self.map.height - tr[1], tr[0], self.map.height - bl[1])
            for bl, tr in zip(normal_areas_tl, normal_areas_br)
        ]
        normal_areas = []
        for i, country_area in enumerate(normal_areas_):
            areas = list(
                product(
                    range(country_area[0], country_area[2]),
                    range(country_area[1], country_area[3]),
                )
            )
            areas = [
                area
                for area in areas
                for s in normal_areas_substract[i]
                if area[0] != s[0] and area[1] != s[1]
            ]
            # l = [for s in normal_areas_substract[i]]
            # if s[0] != x and s[1] != y

            normal_areas.append(
                list(map(lambda p: Plot(p[0], p[1], "", "", "", "", ""), areas))
            )

        broader_areas_ = [
            (bl[0], self.map.height - tr[1], tr[0], self.map.height - bl[1])
            for bl, tr in zip(broader_areas_tl, broader_areas_br)
        ]
        broader_areas = []
        for i, country_area in enumerate(broader_areas_):
            areas = list(
                product(
                    range(country_area[0], country_area[2]),
                    range(country_area[1], country_area[3]),
                )
            )
            broader_areas.append(
                list(map(lambda p: Plot(p[0], p[1], "", "", "", "", ""), areas))
            )
        for i, country in enumerate(name_civ):
            img = self.base_img.copy()
            img = ImageOps.flip(img)
            img = self.draw(img, broader_areas[i], (230, 0, 200))
            img = self.draw(img, normal_areas[i], (200, 230, 0))
            img = self.draw(img, core_areas[i], (0, 200, 230))
            img = ImageOps.flip(img)
            img = self.apply_water(img)
            img = self.upscale_map(img)
            self.save_drawing(img, output_path + "/spawning_areas", f"{country}_map")

    def run(
        self,
        output_path: str,
        rivers: bool,
        features: bool,
        terrains: bool,
        bonuses: bool,
        spawning: bool,
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
        if spawning:
            self.draw_spawning_map(output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", action="store", type=str, help="WBSave to convert."
    )
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
        "--spawning",
        action="store_true",
        default=True,
        help="Draw spawning map. Default to True",
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
        args.spawning = True

    parser = WBSaveParser()
    map = parser.parse(args.file)
    renderer = MapRenderer(map, args.output_format)
    renderer.run(
        args.destination,
        args.rivers,
        args.features,
        args.terrains,
        args.bonuses,
        args.spawning,
    )


if __name__ == "__main__":
    main()
