#!/bin/zsh
cd `dirname $0`
cd ../test
source ~/mambaforge/etc/profile.d/conda.sh
conda activate
python test_model.py