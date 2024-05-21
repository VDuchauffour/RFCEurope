#!/bin/bash

for i in "$@"; do
    recode ISO-8859-1..html "$i"
    sd "&lt;" "<" "$i"
    sd "&gt;" ">" "$i"
    sd "&quot;" '"' "$i"
    sd "&apos;" "'" "$i"
    sd "&#13;" "" "$i"
    sd "&amp;" "&" "$i"
    sd "ISO-8859-1" "utf-8" "$i"
done
