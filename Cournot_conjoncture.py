
import os

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import streamlit as st
sns.set(style="ticks")

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def titre_2020():
	fig = plt.figure(figsize=(1, 1))
	text = fig.text(0.5, 0.5, "L'impact de la pandémie sur les branches \n Situation au 1er trimestre 2021", color='grey',ha='center', va='center', size=16)
	text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	st.pyplot(fig)

titre_2020()

# chargement et préparation des données 

fichier_source = 'cournot/data_interim.csv'
interim = pd.read_csv(fichier_source, sep=';', decimal=",")
interim.set_index('Periode',inplace=True)

fichier_source1 = 'cournot/data_compte_nat.csv'
compta_nat = pd.read_csv(fichier_source1, sep=';', decimal=",")
del compta_nat['Cokefaction et raffinage']
compta_nat=pd.melt(compta_nat,id_vars=['periode','variable_avec_unite'],value_vars=list(compta_nat.columns[2:]),var_name='secteur',value_name='valeur')
compta_nat.rename(columns = { "variable_avec_unite" : "Variables" 
                              }, inplace=True)
compta_nat=pd.pivot_table(compta_nat, index=['secteur','periode'], columns=['Variables'],  values=['valeur'],aggfunc='sum')
compta_nat=compta_nat.T
compta_nat.reset_index(inplace=True)
del compta_nat['level_0']
compta_nat.set_index('Variables',inplace=True)
compta_nat = compta_nat.T
compta_nat.reset_index(inplace=True)
compta_nat.info()

fichier_source2 = 'cournot/data_tx_chomage_partiel.csv'
chom_part = pd.read_csv(fichier_source2, sep=';', decimal=",")
chom_part.set_index('Periode',inplace=True)


list_branche = ['Total branches', 'Marchand non agricole', 'Industrie', 'Manuf', 'Services', 'Serv. pplt marchands', 'Serv. pplt non-marchands', 'Agriculture', 'Energie, eau, dechets', 'Industries agro-alimentaires', "Biens d'equipement", 'Materiels de transport', 'Autres branches industrielles', 'Construction', 'Commerce', 'Transport', 'Hebergement-restauration', 'Information-communication', 'Services financiers', 'Services immobiliers', 'Services aux entreprises', 'Services non marchands', 'Services aux menages']
select = st.selectbox("Choix de la branche",(list_branche))

# tableau pour le secteur 'select'
df_mask=compta_nat['secteur']==select
compta_nat_sect = compta_nat[df_mask]
compta_nat_sect.set_index('periode',inplace=True)
del compta_nat_sect['secteur']
#compta_nat_sect

compta_nat_b100 = compta_nat_sect.T.copy()
col1 = ['2018T1']
v2018=compta_nat_b100[col1]

a=['2018T1', '2018T2', '2018T3', '2018T4', '2019T1', '2019T2', '2019T3', '2019T4', '2020T1', '2020T2', '2020T3', '2020T4', '2021T1']
for i in a:
    compta_nat_b100[i]=compta_nat_b100[i]/v2018['2018T1']*100
compta_nat_b100=compta_nat_b100.T 
#print(compta_nat_b100)
#compta_nat_sect
#"Volume horaire de travail (VHT) de l'ensemble des emplois (salaries ou non) : millions d'heures"



def fproductivite():
	# figure composantes PRODUCTIVITE
	col_productivite = ["Emploi total (equivalent temps plein) : milliers d'emplois", 
                    "Valeur ajoutee brute des branches :  volumes aux prix de l'annee precedente chaines (donnees CVS-CJO), base 2014, milliards d'euros", 
                    "Volume horaire de travail (VHT) de l'ensemble des emplois (salaries ou non) : millions d'heures"]
	productivite = compta_nat_b100[col_productivite]
	productivite.rename(columns = { "Emploi total (equivalent temps plein) : milliers d'emplois" : "Emploi total ETP",
                               "Valeur ajoutee brute des branches :  volumes aux prix de l'annee precedente chaines (donnees CVS-CJO), base 2014, milliards d'euros" : "Valeur ajoutée (volume)", 
                               "Volume horaire de travail (VHT) de l'ensemble des emplois (salaries ou non) : millions d'heures" : "Heures" 
                              }, inplace=True)
	#productivite = compta_nat_b100[col_productivite]
	indfig="Evolution des composantes de la productivité"
	selecfig=productivite
	sns.set_style("darkgrid")
	fig, ax = plt.subplots(figsize=(10,6))
	ax.legend(indfig, facecolor='w')
	plt.ylabel("100 en 2018T1")
	plt.xticks(rotation = 90, size=9)
	sns.lineplot(data=selecfig, palette="OrRd", linewidth=2.5)
	#plt.suptitle(select,weight ="bold")
	plt.title(indfig+", 2018M1-2021M2")
	#plt.figtext(.60,.15,'Source : calculs sur données Destatis',weight ="bold",fontsize=10,ha='left')
	plt.figtext(.50,.15,'Source : calculs sur Comptes nationaux (28-05-21)',fontsize=10,ha='left')
	#plt.savefig(select+'_productivite.svg')
	#plt.show()
	st.write(fig)
	with st.beta_expander("Afficher les données sur les composantes de la productivité"):
    	 st.dataframe(productivite)

