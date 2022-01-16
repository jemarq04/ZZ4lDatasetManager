#!/bin/bash

python updateDatasets.py -i LooseLeptons.json -y 2016 -o LooseLeptons.json_updated --folder /data/hehe/2021_reprocess_signal16/,/data/hehe/2021_reprocess_minor16/
python updateDatasets.py -i LooseLeptons.json -y 2017 -o LooseLeptons.json_updated --folder /data/hehe/2021_reprocess_signal17/,/data/hehe/2021_reprocess_minor17/
python updateDatasets.py -i LooseLeptons.json -y 2018 -o LooseLeptons.json_updated --folder /data/hehe/2021_reprocess_signal18/,/data/hehe/2021_reprocess_minor18/
