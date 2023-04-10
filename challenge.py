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

def h_fNumber(employees):
    print(employees.pivot_table(columns=['sex'],aggfunc='size'))



def employees_per_company(employees):
    print(employees.pivot_table(columns=['company'],aggfunc='size'))
    """for c in companies:
        print("Company ", c , " Number of employees :  ",coll.count_documents({'company':c}))"""

def calculer_Age(age):
    thisyear = datetime.date.today().year
    year, month, day = age.split('-')
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

def pyramide_age(employees):
    ageClass = ['100+','90-100','80-90','70-80','60-70','50-60','40-50','30-40','20-30','10-20','0-10']
    df_=employees.pivot_table(columns=['groupe_age'],aggfunc='size')
    d = df_.reset_index()
    d.columns =['groupe_age','groupe_age_count']
    bar_plot = sns.barplot(x="groupe_age_count",y="groupe_age",data=d,order=ageClass)
    bar_plot.set(xlabel="Population",ylabel="Groupe Age")
    plt.savefig("Pyramide d-age.png")


if __name__ == "__main__":
    os.chdir("C:/StageChallenge/")

    #si database vide
    #load()

    coll = collection("localhost")
    employees = pd.DataFrame(coll.find())
    employees['sex'].replace('M',"Hommes",inplace=True)
    employees['sex'].replace('F',"Femmes",inplace=True)
    employees['age'] = employees ['birthdate'].apply(calculer_Age)
    employees['groupe_age'] = employees['age'].apply(age_class)
    h_fNumber(employees)
    employees_per_company(employees)
    pyramide_age(employees)

    
    
    