def factivite():
	# figure composante TAUX DE MARGE / AVTIVITE / CONJONCTURE
	col_conjoncture = ["Production branche :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" , 
                  "Valeur ajoutee brute des branches :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros",
                  "Excedent brut d'exploitation :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros"]
	#activite = compta_nat_sect[col_conjoncture]
	activite = compta_nat_b100[col_conjoncture]
	activite.rename(columns = {
    	"Production branche :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" : "Production (valeur)", 
    	"Valeur ajoutee brute des branches :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" : "Valeur ajoutée (valeur)",
    	"Excedent brut d'exploitation :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" : "EBE (valeur)"
                              }, inplace=True)
	indfig="Composantes du taux de marge"
	selecfig=activite
	sns.set_style("darkgrid")
	fig, ax = plt.subplots(figsize=(10,6))
	ax.legend(indfig, facecolor='w')
	plt.ylabel("100 en 2018T1")
	plt.xticks(rotation = 90, size=9)
	sns.lineplot(data=selecfig, palette="OrRd", linewidth=2.5)
	#plt.suptitle(select,weight ="bold")
	plt.title(indfig+", 2018M1-2021M2")
	plt.figtext(.50,.15,'Source : calculs sur Comptes nationaux (28-05-21)',fontsize=10,ha='right')
	#plt.savefig(select+'_marge.svg')
	#plt.show()
	st.write(fig)
	with st.beta_expander("Afficher les données sur les composantes du taux de marge"):
    	 st.dataframe(activite)

def subventions():
	# figure ebe subventions
	col_subv = ["Excedent brut d'exploitation :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros",  
    	        "Subventions d'exploitations :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros"]
	subvention = compta_nat_sect[col_subv]
	subvention.rename(columns = {
            "Excedent brut d'exploitation :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" : "EBE",
            "Subventions d'exploitations :  valeurs aux prix courants  (donnees CVS-CJO), milliards d'euros" : "Subventions"
                              }, inplace=True)
	subvention['Subventions']=subvention['Subventions']*(-1)
	indfig="Suventions d'exploitations et EBE"
	selecfig=subvention
	sns.set_style("darkgrid")
	fig, ax = plt.subplots(figsize=(10,6))
	ax.legend(indfig, facecolor='w')
	plt.ylabel("en milliards d'euros")
	plt.xticks(rotation = 90, size=9)
	sns.lineplot(data=selecfig, palette="OrRd", linewidth=2.5)
	#plt.suptitle(select,weight ="bold")
	plt.title(indfig+", 2018M1-2021M2")
	plt.figtext(.50,.20,'Source : calculs sur Comptes nationaux (28-05-21)',fontsize=10,ha='right')
	#plt.savefig(select+'_subventions.svg')
	#plt.show()
	st.write(fig)
	with st.beta_expander("Afficher les données sur les subventions d'exploitations et l'EBE"):
    	 st.dataframe(subvention)


def interimaire() :
	# figure pour le nombre d'intérimaires pour le secteur
	indfig="Nombre d'intérimaires en fin de mois"
	#my_col=[select]
	selecfig=interim[select]
	sns.set_style("darkgrid")
	fig, ax = plt.subplots(figsize=(10,6))
	ax.legend(indfig, facecolor='w')
	plt.ylabel("nombre d'intérimaires")
	plt.xticks(rotation = 90, size=9)
	sns.lineplot(data=selecfig, palette="OrRd", linewidth=2.5)
	#plt.suptitle(select,weight ="bold")
	plt.title(indfig+", 2018M1-2021M2")
	plt.figtext(.35,.15,'Source : Dares (07-05-21)',fontsize=10,ha='right')
	#plt.savefig(select+'_interimaires.svg')
	#plt.show()
	st.write(fig)
	with st.beta_expander("Afficher les données sur le nombre d'intérimaires en fin de mois"):
		st.dataframe(selecfig)

def activite_partielle() :
	# figure pour le % salarie en activité partielle
	indfig="Salariés effectivement en activité partielle"
	#my_col=[select]
	selecfig=chom_part[select]
	sns.set_style("darkgrid")
	fig, ax = plt.subplots(figsize=(10,6))
	ax.legend(indfig, facecolor='w')
	plt.ylabel("en % des salariés du 4e trimestre 2020")
	plt.xticks(rotation = 90, size=9)
	sns.lineplot(data=selecfig, palette="OrRd", linewidth=2.5)
	#plt.suptitle(select,weight ="bold")
	plt.title(indfig+", 2020M3-2021M4")
	#plt.figtext(.60,.15,'Source : calculs sur données Destatis',weight ="bold",fontsize=10,ha='left')
	plt.figtext(.47,.15,'Source : calculs sur données Dares (31-05-21)',fontsize=10,ha='right')
	#plt.savefig(select+'_chomage_partiel.svg')
	st.write(fig)
	with st.beta_expander("Afficher les données sur l'activité partielle (en %)"):
		st.dataframe(selecfig)


c1, c12, c2  = st.beta_columns((5, 1, 5))
with c1 :
	fproductivite()
with c2 :
	factivite()
st.write(' ')
st.write(' ')
c3, c34, c4 = st.beta_columns((5, 1,5))
with c3 :
	interimaire()
with c4 :
	activite_partielle()
st.write(' ')
st.write(' ')
c5, c56, c6 = st.beta_columns((5, 1, 5))
with c5 :
	subventions()