#!/bin/bash

black .
flake8 --config flake8.cfg
python3 -m unittest

for f in build dist *.egg-info; do 
    echo remove $f
    rm $f -rf
done

    
