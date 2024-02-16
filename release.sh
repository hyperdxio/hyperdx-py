#!/bin/bash

# extract version from pyproject.toml
VERSION=$(awk -F'=' '/^version/ {print $2}' pyproject.toml | tr -d ' "')

echo "Releasing version $VERSION"

# build the package
make build

# create a new github tag
git tag -a "v$VERSION" -m "release v$VERSION"

# push the tag to github
git push origin "v$VERSION"

# publish the package to pypi
make publish
