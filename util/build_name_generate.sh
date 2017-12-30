#!/bin/bash

LATEST_TAG=$(curl -s https://api.github.com/repos/agrrh/vscalectl/tags | jq -r '.[0]["name"]')
LATEST_SHA=$(curl -s https://api.github.com/repos/agrrh/vscalectl/commits | jq -r '.[0]["sha"]' | head -c 8)

# ex. v1.0.1-alpha
VERSION_API=$(echo -n ${LATEST_TAG} | cut  -d '.' -f1)
VERSION_MAJOR=$(echo -n ${LATEST_TAG} | cut  -d '.' -f2)
VERSION_MINOR=$(echo -n ${LATEST_TAG} | cut  -d '-' -f1 | cut  -d '.' -f3)

NEW_MINOR=$[${VERSION_MINOR}+1]

NEW_TAG="${VERSION_API}.${VERSION_MAJOR}.${NEW_MINOR}"

export VSCALECTL_BUILD="vscalectl-${NEW_TAG}-pre-${LATEST_SHA}"

echo ${VSCALECTL_BUILD}
