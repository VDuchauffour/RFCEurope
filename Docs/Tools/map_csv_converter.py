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
def convert_civ_dict(path: str, destination_name: str, upside_down: bool = False):
    with pd.ExcelWriter(f"Assets/Maps/{destination_name}.ods", engine="odf") as writer:
        module = _load(path)
        for civ, data in getattr(module, destination_name).items():
            data = pd.DataFrame(data)
            if upside_down:
                data = data.iloc[::-1]
            # data = data.replace("-1", "").replace(-1, "")
            data.to_excel(writer, sheet_name=civ.name.capitalize())


@app.command()
def convert_list(path: str, destination_name: str, upside_down: bool = False):
    with pd.ExcelWriter(f"Assets/Maps/{destination_name}.ods", engine="odf") as writer:
        module = _load(path)
        data = pd.DataFrame(getattr(module, destination_name))
        if upside_down:
            data = data.iloc[::-1]
        data.to_excel(writer)


@app.command()
def convert_ods_to_csv(path: str, destination_name: str):
    df = pd.read_excel(path, engine="odf", sheet_name=None)
    for sheet, data in df.items():
        csv_destination = Path(f"Assets/Maps/{destination_name}")
        csv_destination.mkdir(exist_ok=True)
        data.to_csv(f"{csv_destination.as_posix()}/{sheet.capitalize()}.csv", ",")


if __name__ == "__main__":
    app()
