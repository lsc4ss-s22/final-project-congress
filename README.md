# Large-Scale Computing Final Project: Issue-Based Congressional Network and Legislative Effectiveness
This is the GitHub repository for the final project of MACS 30123 (Spring 2022) Large Scale Computing. 


Author: Lynette Dang

## Social Science Questions
The US Congress is known for having increasing polarization and thus questionable effectiveness with regard to making and passing bills, approving presidential nominations, as well as budgeting. While studying legislative effectiveness, existing literature focuses on the important personal and institutional attributes such as race, gender, and ethnicity that make some Congressmen and Congresswomen more effective legislators than their peers. However, only a limited amount of attention has been directed to individual-based social networks within Congress. Can issue-oriented and committee-oriented cross-partisan social net- works help overcome congressional gridlocks and mitigate polarization? This paper seeks to investigate the impact of these two types of social networks on legislative effectiveness score[^1] of each legislator in the 116th Congress: How does issue-oriented cross-partisan social networks[^2] and committee-oriented cross-partisan social networks affect legislative effectiveness of each legislator in the 116th? Which type of networks has a larger impact on legislative effectiveness? I believe by examining these two types of social networks and their effect on legislative effectiveness, we are one step closer to understanding legislative bargaining, policy making, and political representation on a federal level. Note that I am also proposing to do the same project (or parts of it) for my perspectives and social network analysis class. 

Currently, I have completed constructing committee-oriented cross-partisan social networks and analyzing its effect on legislative effectiveness on the 116th Congress using social network and regression analysis. I want to use large scale computing tools to assemble issue-based congressional networks so that I can analyze their effect on legislative effectiveness. 

## Large-Scale Computing Strategies

I wish to utilize large scale computing methods to construct issue-oriented networks. 

* In order to extract issue-based networks and prepare them for social network and regression analysis, I need to scrape and clean the Congressional records for 116th Congress from Congress.gov[^3]. My intended large scale method is **AWS Lambda and Step functions or AWS EMR or Midway cluster**, but I have encountered some difficulties at the moment. Therefore, I am doing the scraping and cleaning on my local machine as if for now, and store the result, a dictionary that maps each legislator to all speeches made in the given congressional term(s) by the legislator, to ```AWS s3```. 

* With the scraped and cleaned congressional record, I use ```Pyspark``` to pull the speech data out from ```AWS s3```, and build a replicable and scalable pipeline for preprocessing and topic modelling with ```spark nlp``` and the ```ml module (with LDA)```. Although the issue selection process is manual for the speech data from 116th Congress because LDA model isn't very accurate in capturing all important issues and keywords, with more speech data from more congressional terms, this process is likely to become fully automated and scalable. More importantly, once the issues were picked out, the local issue-based network construction process is still replicable and scalable to incorporate more text data from a longer time span. 

[^1]: Legislative effectiveness score is a measure devised by Volden and Wiseman to account for the combination of a Congress member’s bill progress and the ability to pass more significant bills (Volden and Wiseman, 2009 and 2014). For details, please visit: https://thelawmakers.org/category/legislative-effectiveness-scores# 

[^2]: Here, issue-oriented cross-partisan networks refer to social networks formed by legislators who bring up or discuss the same issues as reflected by Congressional record: the official daily record of the debates and proceedings of the U.S. Congress.

[^3]: https://www.congress.gov/congressional-record/116th-congress/browse-by-date  note that the congressional record are daily-based

## Structure of the Project
1. Scrape and clean congressional record: Code can be found in [scrape_cr.py](https://github.com/lsc4ss-s22/final-project-congress/blob/master/scrape_cr.py).

      Run: 
            
            pip install -r requirements.txt
            python3 scrape_cr.py

      Senate record from 2019 will be stored in ```senate_speech (1).json```  <br />
      Senate record from 2020 will be stored in ```senate_speech (2).json```  <br />
      House record from 2019-2020 will be stored in ```house_speech.json``` 

      All the json files map a speaker to his/her speeches in congressional record from 2019-2020 <br />

2. Merge speech dataset and LES dataset: Code and output can be found in [1_merge_speech_and_LES.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/1_merge_speech_and_LES.ipynb).

3. Upload the merged dataset to s3: Code and output can be found in [2_upload_to_S3.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/2_upload_to_S3.ipynb).

4. Topic modelling using pyspark and spark nlp: Code and output can be found in [3_topic_model.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/3_topic_model.ipynb).

5. Construct issue-based congressional networks: Code, output, and analysis can be found in [4_construct_network.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/4_construct_network.ipynb).

6. Regression analysis: Code, output, and analysis can be found in [5_analysis.pdf](https://github.com/lsc4ss-s22/final-project-congress/blob/master/5_analysis.pdf).
