### Deep learning over perturbed data ###
	A. Perturb training and testing csv files with 1) Block-wise RMT 2) Permutation 3) Random Additive Perturbation
	B. Run the MNIST CNN over different block sizes and noise levels

### Dependencies ###
	numpy
	pandas
	TensorFlow

### Dataset ###
  download ubyte.gz files from http://yann.lecun.com/exdb/mnist/
	------------------------------
  Run: python read_mnist.py from ./datasets/

### Individual Program Flows ###
	A. Perturbation flow --- > Disguising training and testing images
	------------------------------
		Run: python ./Perturb/main.py data_path/data_name image_size block_size noise_level \
    RMT_type
		-
		Example: python ./Perturb/main.py ./dataset/mnist 28 28 4 4 10.0 orthogonal
		-
		Outputs: data_name_{train/test}_${noise}_${block_dim}_${block_dim}.csv 
    
    ** there is no padding so ensure the image size is a multiple of block_size
	-------------------------------
	B. DNN over Disguised Images
	-------------------------------
		Run: python ./models/conv_simple.py training_csv testing_csv
		-
		Example: python ./models/conv_simple.py fashion_train.csv fashion_test.csv
		Example: python ./models/conv_simple.py train_10.0_4.csv test_10.0_4.csv

		Generates a file called submission.csv
		
    Run: python ./models/test_results.py

    Produces the test results corect/total

### Model Quality and Visual Re-identification Experiments###
	-------------------------------
  Run: sh ./run_all_deep.sh
	-------------------------------
  
    For different block sizes:
        For different noise levels:
            Perturbation flow for MNIST
            for 5 times:
              train on disguised_images test on disguised images (model quality)
              train on untransformed images test on disguised images (visual re-identification attack)

  The results for model quality are sequntially written on ./out/org_on_org.csv
  The results for visual re-identification attack sequentially written on ./out/org_on_pert.csv 

### Class-membership Attack Experiment ###
	-------------------------------
  A. Generate class_wise test data (the target class images)
	-------------------------------
    Run: python ./class_membership/class_wise_test.py ./datasets/{mnist/fashion}_test.csv \
      ./datasets/{mnist/fashion}_test_labels.csv

	-------------------------------
  B. Run the class-membershp attacks
	-------------------------------
    On untransformed MNIST model
    Run: sh ./run_model_dist.sh

    On transformed MNIST model
    Run: sh ./run_model_dist_pert.sh
      
    Outputs: The model predictions for each class is written to
    ./datasets/class_outputs/class_outputs_i for class i

    These distributions can be analyzed for entropy/fano factor computation
    


