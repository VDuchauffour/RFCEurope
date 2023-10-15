#!/usr/bin/env bash

set -e

LOCAL_ONLY=false

usage() {
	echo "Usage: $0 [-l]" 1>&2
	exit 1
}
while getopts ':l' OPTION; do
	case "$OPTION" in
	l)
		LOCAL_ONLY=true
		;;
	*)
		usage
		;;
	esac
done

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

LOCAL_PATHS=(
	"$SCRIPT_DIR/Assets/Python"
	"$SCRIPT_DIR/Assets/Python/data"
	"$SCRIPT_DIR/Assets/Python/utils"
	"$SCRIPT_DIR/Assets/Python/models"
	"$SCRIPT_DIR/Assets/Python/components"
	"$SCRIPT_DIR/Assets/Python/EntryPoints"
	"$SCRIPT_DIR/Assets/Python/pyWB"
	"$SCRIPT_DIR/Assets/Python/screens"
)
EXTERNAL_PATHS=(
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/EntryPoints)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyWB)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/Screens)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyUnit)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/pyHelper)"
	"$(readlink -f "$SCRIPT_DIR"/../../Assets/Python/PitBoss)"
)
CURRENT_PYTHONPATHS=(
	"$PYTHONPATH"
)

fill_paths() {
	PATHS=("$@")
	for path in "${PATHS[@]}"; do
		_PYTHONPATH="$_PYTHONPATH:$path"
	done
}

fill_paths "${LOCAL_PATHS[@]}"

if [[ $LOCAL_ONLY == false ]]; then
	fill_paths "${EXTERNAL_PATHS[@]}"
fi

fill_paths "${CURRENT_PYTHONPATHS[@]}"

_PYTHONPATH=${_PYTHONPATH:1}
_PYTHONPATH=${_PYTHONPATH::-1}
echo "$_PYTHONPATH"
