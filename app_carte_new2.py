import os
import geopandas as gpd
import pandas as pd
import numpy as np
#from cartopy import crs
import matplotlib.pyplot as plt
import mapclassify
import seaborn as sns
sns.set(style="ticks")
import contextily as ctx
import streamlit as st

#st.set_page_config(layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 




def exploreFile(customers):
    print("{0:30} {1:25} {2:25} {3:25}".format("Name", "n-row", "unique values", "missing values"))
    for i in customers:
        print("{0:30} {1:20} {2:20} {3:25}".format(i, customers[i].count(), customers[i].nunique(),customers[i].isna().sum()))
    print("------------------------------------")
    print(customers.info(verbose=True, null_counts=True))
    #print(customers.dtypes)
    print("------------------------------------")
    print(list(customers))

# fonction pour l'affichage des légendes des cartes
def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k,v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)

# fonctions pour l'affichage du nom des communes
def ensemble_des_communes():
    #CA PAYS AIX EN PROVENCE
    plt.figtext(.72,.51,'Rousset',weight ="bold",fontsize=12,ha='left')
    plt.figtext(.69,.52,'Chateauneuf',fontsize=8,ha='left')
    plt.figtext(.67,.55,'Beaureceuil',fontsize=9,ha='left')
    plt.figtext(.63,.54,'Le Tholonet',fontsize=9,ha='left')
    plt.figtext(.65,.58,'St Marc',fontsize=8,ha='left')
    plt.figtext(.65,.57,'Jaumegarde',fontsize=8,ha='left')
    plt.figtext(.75,.54,'Puyloubier',fontsize=9,ha='left')
    plt.figtext(.71,.58,'Vauvenargues',fontsize=9,ha='left')
    plt.figtext(.70,.54,'St Antonin',fontsize=9,ha='left')
    plt.figtext(.77,.47,'Trets',fontsize=9,ha='left')
    plt.figtext(.72,.48,'Peynier',fontsize=9,ha='left')
    plt.figtext(.67,.49,'Fuveau',fontsize=9,ha='left')
    plt.figtext(.64,.52,'Meyreuil',fontsize=9,ha='left')
    plt.figtext(.59,.56,'Aix',fontsize=12,ha='left')
    plt.figtext(.55,.53,'en-Provence',fontsize=12,ha='left')
    plt.figtext(.48,.49,'Vitrolles',fontsize=9,ha='left')
    plt.figtext(.54,.48,'Cabries',fontsize=9,ha='left')
    plt.figtext(.64,.70,'Pertuis',fontsize=9,ha='left')
    plt.figtext(.57,.72,'Saint',fontsize=9,ha='left')
    plt.figtext(.57,.71,'Estève',fontsize=9,ha='left')
    plt.figtext(.57,.70,'Janson',fontsize=9,ha='left')
    plt.figtext(.80,.70,'Saint-Paul',fontsize=9,ha='left')
    plt.figtext(.80,.69,'lez-Durance',fontsize=9,ha='left')
    plt.figtext(.63,.48,'Gardanne',fontsize=9,ha='left')
    plt.figtext(.51,.44,'Les-Pennes',fontsize=9,ha='left')
    plt.figtext(.52,.43,'Mirabeau',fontsize=9,ha='left')
    plt.figtext(.59,.48,'Bouc',fontsize=9,ha='left')
    plt.figtext(.59,.47,'Bel Air',fontsize=9,ha='left')
    plt.figtext(.66,.46,'Greasque',fontsize=8,ha='left')
    plt.figtext(.64,.45,'Mimet',fontsize=8,ha='left')
    plt.figtext(.60,.45,'Simiane',fontsize=8,ha='left')
    plt.figtext(.75,.67,'Jouques',fontsize=9,ha='left')
    plt.figtext(.70,.63,'Peyrolles',fontsize=9,ha='left')
    plt.figtext(.64,.61,'Venelles',fontsize=9,ha='left')
    plt.figtext(.65,.65,'Meyrargues',fontsize=9,ha='left')
    plt.figtext(.55,.67,'Rognes',fontsize=8,ha='left')
    plt.figtext(.48,.67,'Lambesc',fontsize=8,ha='left')
    plt.figtext(.60,.68,'Le Puy',fontsize=8,ha='left')
    plt.figtext(.60,.67,'Ste Réparade',fontsize=8,ha='left')
    plt.figtext(.52,.63,'St Cannat',fontsize=8,ha='left')
    plt.figtext(.52,.73,'La Roque',fontsize=8,ha='left')
    plt.figtext(.52,.72,"d'Anthéron",fontsize=8,ha='left')
    plt.figtext(.52,.60,'Eguilles',fontsize=8,ha='left')
    plt.figtext(.52,.57,'Ventabren',fontsize=8,ha='left')
    plt.figtext(.49,.59,'Coudoux',fontsize=8,ha='left')

    #CU MARSEILLE PROVENCE METROPOLE
    plt.figtext(.58,.34,'Marseille',fontsize=12,ha='left')
    plt.figtext(.57,.43,'Septemes',fontsize=8,ha='left')
    plt.figtext(.57,.42,'les vallons',fontsize=8,ha='left')
    plt.figtext(.66,.40,'Allauch',fontsize=8,ha='left')
    plt.figtext(.62,.40,'Plan de',fontsize=8,ha='left')
    plt.figtext(.62,.39,'Cuques',fontsize=8,ha='left')
    plt.figtext(.43,.46,'Marignane',fontsize=9,ha='left')
    plt.figtext(.39,.44,'Chateauneuf',fontsize=9,ha='left')
    plt.figtext(.42,.43,'les',fontsize=9,ha='left')
    plt.figtext(.40,.42,'Martigues',fontsize=9,ha='left')
    plt.figtext(.48,.45,'St Victoret',fontsize=7,ha='left')
    plt.figtext(.47,.43,'Gignac',fontsize=8,ha='left')
    plt.figtext(.50,.41,'Le',fontsize=9,ha='left')
    plt.figtext(.49,.40,'Rove',fontsize=9,ha='left')
    plt.figtext(.39,.40,'Sausset',fontsize=8,ha='left')
    plt.figtext(.39,.39,'les Pins',fontsize=8,ha='left')
    plt.figtext(.42,.38,'Carry',fontsize=8,ha='left')
    plt.figtext(.42,.37,'le Rouet',fontsize=8,ha='left')
    plt.figtext(.44,.40,'Ensues la',fontsize=8,ha='left')
    plt.figtext(.45,.39,'Redonne',fontsize=8,ha='left')
    plt.figtext(.73,.35,'Gemenos',fontsize=9,ha='left')
    plt.figtext(.67,.28,'Cassis',fontsize=9,ha='left')
    plt.figtext(.71,.25,'La Ciotat',fontsize=9,ha='left')
    plt.figtext(.68,.31,'Carnoux',fontsize=9,ha='left')
    plt.figtext(.73,.31,'Roquefort la',fontsize=8,ha='left')
    plt.figtext(.73,.30,'Bedoulle',fontsize=8,ha='left')
    plt.figtext(.73,.28,'Ceyreste',fontsize=8,ha='left')

    # CA PAYS D'AUBAGNE ET DE L'ETOILE
    plt.figtext(.68,.36,'Aubagne',fontsize=11,ha='left')
    plt.figtext(.70,.46,'Belcodenne',fontsize=9,ha='left')
    plt.figtext(.75,.40,'Auriol',fontsize=9,ha='left')
    plt.figtext(.72,.44,'La Bouilladisse',fontsize=8,ha='left')
    plt.figtext(.72,.42,'La',fontsize=7,ha='left')
    plt.figtext(.71,.41,'Destrousse',fontsize=7,ha='left')
    plt.figtext(.64,.33,'La Penne',fontsize=9,ha='left')
    plt.figtext(.64,.32,'sur Huveaune',fontsize=9,ha='left')
    plt.figtext(.79,.43,'Saint',fontsize=9,ha='left')
    plt.figtext(.79,.42,'Zacharie',fontsize=9,ha='left')
    plt.figtext(.79,.33,'Cuges les',fontsize=9,ha='left')
    plt.figtext(.79,.32,'Pins',fontsize=9,ha='left')
    plt.figtext(.67,.45,'Saint',fontsize=7,ha='left')
    plt.figtext(.67,.44,'Savournin',fontsize=7,ha='left')
    plt.figtext(.68,.43,'Cadolive',fontsize=7,ha='left')
    plt.figtext(.69,.42,'Peypin',fontsize=8,ha='left')
    plt.figtext(.70,.39,'Roquevaire',fontsize=8,ha='left')

    # CA SALON ETANG DE BERRE
    plt.figtext(.33,.71,'Eguyeres',fontsize=9,ha='left')
    plt.figtext(.37,.75,'Senas',fontsize=9,ha='left')
    plt.figtext(.42,.74,'Mallemort',fontsize=9,ha='left')
    plt.figtext(.42,.61,'Lançon de',fontsize=9,ha='left')
    plt.figtext(.42,.60,'Provence',fontsize=9,ha='left')
    plt.figtext(.37,.72,'Lamanon',fontsize=8,ha='left')
    plt.figtext(.37,.67,'Salon',fontsize=9,ha='left')
    plt.figtext(.36,.57,'Saint',fontsize=9,ha='left')
    plt.figtext(.36,.56,'Chamas',fontsize=9,ha='left')
    plt.figtext(.42,.54,'Berre',fontsize=9,ha='left')
    plt.figtext(.42,.53,"L'Etang",fontsize=9,ha='left')
    plt.figtext(.47,.53,"Rognac",fontsize=9,ha='left')

    # CA PAYS DE MARTIGUES
    plt.figtext(.34,.42,'Martigues',fontsize=9,ha='left')
    plt.figtext(.32,.49,'Saint-Mitre',fontsize=9,ha='left')
    plt.figtext(.30,.46,'Port-de',fontsize=8,ha='left')
    plt.figtext(.30,.45,'Bouc',fontsize=8,ha='left')

    # SAN OUEST PROVENCE
    plt.figtext(.34,.63,'Grans',fontsize=9,ha='left')
    plt.figtext(.32,.61,'Miramas',fontsize=9,ha='left')
    plt.figtext(.37,.61,'Cornillon',fontsize=8,ha='left')
    plt.figtext(.37,.60,'Confous',fontsize=8,ha='left')
    plt.figtext(.30,.56,'Istres',fontsize=9,ha='left')
    plt.figtext(.26,.50,'Fos',fontsize=9,ha='left')
    plt.figtext(.26,.49,'sur-mer',fontsize=9,ha='left')
    plt.figtext(.18,.48,'Port',fontsize=9,ha='left')
    plt.figtext(.16,.47,'Saint-Louis',fontsize=9,ha='left')
    plt.figtext(.45,.58,'La Fare',fontsize=8,ha='left')
    plt.figtext(.45,.57,'les-oliviers',fontsize=8,ha='left')
    plt.figtext(.48,.55,'Velaux',fontsize=8,ha='left')
    plt.figtext(.42,.72,'Alleinss',fontsize=8,ha='left')
    plt.figtext(.43,.70,'Venergues',fontsize=8,ha='left')
    plt.figtext(.43,.68,'Aurons',fontsize=8,ha='left')
    plt.figtext(.47,.72,"Charleval",fontsize=8,ha='left')
    plt.figtext(.42,.65,'Pelissanne',fontsize=8,ha='left')
    plt.figtext(.47,.63,'La',fontsize=8,ha='left')
    plt.figtext(.47,.62,'Barden',fontsize=8,ha='left')


