# RFCEurope

This repository contains a fork of the mod `RFCEurope` for Civilization IV: Beyond the Sword, based on the popular Rhye's and Fall of Civilization mod.

This fork enhances the original mod with minor changes and the following changes:

- add [Advanced Combat Odds](https://forums.civfanatics.com/threads/pieceofminds-advanced-combat-odds.310415/) mod (v2.01)
- add [Blue Marble](https://www.civfanatics.net/bluemarble/content/index.php) mod (v4.50)
- add [RFC DoC soundtrack](https://github.com/dguenms/DoC-Soundtrack/) for middle east civilizations

More information about the original mod can be found on the [CivFanatics forum](https://forums.civfanatics.com/forums/rhyes-and-fall-europe.386/).

Check the file [`ChangeLog.txt`](https://github.com/VDuchauffour/RFCEurope/blob/main/ChangeLog.txt) for all modifications.

## ️⚙️ Installation

Clone this repository into your mod folder (`Beyond the Sword/Mods/`).
You can also download a zip archive in the [release section](https://github.com/VDuchauffour/RFCEurope/releases).

You can still access SVN revisions using the `original` branch of the repository.

## ⛏️ Development

All contribution are welcome!

To ensure that you follow the development workflow, please setup the pre-commit hooks:

```shell
pre-commit install
```

To interact with all existing Python modules, use the following command to populate the `PYTHONPATH` of your Python interpreter (relative to the project root):

```shell
export PYTHONPATH=$(./export-paths.sh)
```

The Python version used by the in-game interpreter is `2.4.1`.

## Acknowledgements

- [Dawn of Civilization:](https://github.com/dguenms/Dawn-of-Civilization) Some data structures and project logics are taken from this excellent mod!
