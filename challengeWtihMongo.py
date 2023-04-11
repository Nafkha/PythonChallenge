import json
from pymongo import MongoClient
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def collection(uri):
    client = MongoClient(uri)
    database = client["rhobs"]
    collection = database["people"]
    return collection
def load(uri="localhost", datapath="data.json"):
    coll = collection(uri=uri)
    with open(datapath,"r") as fp:
        data = json.load(fp)

        for person in data:
            coll.insert_one(person)

def h_fNumber():
    coll = collection("localhost")
    nb_hommes = coll.count_documents({"sex":"M"})
    nb_Femmes = coll.count_documents({"sex":"F"})
    print(f"Nombre d'hommes :  {nb_hommes} Nombre de femmes : {nb_Femmes}")



def employees_per_company():
    coll = collection("localhost")
    result = list(coll.aggregate([
        {
        '$group':{
        '_id':'$company',
        'Total Workers' : {'$sum':1}
        }
        }
    ]))
    for r in result:
        print(f'Entreprise {r["_id"]} | Nombre de travailleurs {r["Total Workers"]}')

def calculer_Age(year):
    thisyear = datetime.date.today().year
    age = thisyear - int(year)
    return age

def age_class(age):
    if age<10:
        return '0-10'
    elif age>=10 and age <20 :
        return '10-20'
    elif age>=20 and age<30 :
        return '20-30' 
    elif age>=30 and age<40 :
        return '30-40' 
    elif age>=40 and age<50 :
        return '40-50' 
    elif age>=50 and age<60 :
        return '50-60' 
    elif age>=60 and age<70 :
        return '60-70' 
    elif age>=70 and age<80 :
        return '70-80' 
    elif age>=80 and age<90 :
        return '80-90' 
    elif age>=90 and age<100 :
        return '90-100'
    else:
        return '100+' 

def pyramide_age():
   
    coll = collection('localhost')
    ageClass = ['100+','90-100','80-90','70-80','60-70','50-60','40-50','30-40','20-30','10-20','0-10']

    group_by_year = coll.aggregate([
        {'$group':{
        '_id' : {'$substr': ['$birthdate',0,4]},
        'count':{'$sum':1}
        }}
    ])
    list_group_age = []

    for g in group_by_year : 
        age_grp = age_class(calculer_Age(g['_id']))
        list_group_age.append([age_grp,g['count']])
    df = pd.DataFrame(list_group_age,columns=['age_group','nombres'])
    df_ = df.groupby("age_group",as_index=False)["nombres"].sum()
    print(df_)
    bar_plot = sns.barplot(x="nombres",y="age_group",data=df_,order=ageClass)
    bar_plot.set(xlabel="Population",ylabel="Groupe Age")
    plt.savefig("Pyramide d-age avec mongo.png")




if __name__ == "__main__":
    os.chdir("C:/StageChallenge/")

    #si database vide
    #load()
    h_fNumber()
    employees_per_company()
    pyramide_age()

    
    
    