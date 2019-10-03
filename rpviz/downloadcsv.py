# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 16:02:42 2019

@author: anael

Comment: not really smart coded but couldn't find a better way 
"""
import csv
import os

def downloadcsv(outfolder,f,LR,reac_smiles,Lreact,Lprod,species_names,dfG_prime_o,dfG_prime_m,dfG_uncert,flux_value,\
            rule_id,rule_score,RdfG_o,RdfG_m, RdfG_uncert,Path_flux_value,roots):
    """create a csv file for each pathway"""

    
    with open(os.path.join(outfolder,str(f)+'.csv'), 'w',newline='') as csvfile:
        fieldnames = ['Pathway', 'RdfG_o','RdfG_m','RdfG_uncert','Path_flux','Reaction',\
                      'Reaction SMILES','reactants','products','rule_id','rule_score',\
                      'dfGprime_o','dfGprime_m','dfG_uncert','flux_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(LR)) :
            reactants=[]
            products=[]
    
            if LR[i] not in roots.keys(): 
                for r in Lreact[i]:
                    reactants.append(species_names[r])
                for p in Lprod[i]:
                    products.append(species_names[p])
                try: #PROBLEM WITH CSV FILES : All those values don't exist
                    dfG_prime_o=dfG_prime_o[LR[i]]
                except :
                    dfG_prime_o=''
                try :
                    dfG_prime_m=dfG_prime_m[LR[i]]
                except:
                    dfG_prime_m=''
                try :
                    dfG_uncert=dfG_uncert[LR[i]]
                except :
                    dfG_uncert=''
                try :
                    flux_value=flux_value[LR[i]]
                except :
                    flux_value=''
                try:
                    Path_flux_value=Path_flux_value[f]
                except:
                    Path_flux_value=''
                writer.writerow({'Pathway': f, 'RdfG_o':RdfG_o[f],'RdfG_m':RdfG_m[f],\
                                 'RdfG_uncert':RdfG_uncert[f],'Path_flux':Path_flux_value,\
                                 'Reaction': LR[i],'Reaction SMILES':reac_smiles[LR[i]],\
                                 'reactants': reactants, 'products':products,\
                                 'rule_id':rule_id[LR[i]],'rule_score':rule_score[LR[i]],\
                                 'dfGprime_o':dfG_prime_o,'dfGprime_m':dfG_prime_m,\
                                 'dfG_uncert':dfG_uncert,'flux_value':flux_value})
    csvfile.close()