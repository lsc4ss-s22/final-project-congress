"""
Name: util_record_linkage.py
Author: Lynette Dang

Utility function to help merge the LES dataset and the connection dictionaries
using record linkage
"""
import pandas as pd
import fuzzy_pandas as fpd
import json

house = pd.read_excel("House116.xlsx")
senate = pd.read_excel("Senate116.xlsx")
house = house[['Legislator name', 'Legislative Effectiveness Score', 'party']]
senate = senate[['Legislator name',
                 'Legislative Effectiveness Score', 'party']]
df_les = pd.concat([house, senate], axis=0)
with open('conn_network.json') as json_file:
    conn_network = json.load(json_file)
with open('ind_network.json') as json_file_2:
    ind_network = json.load(json_file_2)


def record_link(dic, df2, threshold, name):
    """
    Merge a dictionary with the LES dataset using record linkage

    Inputs:
        dic: dictionary object
        df2: dataframe containing the LES dataset
        threshold: threshold for record linkage
        name: name of the output csv file
    Outputs:
        /
    """
    df1 = pd.DataFrame(dic.items(), columns=[
        "Legislator name", "Connections", "party"])
    df_analysis = fpd.fuzzy_merge(df1, df2,
                                  left_on='Legislator name',
                                  right_on='Legislator name',
                                  method='levenshtein',
                                  threshold=threshold)
    df_analysis.to_csv(name+".csv")


record_link(conn_network, df_les, 0.80, 'analysis_conn')
record_link(ind_network, df_les, 0.80, 'analysis_ind')
