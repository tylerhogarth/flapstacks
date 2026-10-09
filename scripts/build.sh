#!/usr/bin/env sh
# Build the deployable tree: dist/server.mjs plus dist/public/ holding the site.
set -eu
cd "$(dirname "$0")/.."
rm -rf dist
mkdir -p dist/public
bun build app/server.ts --target bun --format esm --outfile dist/server.mjs
cp index.html favicon.ico site.webmanifest dist/public/
cp -R assets dist/public/assets
echo "built dist/"
