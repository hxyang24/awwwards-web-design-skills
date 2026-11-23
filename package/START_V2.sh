#!/bin/sh
set -eu
cd "$(dirname "$0")/v2"
exec node server.mjs
