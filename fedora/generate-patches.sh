#!/usr/bin/bash

set -e

rm -f *.patch 2>/dev/null
git format-patch origin/master

num=1

for f in *.patch; do
    p=${f#*-};
    mv $f machinekit-$f;
    echo -e "Patch${num}:\t\t%{name}-$f"
    num=$((num + 1))
done
