#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

PATHS=(
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/data)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/utils)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/components)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/EntryPoints)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/pyWB)"
	"$(readlink -f "$SCRIPT_DIR"/Assets/Python/screens)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/EntryPoints)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyWB)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/Screens)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyUnit)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyHelper)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/PitBoss)"
	"$PYTHONPATH"
)

for path in "${PATHS[@]}"; do
	PYTHONPATH="$PYTHONPATH:$path"
done

echo "$PYTHONPATH"
