"""This script converts old maps data from python file to csv."""
from pathlib import Path
import typer
import importlib
import importlib.util
import sys
import pandas as pd

app = typer.Typer()


def _load(path: str):
    path = Path(path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)
    return module


@app.command()
def convert_civ_dict(path: str, object: str, upside_down: bool = False):
    with pd.ExcelWriter(f"Assets/Maps/{object}.ods", engine="odf") as writer:
        module = _load(path)
        for civ, data in getattr(module, object).items():
            data = pd.DataFrame(data)
            if upside_down:
                data = data.iloc[::-1]
            # data = data.replace("-1", "").replace(-1, "")
            data.to_excel(writer, sheet_name=civ.name.capitalize())
            # csv_destination = Path(f"Assets/Maps/{object}")
            # csv_destination.mkdir(exist_ok=True)
            # data.to_csv(f"{csv_destination.as_posix()}/{civ.name.capitalize()}.csv", ",")


@app.command()
def convert_list(path: str, object: str, upside_down: bool = False):
    with pd.ExcelWriter(f"Assets/Maps/{object}.ods", engine="odf") as writer:
        module = _load(path)
        data = pd.DataFrame(getattr(module, object))
        if upside_down:
            data = data.iloc[::-1]
        data.to_excel(writer)


if __name__ == "__main__":
    app()
