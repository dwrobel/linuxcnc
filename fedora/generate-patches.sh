#!/usr/bin/bash

set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD)

rm -f *.patch 2>/dev/null

# where upstream/master is https://github.com/LinuxCNC/linuxcnc
git format-patch $(git merge-base upstream/master ${BRANCH})..${BRANCH}

num=1

for f in *.patch; do
    [ -f "$f" ] || continue
    p=${f#*-};
    mv $f linuxcnc-$f;
    printf "Patch%s:   %%{name}-%s\n" $num $f
    num=$((num + 1))
done
