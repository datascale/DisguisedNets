#!/bin/bash
KK=(7)
NL=(100.0)

for noise in "${NL[@]}"
  do
  for k in "${KK[@]}"
  do
    python ./Perturb/main.py ./datasets/mnist 28 28 $k $k $noise orthogonal
    python ./models/conv_simple.py ./mnist_train_${noise}_${k}_${k}.csv \
    ./mnist_test_${noise}_${k}_${k}.csv
    for i in {0..9}
    do
        python ./models/conv_simple_test.py ./mnist_train_${noise}_${k}_${k}.csv \
        ./datasets/class_subsets/test_class_${i}
        cp ./submission.csv ./datasets/class_outputs/class_outputs_${i}
    done
  done
  done



