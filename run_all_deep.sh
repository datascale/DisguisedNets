#!/bin/bash

KK=(2 4 7 14 28)
NL=(0.0 25.0 50.0 100.0 200.0)

for noise in "${NL[@]}"
  do
  for k in "${KK[@]}"
  do
	python ./Perturb/main.py ./datasets/mnist 28 28 $k $k $noise orthogonal
    for i in {1..2}}
    do
        python ./models/conv_simple.py ./mnist_train_${noise}_${k}_${k}.csv \
        ./mnist_test_${noise}_${k}_${k}.csv
        python ./models/test_results.py ./datasets/mnist_test_labels.csv \
        >>./out/org_on_org.csv
        python ./models/conv_simple.py ./datasets/mnist_train.csv \
        ./mnist_test_${noise}_${k}_${k}.csv
        python ./models/test_results.py ./datasets/mnist_test_labels.csv \
        >>./out/org_on_pert.csv
    done
	  rm ./mnist_train_${noise}_${k}_${k}.csv
	  rm ./mnist_test_${noise}_${k}_${k}.csv
  done
  done



