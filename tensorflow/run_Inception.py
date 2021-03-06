#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: run_Inception.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 09-07-2018
#  Last Modified: Wed Sep 12 21:07:06 2018
#
#  Usage: python run_Inception.py
#  Description:
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

import time
import subprocess
import shlex

#Multiple GPUs used in the experiment. 
gpu_set = ['0', '1']

#For car196 dataset
parameter_set = [
                '--normed_test --alpha=1.0 --learning_rate=0.004 --optimizer=SGD ', #Softmax baseline
                '--normed_test --alpha=1.0 --learning_rate=0.004 --optimizer=SGD --label_smoothing', #Similar to No-Fuss static anchor setting
                '--bn --norm_weights --normed_test --alpha=16.0 --learning_rate=0.004 --optimizer=SGD', #BN
                '--bn --norm_weights --normed_test --alpha=16.0 --learning_rate=0.004 --optimizer=SGD\
                        --heat_up --nb_hu_epoch=20', #Heated-up BN
                '--l2_norm --norm_weights --normed_test --alpha=16.0 --learning_rate=0.004 --optimizer=SGD', #L2Norm
                '--l2_norm --norm_weights --normed_test --alpha=16.0 --learning_rate=0.004 --optimizer=SGD\
                        --heat_up --nb_hu_epoch=20', #Heated_up L2Norm
                ]

#for bird200 dataset
#parameter_set = [
#                '--dataset=bird200 --normed_test --alpha=1.0 \
#                        --learning_rate=0.004 --optimizer=SGD ', #Softmax baseline
#
#                '--dataset=bird200 --normed_test --alpha=1.0 --learning_rate=0.004 \
#                        --optimizer=SGD --label_smoothing', #Similar to No-Fuss static anchor
#
#                '--dataset=bird200 --bn --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.004 --optimizer=SGD', #BN
#
#                '--dataset=bird200 --bn --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.004 --optimizer=SGD --heat_up --nb_hu_epoch=20', #Heated-up BN
#                        
#                '--dataset=bird200 --l2_norm --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.004 --optimizer=SGD', #L2Norm
#
#                '--dataset=bird200 --l2_norm --norm_weights --normed_test --alpha=16.0 --learning_rate=0.004 \
#                        --optimizer=SGD --heat_up --nb_hu_epoch=20', #Heated_up L2Norm
#                ]

#for ebay dataset, need --fast_kmeans to speedup the clustering evaluation.
#parameter_set = [
#                '--dataset=ebay --normed_test --alpha=1.0 --learning_rate=0.01 \
#                       --optimizer=ADAM --better_init --fast_kmeans ', #Softmax baseline
#
#                '--dataset=ebay --normed_test --alpha=1.0 --learning_rate=0.01 \
#                        --optimizer=ADAM --better_init --fast_kmeans --label_smoothing', #Similar to No-Fuss static anchor
#
#                '--dataset=ebay --bn --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.01 --optimizer=ADAM --better_init --fast_kmeans', #BN
#
#                '--dataset=ebay --bn --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.01 --optimizer=ADAM --better_init \
#                        --fast_kmeans --heat_up --nb_hu_epoch=20', #Heated-up BN
#                        
#                '--dataset=ebay --l2_norm --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.01 --optimizer=ADAM --better_init --fast_kmeans', #L2Norm
#
#                '--dataset=ebay --l2_norm --norm_weights --normed_test --alpha=16.0 \
#                        --learning_rate=0.01 --optimizer=ADAM --better_init \
#                        --fast_kmeans --heat_up --nb_hu_epoch=20', #Heated_up L2Norm
#                ]

number_gpu = len(gpu_set)
process_set = []

for idx, parameter in enumerate(parameter_set):
    print('Test Parameter: {}'.format(parameter))
    command = 'python ./tensorflow/deep_metric_learning_Inception.py --data_dir=./data/ \
            --nb_epoch 80 {} --log_dir=./Inception_log/ --data_augment --gpu-id {} \
            '.format(parameter, gpu_set[idx%number_gpu])

    print(command)
    p = subprocess.Popen(shlex.split(command))
    process_set.append(p)
    
    if (idx+1)%number_gpu == 0:
        print('Wait for process end')
        for sub_process in process_set:
            sub_process.wait()
    
        process_set = []

    time.sleep(60)

for sub_process in process_set:
    sub_process.wait()
