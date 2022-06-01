# Large-Scale Computing Final Project: Issue-Based Congressional Network and Legislative Effectiveness
This is the GitHub repository for the final project of MACS 30123 (Spring 2022) Large Scale Computing. 


Author: Lynette Dang

## Social Science Questions
The US Congress is known for having increasing polarization and thus questionable effectiveness with regard to making and passing bills, approving presidential nominations, as well as budgeting. While studying legislative effectiveness, existing literature focuses on the important personal and institutional attributes such as race, gender, and ethnicity that make some Congressmen and Congresswomen more effective legislators than their peers. However, only a limited amount of attention has been directed to individual-based social networks within Congress. Can issue-oriented and committee-oriented cross-partisan social networks help overcome congressional gridlocks and mitigate polarization? This paper seeks to investigate the impact of these two types of social networks on legislative effectiveness score[^1] of each legislator in the 116th Congress: How does issue-oriented cross-partisan social networks[^2] and committee-oriented cross-partisan social networks affect legislative effectiveness of each legislator in the 116th Congress? Which type of networks has a larger impact on legislative effectiveness? I believe by examining these two types of social networks and their effect on legislative effectiveness, we are one step closer to understanding legislative bargaining, policy making, and political representation on a federal level. Note that I am also proposing to do the same project (or parts of it) for my perspectives and social network analysis class. Eventually, I want to answer this research question for my MA thesis and expand my analysis to include more congressional terms (ideally from 2000-2022).

Currently, I have completed constructing committee-oriented cross-partisan social networks and analyzing its effect on legislative effectiveness on the 116th Congress using social network and regression analysis. I want to use large scale computing tools to build a scalable pipeline for assembling issue-based congressional networks, so I can analyze their effect on legislative effectiveness for the 116th Congress, and expand the analysis to include the 107th-116th Congress for my MA thesis. 

## Large-Scale Computing Strategies

I wish to utilize large scale computing methods to scrape/clean congressional record and select the issues for the issue-oriented congressional networks to ensure time efficiency, replicability and scalability. 

* In order to extract issue-based networks and prepare them for social network and regression analysis, I need to scrape and clean the Congressional records for 116th Congress from Congress.gov[^3]. My intended large scale method is **a combination of AWS Lambda and Step functions, or AWS EMR, or Midway cluster**, but I have encountered some difficulties at the moment. Therefore, I am doing the scraping and cleaning on my local machine as if for now, and store the result, a dictionary that maps each legislator to all speeches made in the given congressional term(s) by the legislator, to ```AWS s3```. 

* With the scraped and cleaned congressional record, I use ```Pyspark``` to pull the speech data out from ```AWS s3```, and build a replicable and scalable pipeline for preprocessing and topic modelling with ```spark nlp``` and the ```ml module (with LDA)```. Although the issue selection process is manual for the speech data from 116th Congress because LDA model isn't very accurate in capturing all important issues and keywords, with more speech data from more congressional terms, this process is likely to become fully automated and scalable. 

[^1]: Legislative effectiveness score is a measure devised by Volden and Wiseman to account for the combination of a Congress member’s bill progress and the ability to pass more significant bills (Volden and Wiseman, 2009 and 2014). For details, please visit: https://thelawmakers.org/category/legislative-effectiveness-scores# 

[^2]: Here, issue-oriented cross-partisan networks refer to social networks formed by legislators who bring up or discuss the same issues as reflected by Congressional record: the official daily record of the debates and proceedings of the U.S. Congress.

[^3]: https://www.congress.gov/congressional-record/116th-congress/browse-by-date  note that the congressional record are daily-based