def cartographie():
    choix2 = st.radio("Construction de la carte",("Garder les paramètres par défaut",'Changer les paramètres'))
    if choix2=='Changer les paramètres':
        #st.sidebar.header('Changer les paramètres de la carte')
        kl = st.number_input("Choix du nombre de classes", min_value=1, value=7, step=1)  
        titre = indic
        method = st.selectbox('Choix de la méthode pour la construction des classes',('Seuils naturels', 'Quantiles','Intervalle égal'))
        if method =='Seuils naturels':
            m = mapclassify.NaturalBreaks
        if method =='Quantiles':
            m = mapclassify.Quantiles
            meth = 'Quantile'
        if method =='Intervalle égal':
            m = mapclassify.EqualInterval
            meth = "Interval égal"
    if choix2=='Garder les paramètres par défaut':
        kl = 7
        m = mapclassify.NaturalBreaks
        meth='Seuils naturels'
    couleur = 'Oranges'
    transparence = 0.95
    source = "Source : calculs sur données DGCL"
    titre = indic
    if titre == 'AC/RFF*100':
        titre = "Poids de l'attribution de compensation dans les Recettes réelles de fonctionnement"
    if titre == 'Pot. fin. par hab. com/metropole':
        titre = "Potentiel financier par hab. divisé par le Potentiel financier par hab. moyen de la métropole"
    if titre == 'Part logements sociaux':
        titre = 'Part des logements sociaux dans les logements TH de la commune'       
    q10 = m(data_carte[indic],k=kl)
    mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
    f, ax = plt.subplots(1, figsize=(14, 14))
    data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
    ax.set_axis_off()
    replace_legend_items(ax.get_legend(), mapping)
    ax.set_title(titre,fontsize=14)
    plt.figtext(.15,.22,source,fontsize=12,ha='left')
    ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
    #carte(indic)
    #plt.savefig(indic+'.jpg')
    #f.savefig(indic+".pdf", bbox_inches='tight')
    st.header(titre+' (en €, 2019)')
    ensemble_des_communes()
    st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    mycol=['codgeo','Nom Collectivité',indic]
    tab = data_carte[mycol]
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab)

