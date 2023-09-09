#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

export PYTHONPATH=$(
    tr -d $'\n ' <<<"
    $SCRIPT_DIR/Assets/Python:
    $SCRIPT_DIR/Assets/Python/models:
    $SCRIPT_DIR/Assets/Python/EntryPoints:
    $SCRIPT_DIR/Assets/Python/pyWB:
    $SCRIPT_DIR/Assets/Python/screens:
    $SCRIPT_DIR/../../Assets/Python:
    $SCRIPT_DIR/../../Assets/Python/EntryPoints:
    $SCRIPT_DIR/../../Assets/Python/pyWB:
    $SCRIPT_DIR/../../Assets/Python/Screens:
    $SCRIPT_DIR/../../Assets/Python/pyUnit:
    $SCRIPT_DIR/../../Assets/Python/pyHelper:
    $SCRIPT_DIR/../../Assets/Python/PitBoss:
    $PYTHONPATH"
)
