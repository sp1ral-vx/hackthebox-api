#!/bin/bash
VERSION=$1
rm -rf ./build ./dist ./hackthebox_api.egg-info

sed -i "s/VERSION = .*/VERSION = '${VERSION}'/" ./setup.py
python setup.py sdist
git add .
git commit -m "Release ${VERSION}"
git push
~/.virtualenvs/hackthebox-api/bin/twine upload dist/*

git tag "$VERSION" -m "Release ${VERSION}"
git push --tags origin master
