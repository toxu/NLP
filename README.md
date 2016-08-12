# Distinguish english words and pinyin

Requirement: python 2.7

1. train the classifier
  python classify.py train [-s] configure-file

2. run the task
  python classify.py run [-s] configure-file

  you can find the result in output folder
  
3. run the benchmark
  python classify.py benchmark [-s] configure-file

The configure-file is optional, if not provided, the default.json in config folder will be used.

For more details, please use python classify.py -h
