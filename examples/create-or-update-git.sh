#!/usr/bin/env bash

DIRECTORY="$1"
URL="$2"
BRANCH="$3"
COMMIT="$4"

if [ -d "$DIRECTORY/.git" ]; then
    mkdir -p "$DIRECTORY"
    cd "$DIRECTORY"
    git fetch origin
    git reset --hard origin/master
else
    git clone "$URL" "$DIRECTORY"
fi