def cartographie2():
    choix2 = st.radio("Construction de la carte",("Garder les paramètres par défaut",'Changer les paramètres'))
    if choix2=='Changer les paramètres':
        #st.header('Changer les paramètres de la carte')
        kl = st.number_input("Choix du nombre de classes", min_value=1, value=7, step=1)  
        titre = indic
        method = st.selectbox('Choix de la méthode pour la construction des classes',('Seuils naturels', 'Quantiles','Intervalle égal'))
        if method =='Seuils naturels':
            m = mapclassify.NaturalBreaks
        if method =='Quantiles':
            m = mapclassify.Quantiles
            meth = 'Quantile'
        if method =='Intervalle égal':
            m = mapclassify.EqualInterval
            meth = "Interval égal"
    if choix2=='Garder les paramètres par défaut':
        kl = 7
        m = mapclassify.NaturalBreaks
        meth='Seuils naturels'
    couleur = 'Oranges'
    transparence = 0.95
    source = "Source : calculs sur données DGCL"
    titre = titre2
    q10 = m(data_carte[indic],k=kl)
    mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
    f, ax = plt.subplots(1, figsize=(14, 14))
    data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
    ax.set_axis_off()
    replace_legend_items(ax.get_legend(), mapping)
    ax.set_title(titre,fontsize=14)
    plt.figtext(.15,.22,source,fontsize=12,ha='left')
    ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
    #carte(indic)
    #plt.savefig(indic+'.jpg')
    #f.savefig(indic+".pdf", bbox_inches='tight')
    st.header(titre)
    ensemble_des_communes()
    st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    mycol=['codgeo','Nom Collectivité',indic]
    tab = data_carte[mycol]
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab)



