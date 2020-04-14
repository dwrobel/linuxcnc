#!/usr/bin/bash

set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD)

rm -f *.patch 2>/dev/null

git format-patch $(git merge-base upstream/master ${BRANCH})..${BRANCH}

num=1

for f in *.patch; do
    p=${f#*-};
    mv $f machinekit-$f;
    echo -e "Patch${num}:\t%{name}-$f"
    num=$((num + 1))
done
