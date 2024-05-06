#!/bin/bash

values=(
    "0 The_Byzantines"
    "1 The_French"
    "2 The_Arabs"
    "3 The_Bulgarians"
    "4 The_Cordobans"
    "5 The_Venetians"
    "6 The_Burgundians"
    "7 The_Germans"
    "8 The_Novgorodians"
    "9 The_Norwegians"
    "10 The_Kievans"
    "11 The_Hungarians"
    "12 The_Spanish"
    "13 The_Danish"
    "14 The_Scottish"
    "15 The_Polish"
    "16 The_Genoans"
    "17 The_Moroccans"
    "18 The_English"
    "19 The_Portuguese"
    "20 The_Aragonese"
    "21 The_Swedish"
    "22 The_Prussians"
    "23 The_Lithuanians"
    "24 The_Austrians"
    "25 The_Ottomans"
    "26 The_Muscovites"
    "27 The_Dutch"
    "28 The_Pope"
    "29 Independent_leader"
    "30 Independent_leader"
    "31 Independent_leader"
    "32 Independent_leader"
    "33 The_Barbarians"
)

for i in "${values[@]}"; do
    set -- $i
    name=$(echo "$2" | sd "_" " ")
    sd "TeamID=$1, \(\)" "TeamID=$1, ($name)" PrivateMaps/*
    sd "UnitOwner=$1, \(\)" "UnitOwner=$1, ($name)" PrivateMaps/*
    sd "CityOwner=$1, \(\)" "CityOwner=$1, ($name)" PrivateMaps/*
done