def poids_rousset():
    #st.title("Poids de Rousset dans les ressources de la Métropole")
    ressources = pd.read_csv('data_cartes/ressources_mpm2016_2021.csv',sep=";")
    ressources['date']= pd.to_datetime(ressources['Exercice'], format='%Y')
    ressources['année'] = ressources['date'].dt.year
    ressources['IFER']= ressources['IFER'].round(0)
    ressources['TASCOM']= ressources['TASCOM'].round(0)
    ressources['Fiscalité économique (y compris DCRTP et GIR)'] =ressources['CFE']+ressources['CVAE']+ressources['TAFNB']+ressources['IFER']+ressources['TASCOM']+ressources['DCRTP_GIR']
    ressources['Fiscalité économique (y compris DCRTP et GIR)']= ressources['Fiscalité économique (y compris DCRTP et GIR)'].round(0)
    explain0=st.checkbox("retirer les estimations 2020 et 2021")
    if explain0:
        ressources = ressources.drop(ressources[(ressources['année'] ==2020) | (ressources['année'] ==2021)].index)
        #construction tableau avec les hypothèse sur les données
    h='Hypothèse sur les indicateurs (par année)'
    mycol = ['année','Perimetre',h]
    hyp1 =  ressources[mycol]
    hyp = hyp1.pivot(index='année', columns='Perimetre', values=h)
    hyp0=hyp.copy()
    with st.beta_expander("Les hypothèses"):
                st.dataframe(hyp0)
    st.write(' ')            
    del ressources['Hypothèse sur les indicateurs (par année)']
    #a = st.sidebar.selectbox("Choix de l'indicateur",('CFE', 'CVAE', 'TAFNB', 'IFER', 'TASCOM','FNB','FB','TH'))
    st.title(a)
    mycol = ['année','Perimetre',a]
    trav =  ressources[mycol]
    trav1 = trav.pivot(index='année', columns='Perimetre', values=a)
    tab_data=trav1.copy()
    tab_data['Poids de Rousset dans la Métropole (%)']=tab_data['Rousset']/tab_data['Metropole']*100
    tab_data['Poids de Rousset dans la Métropole (%)']=tab_data['Poids de Rousset dans la Métropole (%)'].round(2)
    tab_data.rename(columns={'Metropole': 'Metropole (en €)', 'Rousset': 'Rousset (en €)'}, inplace=True)
    var1="Poids de Rousset dans la Métropole (%)"
    #tab_data['année']=tab_data['année'].astype(str)
    fig_dims = (5, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    sns.lineplot(x = 'année', y = var1,ax=ax, data=tab_data)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.title(var1,size=14)
    plt.ylabel("en % de la Métropole",size=12)
    plt.xlabel("année",size=12)
    st.pyplot()
    st.write(' ')
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab_data)

