#!/bin/bash

# prevents from error stacking
set -e

pip3 install -r requirements.txt
flask db upgrade
