# -*- coding: utf-8 -*-
"""Conversational Analysis with GPT-2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e_1zWG9M0dIJcRn7hwCpjRREKzTsoO7i
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import json
import random
import re
import pandas as pd
from numpy import int64

!git clone https://github.com/tenoke/gpt-2

os.chdir('gpt-2')

!pip3 install -r requirements.txt

!mkdir .kaggle

ls

token = {"username":"xianshou","key":"9df2f9227d52fa331b2ea240826b976f"}
with open('/content/gpt-2/.kaggle/kaggle.json', 'w') as file:
    json.dump(token, file)

!cp /content/gpt-2/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle config set -n path -v{/content}

!chmod 600 /root/.kaggle/kaggle.json

!kaggle datasets download -d rtatman/ubuntu-dialogue-corpus -p /content/gpt-2 --force

!unzip ubuntu-dialogue-corpus.zip

#By and large if we want to use all datasets - uncomment as necessary.
#For this instance I have only used dialogueText_301.csv

#dialogue_1 = 'Ubuntu-dialogue-corpus/dialogueText.csv'
#dialogue_2 = 'Ubuntu-dialogue-corpus/dialogueText_196.csv'
dialogue_3 = 'Ubuntu-dialogue-corpus/dialogueText_301.csv'

#d1_df = pd.read_csv(dialogue_1, parse_dates=['date'], chunksize=1200000)
#d2_df = pd.read_csv(dialogue_2, parse_dates=['date'], chunksize=1200000)
d3_df = pd.read_csv(dialogue_3, parse_dates=['date'], chunksize=1200000)

!python download_model.py 345M

!mkdir ubuntu-data ubuntu-npz

#function creates a processed version of the csv
#extracting the content we need: date, sender, message
def clean(dataset, file_name):
  i = 1
  for data in dataset:    
    text_corpus = ''
    current = None
    for msg in data.itertuples():
      if msg.dialogueID != current:
        current = msg.dialogueID
        text_corpus += '\n\n'
      try: 
        text_corpus += f"({msg.date}) {msg._4}: {msg.text}\n"
      except KeyError:
        pass
    
    
    with open(f'ubuntu-data/{file_name}_{i}.txt', 'w') as f:
      f.write(text_corpus)  
    del(text_corpus)
    i += 1

#We only read the d3_df so we are only cleaning that file
#clean(d1_df, 'cleaned_d1_df')
#(d2_df, 'cleaned_d2_df')
clean(d3_df, 'cleaned_d3_df')

#Encoding processed files generated from the csv as necessary
#to find this file I used the 'ls' command
#after changing to the appropriate directory
#As it stands I'm only working with the output from clean(d3_df, 'cleaned_d3_df')
#Uncomment the other lines as necessary
 
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d1_df_1.txt ubuntu-npz/cleaned_d1_df_1.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_1.txt ubuntu-npz/cleaned_d2_df_1.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_2.txt ubuntu-npz/cleaned_d2_df_2.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_3.txt ubuntu-npz/cleaned_d2_df_3.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_4.txt ubuntu-npz/cleaned_d2_df_4.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_5.txt ubuntu-npz/cleaned_d2_df_5.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_6.txt ubuntu-npz/cleaned_d2_df_6.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_7.txt ubuntu-npz/cleaned_d2_df_7.txt.npz --model_name 345M
#!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d2_df_8.txt ubuntu-npz/cleaned_d2_df_8.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_1.txt ubuntu-npz/cleaned_d3_df_1.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_2.txt ubuntu-npz/cleaned_d3_df_2.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_3.txt ubuntu-npz/cleaned_d3_df_3.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_4.txt ubuntu-npz/cleaned_d3_df_4.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_5.txt ubuntu-npz/cleaned_d3_df_5.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_6.txt ubuntu-npz/cleaned_d3_df_6.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_7.txt ubuntu-npz/cleaned_d3_df_7.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_8.txt ubuntu-npz/cleaned_d3_df_8.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_9.txt ubuntu-npz/cleaned_d3_df_9.txt.npz --model_name 345M
!PYTHONPATH=src ./encode.py ubuntu-data/cleaned_d3_df_10.txt ubuntu-npz/cleaned_d3_df_10.txt.npz --model_name 345M

!PYTHONPATH=src ./train.py --dataset ubuntu-npz/ --sample_every 250 --stop_after 1501 --model_name 345M  #default learning rate = 0.001

!PYTHONPATH=src ./train.py --dataset ubuntu-npz/ --sample_every 250 --learning_rate 0.00001 --stop_after 3501 --model_name 345M

!PYTHONPATH=src ./train.py --dataset ubuntu-npz/ --sample_every 250 --learning_rate 0.000001 --stop_after 5001 --model_name 345M

!python3 src/generate_unconditional_samples.py --top_k 40 --temperature 0.95 --model_name 345M

