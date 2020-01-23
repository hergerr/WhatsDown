#!/bin/bash

set -e
cd e2e_tests

for f in *.py; do
  python3 "$f"
done