#!/bin/bash
KK=(7)
NL=(100.0)

for noise in "${NL[@]}"
  do
  for k in "${KK[@]}"
  do
    python ./models/conv_simple.py ./datasets/mnist_train.csv \
    ./datasets/mnist_test.csv
    for i in {0..9}
    do
        python ./models/conv_simple_test.py ./datasets/mnist_train.csv \
        ./datasets/class_subsets/test_class_${i}
        cp ./submission.csv ./datasets/class_outputs/class_outputs_${i}
    done
  done
  done