def base100_2017():
    #st.title("Poids de Rousset dans les ressources de la Métropole")
    ressources = pd.read_csv('data_cartes/ressources_mpm2016_2021.csv',sep=";")
    ressources['date']= pd.to_datetime(ressources['Exercice'], format='%Y')
    ressources['année'] = ressources['date'].dt.year
    ressources['IFER']= ressources['IFER'].round(0)
    ressources['TASCOM']= ressources['TASCOM'].round(0)
    ressources['Fiscalité économique (y compris DCRTP et GIR)'] =ressources['CFE']+ressources['CVAE']+ressources['TAFNB']+ressources['IFER']+ressources['TASCOM']+ressources['DCRTP_GIR']
    ressources['Fiscalité économique (y compris DCRTP et GIR)']= ressources['Fiscalité économique (y compris DCRTP et GIR)'].round(0)
    explain0=st.checkbox("retirer les estimations 2020 et 2021")
    if explain0:
        ressources = ressources.drop(ressources[(ressources['année'] ==2020) | (ressources['année'] ==2021)].index)
        #construction tableau avec les hypothèse sur les données
    h='Hypothèse sur les indicateurs (par année)'
    mycol = ['année','Perimetre',h]
    hyp1 =  ressources[mycol]
    hyp = hyp1.pivot(index='année', columns='Perimetre', values=h)
    hyp0=hyp.copy()
    with st.beta_expander("Les hypothèses"):
                st.dataframe(hyp0)
    st.write(' ')            
    del ressources['Hypothèse sur les indicateurs (par année)']
    df_mask=ressources['année']==2017
    ressources2017 = ressources[df_mask]
    del ressources2017['Exercice']
    del ressources2017['date']
    del ressources2017['année']
    ressources2017.columns = ['Perimetre','CFE_2017', 'CVAE_2017', 'TAFNB_2017', 'IFER_2017', 'TASCOM_2017', 'DCRTP_GIR-2017', 'FNB_2017', 'FB_2017', 'TH_2017', 'TVA_2017','Fiscalité économique (y compris DCRTP et GIR)_2017']
    ressources_b100 = ressources.merge(ressources2017,how='inner',on='Perimetre')
    ressources_b100['CFE']=ressources_b100['CFE']/ressources_b100['CFE_2017']*100
    ressources_b100['CVAE']=ressources_b100['CVAE']/ressources_b100['CVAE_2017']*100
    ressources_b100['TAFNB']=ressources_b100['TAFNB']/ressources_b100['TAFNB_2017']*100
    ressources_b100['IFER']=ressources_b100['IFER']/ressources_b100['IFER_2017']*100
    ressources_b100['TASCOM']=ressources_b100['TASCOM']/ressources_b100['TASCOM_2017']*100
    ressources_b100['DCRTP_GIR']=ressources_b100['DCRTP_GIR']/ressources_b100['DCRTP_GIR']*100
    ressources_b100['FNB']=ressources_b100['FNB']/ressources_b100['FNB_2017']*100
    ressources_b100['FB']=ressources_b100['FB']/ressources_b100['FB_2017']*100
    ressources_b100['TH']=ressources_b100['TH']/ressources_b100['TH_2017']*100
    ressources_b100['TVA']=ressources_b100['TVA']/ressources_b100['TVA_2017']*100
    ressources_b100['Fiscalité économique (y compris DCRTP et GIR)']=ressources_b100['Fiscalité économique (y compris DCRTP et GIR)']/ressources_b100['Fiscalité économique (y compris DCRTP et GIR)_2017']*100
    ressources_b100_2017=ressources_b100.drop(columns=['CFE_2017', 'CVAE_2017', 'TAFNB_2017', 'IFER_2017', 'TASCOM_2017', 'DCRTP_GIR-2017', 'FNB_2017', 'FB_2017', 'TH_2017', 'TVA_2017','Fiscalité économique (y compris DCRTP et GIR)_2017'])
    #a = st.sidebar.selectbox("Choix de l'indicateur",('CFE', 'CVAE', 'TAFNB', 'IFER', 'TASCOM','FNB','FB','TH'))
    st.title(a)
    mycol = ['année','Perimetre',a]
    trav =  ressources[mycol]
    trav1 = trav.pivot(index='année', columns='Perimetre', values=a)
    tab_data=trav1.copy()
    #print(trav2.info())
    m2017=tab_data.loc[2017,'Metropole']
    r2017=tab_data.loc[2017,'Rousset']
    tab_data['Metropole (100 en 2017)']=tab_data['Metropole']/m2017*100
    tab_data['Metropole (100 en 2017)']=tab_data['Metropole (100 en 2017)'].round(2)
    tab_data['Rousset (100 en 2017)']=tab_data['Rousset']/r2017*100
    tab_data['Rousset (100 en 2017)']=tab_data['Rousset (100 en 2017)'].round(2)
    tab_data.rename(columns={'Metropole': 'Metropole (en €)', 'Rousset': 'Rousset (en €)'}, inplace=True)
    fig_dims = (5, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    #st.bar_chart(x = 'année', y = var1)
    #tab_data['année']=ressources_b100_2017['année'].astype(str)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    ressources_b100_2017['année']=ressources_b100_2017['année'].astype(str)
    sns.lineplot(x = 'année', y = a, hue='Perimetre',data=ressources_b100_2017)
    plt.title("Evolution de Rousset et de la Métropole, base 100 en 2017",size=14)
    plt.ylabel("montant",size=12)
    plt.xlabel("année",size=12)
    st.pyplot()
    st.write(' ')
    #st.header(a+' : Les données')
    #st.dataframe(tab_data)
    with st.beta_expander("Les données"):
            st.dataframe(tab_data)




# shapefile pour la cartographie
pth ='contour_cartes/a_com2020_mpm.shp'
carte = gpd.read_file(pth)
# fichier avec les données source
fichier_source = 'data_cartes/data_mpm.csv' 
data_carte = pd.read_csv(fichier_source, sep =',')
data_carte = data_carte.fillna(0)
data_carte['codgeo'] = data_carte['codgeo'].astype(str)
data_carte = carte.merge(data_carte, how='inner',on ='codgeo')
data_carte = data_carte.to_crs(epsg=3857)
data_carte['AC/RFF*100']=data_carte["Attribution de compensation de la commune divisé par Recettes réelles de fonctionnement"]
data_carte['Pot. fin. par hab. com/metropole']=data_carte["Potentiel financier par hab. divisé par le Potentiel financier par hab. moyen de la métropole"]
data_carte['Part logements sociaux'] = data_carte['Nombre logements sociaux de la commune divisé par Nombre de logements TH de la commune']


# MAIN

#st.title("Outils pour la Ville de Rousset")
expander_bar = st.beta_expander("Sur cette application")
expander_bar.markdown("""
* **Travaux réalisés pour  :** la Ville de Rousset
* **Auteur :** olivier Boylaud  (olivier@boylaud.eu)
* **Source des données : ** DGCL et DGFIP.
""")
st.write(' ')
st.write(' ')
st.sidebar.header('MENU')
choix = st.sidebar.radio("Que voulez-vous obtenir ?",("Revenir à zéro",'Les ressources fiscales par habitant captées par la Métropole (cartographie)','Les bases fiscales par habitant des communes de la Métropole (cartographie)',"Poids de Rousset dans les ressources de la Métropole","Dynamique des ressources fiscales rattachables  à Rousset et à l'ensemble des communes de la Métropole","Poids de l'allocation de compensation dans les ressources réelles de fonctionnement (cartographie)","Mesurer l'impact d'une révision de l'allocation de compensation","Revenu imposable par habitant (cartographie)","Part des logements sociaux (cartographie)"))

if choix == 'Revenir à zéro':
    st.title("Travaux statistiques pour la Ville de Rousset")
    st.write(" ")
    st.header("Selectionner le module désiré dans le menu à gauche de l'écran")

if choix == 'Les ressources fiscales par habitant captées par la Métropole (cartographie)':
    st.title('Les ressources fiscales par habitant captées par la métropole Aix-Marseille-Provence, en euros')
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    indic = st.selectbox("Choix de la ressource captée par la Métropole",('CVAE par habitant','CFE par habitant','CET par habitant','TASCOM par habitant','IFER par habitant','TAFNB par habitant'))
    cartographie()

if choix == 'Les bases fiscales par habitant des communes de la Métropole (cartographie)':
    st.title('Les bases fiscales par habitant des communes de la métropole Aix-Marseille-Provence, en euros')
    st.header('Selectionner dans le menu déroulant la base fiscale')
    indic = st.selectbox("Choix de la base fiscale",('Bases CFE par habitant','Bases brutes de FB par habitant','Bases brutes de FNB par habitant','Bases brutes de TH par habitant', 'Bases nettes FB par habitant','Bases nettes FNB par habitant','Bases nettes TH par habitant'))
    cartographie()

if choix == "Poids de Rousset dans les ressources de la Métropole":
    st.title("Poids de Rousset dans les ressources de la Métropole")
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    a = st.selectbox("Choix de l'indicateur",('CFE', 'CVAE', 'TAFNB', 'IFER', 'TASCOM','FNB','FB','TH'))
    poids_rousset()

if choix == "Dynamique des ressources fiscales rattachables  à Rousset et à l'ensemble des communes de la Métropole":
    st.title("Dynamique des ressources fiscales rattachables  à Rousset et à l'ensemble des communes de la Métropole")
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    a = st.selectbox("Choix de l'indicateur",('CFE', 'CVAE', 'TAFNB', 'IFER', 'TASCOM','FNB','FB','TH'))
    base100_2017()

if choix == "Poids de l'allocation de compensation dans les ressources réelles de fonctionnement (cartographie)":
    st.title("Poids de l'allocation de compensation dans les ressources réelles de fonctionnement, en %")
    indic = "Attribution de compensation de la commune divisé par Recettes réelles de fonctionnement"
    titre2 = "Poids de l'allocation de compensation dans les ressources réelles de fonctionnement, en %"
    cartographie2()

if choix == "Revenu imposable par habitant (cartographie)":
    st.title("Revenu imposable par habitant, en euros")
    indic = 'Revenu imposable par hab.'
    titre2 = "Revenu imposable par habitant, en euros"
    cartographie2()

if choix == "Part des logements sociaux (cartographie)":
    st.title("Part des logements sociaux dans le nombre total de logement TH, en %")
    indic = "Nombre logements sociaux de la commune divisé par Nombre de logements TH de la commune"
    titre2 = "Part des logement sociaux, en %"
    cartographie2()

# module simulation AC
if choix == "Mesurer l'impact d'une révision de l'allocation de compensation":
    st.title("Impact d'une révision du montant de l'allocation de compensation")
    with st.beta_expander("Origine des attributions de compensation"):
        st.write("""
                 L’attribution de compensation (AC) est le principal flux financier entre les communes et les établissements publics de coopération intercommunale (EPCI) à fiscalité professionnelle unique (FPU). Avec l’AC, l’EPCI a
vocation à reverser à la commune le montant des produits de fiscalité professionnelle perçus par cette dernière, l’année précédant celle de la première application du régime de la FPU, en tenant compte du
montant des transferts de charges opérés entre l’EPCI et la commune
                """)
    compar2 = st.radio("Choisir le type de simulation",("Révision individualisée","Révision unilatérale"))
    if compar2=="Révision individualisée":
        st.header("Révision individualisée")
        explain1=st.checkbox("voir l'explication") 
        if explain1:
            st.write(""" Les EPCI faisant application du régime de fiscalité professionnelle unique et leurs communes membres peuvent procéder à la diminution des attributions de compensation d'une partie des communes membres lorsque les communes concernées disposent d'un potentiel financier par habitant
supérieur de plus de 20 % au potentiel financier par habitant moyen de l'ensemble des communes membres. Les délibérations concordantes doivent être adoptées par deux tiers au moins des conseils municipaux des communes intéressées représentant plus de la moitié de la population totale de celles-ci, ou par la moitié au moins des conseils municipaux des communes représentant les deux tiers de la
population totale de l’EPCI. Dans ce cadre, toutes les communes de l’EPCI sont dites « intéressées » et doivent se prononcer sur la mise en œuvre de la révision « individualisée ». Cette révision à la baisse
du montant des AC ne peut excéder 5 % du montant initial de celles-ci . """)
        st.write("Choix des paramètres pour la simulation")
        pfsup = st.number_input("Commune avec un potentiel fiancier supérieure à ", min_value=1.2, value=1.2, step=0.1)
        taux_reduc_pf = st.number_input("% de réduction de l'AC", max_value=5, value=5, step=1)
        data_carte["AC_PFsup"] = np.where(data_carte["PF_hab_com / PF_hab_mpm"] >pfsup, data_carte['Attribution de compensation de la commune'],0)
        data_carte['AC_PFsup_reduc']=data_carte['AC_PFsup']*taux_reduc_pf/100
        data_carte["AC_PFsup_reduc_max"] = np.where(data_carte["AC_PFsup_reduc"] > data_carte["RRF_5pc"], data_carte["RRF_5pc"],data_carte["AC_PFsup_reduc"])
        indic1 = "AC_PFsup_reduc_max"
        eco_mpm = data_carte["AC_PFsup_reduc_max"].sum()
        eco_mpm=int(eco_mpm)
        titre = "Montant de la réduction des AC en tenant compte de la limite maximale de 5 % des recettes de fonctionnement "
        source = "calculs sur données DGCL"
        st.set_option('deprecation.showPyplotGlobalUse', False)
        data_carte = data_carte.to_crs(epsg=3857)
        unite = 500 #mettre 1 si on maintient l'unité
        centroids = data_carte.copy()
        centroids.geometry =data_carte.centroid
        centroids['size'] = centroids[indic1] / unite  # to get reasonable plotable number
        ax = data_carte.plot(facecolor='beige', alpha=0.9, edgecolor='k',figsize=(14, 14))
        ax.set_title(titre)
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #centroids.plot(markersize='size', color = '#FFE4B5',ax=ax)
        centroids.plot(markersize='size', color = 'blue',alpha=0.4, ax=ax)
        gl = plt.scatter([],[], s=100, marker='o', color='#555555')
        ga = plt.scatter([],[], s=1000, marker='o', color='#555555')
        ensemble_des_communes()
        #principales_communes()
        #plt.legend((gl,ga),('10 000', '100 000'),scatterpoints=1,loc='upper left',ncol=1,fontsize=12)
        #plt.savefig(indic1+'_circle.jpg')
        #plt.savefig(indic1+"_circle.pdf", bbox_inches='tight')
        st.pyplot()
        st.write('gain pour la métropole :',eco_mpm)
        mycol=['codgeo','Nom Collectivité',indic1]
        tab = data_carte[mycol]
        with st.beta_expander("Les données"):
            st.dataframe(tab)
    if compar2=="Révision unilatérale":
        st.header("Révision unilatérale")
        explain1=st.checkbox("voir l'explication") 
        if explain1:
            st.write(""" La révision unilatérale du montant de l’AC est une révision opérée sans accord entre l’EPCI et la commune intéressée. Cette procédure de révision implique donc qu’une commune puisse voir le montant de son AC révisé sans avoir au préalable donné son accord. Seul l’EPCI est compétent pour
enclencher cette procédure de révision et peut y recourir uniquement dans les deux cas suivants :""")
            st.write("""1/ Lors d’une diminution des bases imposables de fiscalité professionnelle de l’EPCI L’accord des conseils municipaux des communes dont l’AC serait diminuée n’est
pas requis.;Un vote à la majorité simple de l’organe délibérant du groupement suffit. La diminution des bases imposables doit découler principalement du départ d’entreprises du territoire de l’EPCI
entraînant une diminution du produit de la fiscalité professionnelle, c'est-à-dire la CFE, la CVAE, l’IFER,la taxe additionnelle à la taxe foncière sur les propriétés non bâties et la TASCOM. Ces conditions sont
appréciées de façon stricte, l'incidence des abattements, exonérations et autres réfactions facultatives adoptés par l’EPCI ne peut pas justifier une modulation à la baisse du montant individuel des AC. Il
n’est pas possible de diminuer le montant des AC d’un montant supérieur à la perte de bases subies par l’EPCI""")
            st.write("""2/ Lors d’une fusion ou en cas de modification de périmètre de l’EPCI. Cette révision est limitée à 30 % du montant de l’AC versée initialement par l’EPCI
à FPU préexistant, sans que cela puisse représenter plus de 5 % des recettes réelles de fonctionnement perçues en N-1 par la commune intéressée par la révision. Par ailleurs, cette révision
ne peut s’exercer qu’une seule fois pendant les trois années qui suivent la fusion ou la modification de périmètre intercommunal. """)
        taux_reduc = st.number_input("% de réduction de l'AC", max_value=30, value=10, step=1)
        data_carte['reduc1']=data_carte['Attribution de compensation de la commune']*taux_reduc/100
        data_carte["reduc_max1"] = np.where(data_carte["reduc1"] > data_carte["RRF_5pc"], data_carte["RRF_5pc"],data_carte["reduc1"])
        data_carte["reduc_max1"] = np.where(data_carte["reduc_max1"] <0, 0,data_carte["reduc_max1"])
        data_carte["en % des RRF"]=data_carte["reduc_max1"]/data_carte["Recettes réelles de fonctionnement des communes N-2"]*100
        indic2 = "reduc_max1"
        eco_mpm2 = data_carte["reduc_max1"].sum()
        eco_mpm2=int(eco_mpm2)
        titre = "Montant de la réduction des AC en tenant compte de la limite maximale de 5 % des recettes de fonctionnement "
        source = "calculs sur données DGCL"
        st.set_option('deprecation.showPyplotGlobalUse', False)
        data_carte = data_carte.to_crs(epsg=3857)
        unite = 500 #mettre 1 si on maintient l'unité
        centroids = data_carte.copy()
        centroids.geometry =data_carte.centroid
        centroids['size'] = centroids[indic2] / unite  # to get reasonable plotable number
        ax = data_carte.plot(facecolor='beige', alpha=0.9, edgecolor='k',figsize=(14, 14))
        ax.set_title(titre)
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #centroids.plot(markersize='size', color = '#FFE4B5',ax=ax)
        centroids.plot(markersize='size', color = 'blue',alpha=0.4, ax=ax)
        gl = plt.scatter([],[], s=100, marker='o', color='#555555')
        ga = plt.scatter([],[], s=1000, marker='o', color='#555555')
        ensemble_des_communes()
        #plt.savefig(indic2+'_circle.jpg')
        #plt.savefig(indic2+"_circle.pdf", bbox_inches='tight')
        #principales_communes()
        #plt.legend((gl,ga),('10 000', '100 000'),scatterpoints=1,loc='upper left',ncol=1,fontsize=12)
        st.pyplot()
        st.write('gain pour la métropole :',eco_mpm2)
        mycol=['codgeo','Nom Collectivité',indic2,"en % des RRF"]
        tab = data_carte[mycol]
        with st.beta_expander("Les données"):
            st.dataframe(tab)