## Structure of the Project
1. **Scrape and clean congressional record (local, no pool threading)**: Code can be found in [scrape_cr.py](https://github.com/lsc4ss-s22/final-project-congress/blob/master/scrape_cr.py).

      Run: 
            
            pip install -r requirements.txt
            python3 scrape_cr.py

      Senate record from 2019 will be stored in ```senate_speech (1).json```  <br />
      Senate record from 2020 will be stored in ```senate_speech (2).json```  <br />
      House record from 2019-2020 will be stored in ```house_speech.json``` 

      All the json files map a speaker to his/her speeches in congressional record from 2019-2020 <br />


### OR 


1. **Scrape and clean congressional record (local, with pool threading)**: Code can be found in [scrape_cr_pt.py](https://github.com/lsc4ss-s22/final-project-congress/blob/master/scrape_cr_pt.py).

      Run: 
            
            pip install -r requirements.txt
            python3 scrape_cr_pt.py

      Note that: The pool threading implementation has been pilot tested. It can only parallelize the scraping part, not the cleaning part

2. **Merge speech dataset and LES dataset**: Code and output can be found in [1_merge_speech_and_LES.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/1_merge_speech_and_LES.ipynb).

3. **Upload the merged dataset to s3**: Code and output can be found in [2_upload_to_S3.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/2_upload_to_S3.ipynb).

4. **Topic modelling using pyspark machine learning and spark nlp**: Code and output can be found in [3_topic_model.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/3_topic_model.ipynb).

5. **Construct issue-based congressional networks (local)**: Code, output, and analysis can be found in [4_construct_network.ipynb](https://github.com/lsc4ss-s22/final-project-congress/blob/master/4_construct_network.ipynb).

6. **Regression analysis (local)**: Code, output, and analysis can be found in [5_analysis.pdf](https://github.com/lsc4ss-s22/final-project-congress/blob/master/5_analysis.pdf).

Note that: I could have directly wrote the scraped and cleaned speeches to s3 from my python script from step 1, upload the LES dataset, and do the merging through spark so that step 2 and 3 are no longer needed. But because the runtime for the scraping and cleaning program is very long on local machines, I separated the program into two parts: house and senate. My classmate Joe helped me to scrape house speeches and sent the file to me. Therefore, specifically for the workflow of this final project, I have decided to merge the datasets first, then upload to s3.

## Network Analysis
<p float="left">
<p align="center"> Figure 1: Issue-Based Congressional Network </p>
<p align="center"> <img src="https://user-images.githubusercontent.com/91070896/171289064-7bef7d4c-5e3d-410a-a7c8-ac59732f030e.png" data-canonical-src="https://user-images.githubusercontent.com/91070896/171289064-7bef7d4c-5e3d-410a-a7c8-ac59732f030e.png" width="500" height="500" />  </p>

<p align="center"> Figure 2: Committee-Based Congressional Network </p>
<p align="center"> <img src="https://user-images.githubusercontent.com/91070896/171291227-bbd58e04-561a-48c2-9f06-e0f3867a90d5.png" data-canonical-src="https://user-images.githubusercontent.com/91070896/171291227-bbd58e04-561a-48c2-9f06-e0f3867a90d5.png" width="500" height="500" />  </p>
</p>

We will first take a look at the network structure before regression analysis. The network consists of digraphs, and has 411 nodes as individual legislators (missing a few legislators during record linkage and due to the lack of issue-related speeches) and 20610 edges representing their committee-based connections, with density of 0.35, and average clustering coefficient of 0.43. The first graph is a visualizations of issue-based based congressional networks. Each tie in the visualization represents a issue-based connection between legislators, meaning that the two legislators care about the same issue and have mentioned related keywords in their speeches as reflected by congressional records. To distinguish the party affiliation of each legislator, blue nodes refer to Democrat legislators, and red nodes refer to Republican legislators. The issue-based networks formed a moderately-connected and clustered network among all legislators. Legislators from the two parties are at a roughly equal level of connectedness. There is no major clusters as observed in the network, unlike committee-based network, shwon in Figure 2, where senators and house of representatives have formed two distinct clusters. 



## Regression Analysis
Do centrality measures (betweenness centrality, closeness centrality, degree centrality, and eigenvector centrality), race, and gender play a role in determining whether a legislator is effective or not? In order to find out which independent variable or combination of independent variables will affect legislative effectiveness score, I decided to run a ridge regression and cross validate with a wide range of lambda values from 0.01 to 1000 on standardized features with first-order interaction terms in R. Ridge regression models use L2 regularization to weight and penalize residuals. They will likely shrink some coefficients to 0, or closer to 0, which helps me eliminate the unimportant features. It tends to generalize better because it is less sensitive to extreme variance in the data such as outliers. After training the models, the author compute the Bayesian information criterion (BIC) for model selection. BIC is derived from Bayesian probability and inference. It is appropriate for models fit under the maximum likelihood estimation framework. Typically, lower BIC value indicates lower penalty terms, hence a better model. The BIC values for all models ranges from 174 to 203, indicating the evidence for the best model and against the weaker model is strong. The most optimal lambda value turned out to be 0.01, with BIC = 173.8858. The results from the best performing model are shown in the table below.
<p align="center"> Figure 3: Effect of Centrality (Issue-Based Network), Race and Ethnicity on Legislative Effectiveness </p>
<p align="center"> <img src="https://user-images.githubusercontent.com/91070896/171294701-a6006847-ed1c-4f36-820a-970da791b32b.png" data-canonical-src="https://user-images.githubusercontent.com/91070896/171294701-a6006847-ed1c-4f36-820a-970da791b32b.png" width="450" height="600" />  </p>

From the table above, we can conclude that he 6 original features (centrality measures, predicted gender and ethnicity) individually does not make a large impact on legislative effectiveness. The regression coefficients from the four centrality measures are either not in magnitude or negative, suggesting there is weak relationship or even negative relationship between the feature and legislative effectiveness.

However, the interaction effects between between eigenvector centrality and betweenness centrality, closeness centrality and betweenness centrality as well as between degree centrality and betweenness centrality are remarkable. The large interaction coefficients for both measures each indicates a significant interaction effect between the two features. In other words, the legislators who have the most influential neighbors (high eigenvector centrality) and are more likely to control information flow (high betweenness centrality) are predicted to be more effective legislators by the model. Likewise, the legislators find it easier to reach other legislators (high closeness centrality) and more likely to control information flow (betweenness centrality), the legislators who stand on more and larger congressional committees (high degree centrality) and more likely to control information flow (high betweenness centrality), as well as black and hispanic legislators who are more likely to control information flow (high betweenness centrality) are predicted to be more effective legislators by the model. 

In conclusion, the results from regression analysis has shown that the following types of legislators are more effective than their peers based on issue-oriented congressional networks:
* information leaders who also influential neighbors
* information leaders who are more reachable
* information leaders who are involve in more and larger congressional committees
* black and hispanic information leaders

The results from committee-based congressional networks also state that black information leaders, information leaders who are more reachable, or involved in more and larger congressional committees to be more effective. The results from issue-based congressional networks is similar to the results from committee-based congressional networks, with some differences regarding the effect of interaction between eigenvector centrality and betweenness centrality, as well as hispanic and betweenness centrality. Although the reasons behind the similarities and differences is unclear, it is evident from both congressional networks that an increase in participation in committees and discussion about most frequnt issues can potentially improve the effectiveness of elected representatives.



## Reference
1. https://github.com/lsc4ss-s21/large-scale-personal-finance/blob/main/4_Pyspark_topic_modeling.ipynb
2. https://github.com/jchaskell/scraper-cr/blob/master/clean/filterCR_fix.py
3. https://github.com/unitedstates/congressional-record/tree/master/congressionalrecord
4. https://colab.research.google.com/github/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/Certification_Trainings/Public/2.Text_Preprocessing_with_SparkNLP_Annotators_Transformers.ipynb#scrollTo=EgdWV7yFix8e
5. https://medium.com/trustyou-engineering/topic-modelling-with-pyspark-and-spark-nlp-a99d063f1a6e
6. https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.clustering.LDA.html
