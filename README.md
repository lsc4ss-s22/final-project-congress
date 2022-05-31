## Workflow
1. Scrape and clean congressional record: Code can be found in [scrape_cr.py](https://github.com/lsc4ss-s22/final-project-congress/blob/master/scrape_cr.py). My goal is to parallelize the scraping and cleaning process.

Locally, run:

```python3 scrape_cr.py```

Senate record from 2019 will be stored in ```senate_speech (1).json```
Senate record from 2020 will be stored in ```senate_speech (2).json```
House record from 2019-2020 will be stored in ```house_speech.json```

All the json files map a speaker to his/her speeches in congressional record from 2019-2020

2. Merge speech dataset and LES dataset: Code and output can be found in [1_merge_speech_and_LES.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/1_merge_speech_and_LES.ipynb).

3. Upload the merged dataset to s3: Code and output can be found in [2_upload_to_S3.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/2_upload_to_S3.ipynb).

4. Topic modelling using pyspark and spark nlp: Code and output can be found in [3_topic_model.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/3_topic_model.ipynb).

5. Construct issue-based congressional networks: Code, output, and analysis can be found in [4_construct_network.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/4_construct_network.ipynb).

6. Regression analysis: Code, output, and analysis can be found in [5_analysis.pdf](https://github.com/lsc4ss-s22/final-project-congress/blob/master/5_analysis.pdf).
