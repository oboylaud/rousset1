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

st.set_page_config(layout="wide")

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


def cartographie_classe_euros():
    c1, c2 = st.beta_columns((4, 1))
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    couleur = 'Oranges'
    transparence = 0.95
    source = "Source : calculs sur données DGFIP et DGCL"
    titre = titreindic
    with c2 :
        st.write(" ")
        st.write(" ")
        st.write('Unité')
        choix_unit = st.selectbox('Méthode de construction des classes',('en € par habitant','en 1000 €', 'écart en % à la moyenne par hab.','en 0/00 de la Métropole'))
        if choix_unit =='en € par habitant':
            indic = 'en_euros_par_habitant'
        if choix_unit == 'écart en % à la moyenne par hab.':
            indic='ecart'
        if choix_unit =='en 0/00 de la Métropole':
            indic = 'poids_dans_amp'
        if choix_unit =='en 1000 €':
            indic = 'en_milliers'            
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write('Paramètres de la carte')
        kl = st.number_input("Nombre de classes", min_value=1, value=7, step=1)  
        method = st.selectbox('Méthode de construction des classes',('Seuils naturels', 'Quantiles','Intervalle égal'))
        if method =='Seuils naturels':
            m = mapclassify.NaturalBreaks
        if method =='Quantiles':
            m = mapclassify.Quantiles
            meth = 'Quantile'
        if method =='Intervalle égal':
            m = mapclassify.EqualInterval
            meth = "Intervalle égal"
    with c1:
        q10 = m(data_carte[indic],k=kl)
        mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
        f, ax = plt.subplots(1, figsize=(14, 14))
        data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
        ax.set_axis_off()
        replace_legend_items(ax.get_legend(), mapping)
        #ax.set_suptitle(choix_unit)
        ax.set_title(titre+', '+choix_unit,fontsize=14, weight = 'bold')
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #carte(indic)
        #plt.savefig(indic+'.jpg')
        #f.savefig(indic+".pdf", bbox_inches='tight')
        #st.header(titre+' (en €, 2019)')
        ensemble_des_communes()
        st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    mycol=['codgeo','commune',indic]
    tab = data_carte[mycol]
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab)   

def cartographie_classe_evo():
    c1a, c2a = st.beta_columns((4, 1))
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    couleur = 'Oranges'
    transparence = 0.95
    source = "Source : calculs sur données DGFIP et DGCL"
    titre = titreindic1
    with c2a :
        st.write(" ")
        st.write(" ")
        #st.write('Unité')
        choix_unit1 = st.selectbox('Unité',('en € par habitant',"taux de croissance",'en K€'))
        if choix_unit1 =='taux de croissance':
            indic1 = 'TC'
        if choix_unit1 == 'en K€':
            indic1='ecart en k€'
        if choix_unit1 == 'en € par habitant':
            indic1='ecart en euro par hab'
            #st.write('aa')
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write('Paramètres de la carte')
        kl = st.number_input("Nombre de classes", min_value=1, value=7, step=1)  
        method = st.selectbox('Méthode de construction des classes',('Quantiles','Seuils naturels', 'Intervalle égal'))
        if method =='Quantiles':
            m = mapclassify.Quantiles
            meth = 'Quantile'
        if method =='Seuils naturels':
            m = mapclassify.NaturalBreaks
        if method =='Intervalle égal':
            m = mapclassify.EqualInterval
            meth = "Intervalle égal"
    with c1a:
        q10 = m(data_carte[indic1],k=kl)
        mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
        f, ax = plt.subplots(1, figsize=(14, 14))
        data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
        ax.set_axis_off()
        replace_legend_items(ax.get_legend(), mapping)
        #ax.set_suptitle(choix_unit)
        ax.set_title(titre+', '+choix_unit1,fontsize=14, weight = 'bold')
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #carte(indic)
        #plt.savefig(indic+'.jpg')
        #f.savefig(indic+".pdf", bbox_inches='tight')
        #st.header(titre+' (en €, 2019)')
        ensemble_des_communes()
        st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    mycol=['codgeo','commune',indic1]
    tab = data_carte[mycol]
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab)   

def cartographie_classe_3():
    c1a, c2a = st.beta_columns((4, 1))
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    couleur = 'Oranges'
    transparence = 0.95
    source = "Source :  DGCL"
    titre = titreindic3
    with c2a :
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write('Paramètres de la carte')
        kl = st.number_input("Nombre de classes", min_value=1, value=7, step=1)  
        method = st.selectbox('Méthode de construction des classes',('Quantiles','Seuils naturels', 'Intervalle égal'))
        if method =='Quantiles':
            m = mapclassify.Quantiles
            meth = 'Quantile'
        if method =='Seuils naturels':
            m = mapclassify.NaturalBreaks
        if method =='Intervalle égal':
            m = mapclassify.EqualInterval
            meth = "Intervalle égal"
    with c1a:
        q10 = m(data_carte[indic3],k=kl)
        mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
        f, ax = plt.subplots(1, figsize=(14, 14))
        data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
        ax.set_axis_off()
        replace_legend_items(ax.get_legend(), mapping)
        #ax.set_suptitle(choix_unit)
        ax.set_title(titre,fontsize=14, weight = 'bold')
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #carte(indic)
        #plt.savefig(indic+'.jpg')
        #f.savefig(indic+".pdf", bbox_inches='tight')
        #st.header(titre+' (en €, 2019)')
        ensemble_des_communes()
        st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    mycol=['codgeo','commune',indic3]
    tab = data_carte[mycol]
    with st.beta_expander("Afficher les données"):
        st.dataframe(tab)   



@st.cache
def chargement_data_carte_base():
    # shapefile pour la cartographie
    pth ='contour_cartes/a_com2020_mpm.shp'
    carte = gpd.read_file(pth)
    # fichier avec les données source
    fichier_source = 'data_amp/REI_DOT_AMP_2020a1.csv'
    data_carte_base = pd.read_csv(fichier_source, sep =';',decimal=",")
    data_carte_base['codgeo'] = data_carte_base['codgeo'].astype(str)
    data_carte_base = carte.merge(data_carte_base, how='inner',on ='codgeo')
    return data_carte_base



st.write(' ')
st.write(' ')
st.sidebar.header('MENU')
choix = st.sidebar.radio(" ",("Accueil",'Ressources 2020','Evolution entre 2016 et 2020','Caractéristiques des communes'))

if choix == 'Accueil':
    st.title("Métropole d'Aix-Marseille-Provence : ")
    st.title("Contribution de Rousset et des autres communes de la Métropole aux ressources issues de la fiscalité économique locale")
    st.write(" ")
    st.write(" ")
    #st.header("Travaux réalisés pour la Ville de Rousset")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    #st.write("Selectionner le module désiré dans le menu à gauche de l'écran")


if choix == 'Ressources 2020':
    data_carte=chargement_data_carte_base().copy()
    st.title('La fiscalité économique locale perçue sur les communes par la Métropole Aix-Marseille-Provence, par commune, 2020 ')
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    selec = st.selectbox("Choix de la ressource captée par la Métropole",('CVAE : due (payé par les entreprises)','CVAE : dégrevements', 'CVAE : total','CFE : base','CFE : produit', 'IFER','Tascom', "Compensations réforme TP",'Total (sans ajustement réforme TP)',"Total (avec ajustement réforme TP)",'Allocation de compensation'))
    if selec == 'CFE : base':
        code_var = 'CFE_BASE_GFP_2020'
        titreindic = "Base 2020 de la Cotisation foncière des entreprises (CFE)"
    if selec == 'CFE : produit':
        code_var = 'CFE_PROD_GFP_2020'
        titreindic = "Produit 2020 de la Cotisation foncière des entreprises (CFE)" 
    if selec == 'CVAE : total':
        code_var = 'CVAE_GFP_2020'
        titreindic = "Cotisation sur la valeur ajoutée des entreprises, 2020" 
    if selec == 'CVAE : due (payé par les entreprises)':
        code_var = 'CVAE_DUE_GFP_2020'
        titreindic = "Cotisation sur la valeur ajoutée des entreprises due (payé par les entreprises), 2020" 
    if selec == 'CVAE : dégrevements':
        code_var = 'CVAE_DEG_GFP_2020'
        titreindic = "Dégrévements de la Cotisation sur la valeur ajoutée des entreprises, 2020"
    if selec == 'Tascom':
        code_var = 'TASCOM_2020'
        titreindic = "Taxe sur les surfaces commerciales (Tascom) -2019 ou 2020-"
    if selec == 'IFER':
        code_var = 'IFER_2020'
        titreindic = "Imposition forfaitaire des entreprises de réseaux (IFER) -provisoire-*"
    if selec == 'Compensations réforme TP':
        code_var = 'Compensation_reforme_TP'
        titreindic = "Compensation réforme de la taxe professionnelle* (impact sur les dotations perçues)"
    if selec == 'Total (sans ajustement réforme TP)':
        code_var = 'Total_2020'
        titreindic = "Fiscalité économique locale (sans ajustement compensation réforme TP)"
    if selec == 'Total (avec ajustement réforme TP)':
        code_var = 'Total2020_cor'
        titreindic = "Fiscalité économique locale (avec ajustement compensation réforme TP)"    
    if selec == 'Allocation de compensation':
        code_var = 'AC'
        titreindic = "Allocation de compensation"
    data_carte['poids_dans_amp']=data_carte[code_var]/(data_carte[code_var].sum())*1000
    data_carte['ecart']=((data_carte[code_var]/(data_carte[code_var].sum())/(data_carte['POP_INSEE']/(data_carte['POP_INSEE'].sum())))*100)-100
    data_carte['en_euros_par_habitant']=data_carte[code_var]/data_carte['POP_INSEE']
    data_carte['en_milliers']=data_carte[code_var]/1000
    cartographie_classe_euros()


if choix == 'Evolution entre 2016 et 2020':
    data_carte=chargement_data_carte_base().copy()
    st.title('Evolution entre 2016 et 2020')
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    #code_var1="att1"
    #code_var2="att2"
    selec2 = st.selectbox("Choix de la ressource captée par la Métropole",('CVAE','CFE : base','CFE : produit', 'IFER'))
    if selec2 == 'CVAE':
        code_var1 = 'CVAE_GFP_2020'
        code_var2 = 'CVAE_2016'
        #data_carte['TC']=(data_carte[code_var1]-data_carte[code_var2])/data_carte[code_var2]*100
        titreindic1 = "Evolution de la Cotisation sur la valeur ajoutée des entreprises (CVAE) entre 2016 et 2020"
    if selec2 == 'CFE : base':
        code_var1 = 'CFE_BASE_GFP_2020'
        code_var2 = 'CFE_BASE_GFP_2016'
        titreindic1 = "Evolution de la base de la Cotisation foncière des entreprises (CFE) entre 2016 et 2020"
    if selec2 == 'CFE : produit':
        code_var1 = 'CFE_PROD_GFP_2020'
        code_var2 = 'CFE_PROD_GFP_2016'
        titreindic1 = "Evolution du produit de la Cotisation foncière des entreprises (CFE) entre 2016 et 2020"
    if selec2 == 'IFER':
        code_var1 = 'IFER_2020'
        code_var2 = 'IFER_2016'
        titreindic1 = "Evolution de l'IFER entre 2016 et 2020 -provisoire-"
    data_carte['TC']=(data_carte[code_var1]-data_carte[code_var2])/data_carte[code_var2]*100
    data_carte['ecart en k€']=(data_carte[code_var1]-data_carte[code_var2])/1000
    data_carte['ecart en euro par hab']=data_carte['ecart en k€']/data_carte['POP_INSEE']*1000
    cartographie_classe_evo()
    #st.dataframe(data_carte)
    


if choix == "Caractéristiques des communes":
    data_carte=chargement_data_carte_base().copy()
    st.title("Caractéristiques des communes")
    st.header('Selectionner dans le menu déroulant la caractéristique')
    selec3 = st.selectbox("Choix de l'indicateur",('Part des logement sociaux', 'Revenu imposable par habitant','Potentiel financier par habitant','Recettes réelles de fonctionnement par habitant','Allocation de compensation sur recettes réelles de fonctionnement'))
    if selec3 == 'Part des logement sociaux':
        indic3 = 'PART_LOGEMENT_SOCIAUX'        
        #data_carte['TC']=(data_carte[code_var1]-data_carte[code_var2])/data_carte[code_var2]*100
        titreindic3 = "Part des logements sociaux dans les logements soumis à la taxe d'habitation"
    if selec3 == 'Revenu imposable par habitant':
        indic3 = 'REV_IMPOSABLE_PAR_HAB'
        titreindic3 = "Revenu imposable par habitant"
    if selec3 == 'Potentiel financier par habitant':
        indic3 = 'POTENTIEL_FINANCIER_PAR_HAB'
        titreindic3 = "Potentiel financier par habitant"
    if selec3 == 'Recettes réelles de fonctionnement par habitant':
        data_carte['RRF_PAR_HAB']=data_carte['RRF']/data_carte['POP_DGF']
        indic3 = 'RRF_PAR_HAB'
        titreindic3 = "Recettes réelles de fonctionnement par habitant"
    if selec3 == 'Allocation de compensation sur recettes réelles de fonctionnement':
        indic3 = 'AC_RRF'
        titreindic3 = "Poids de l'allocation de compensation dans les recettes réelles de fonctionnement"
    cartographie_classe_3()


if choix == "Option 4":
    st.title("Poids de Rousset dans les ressources de la Métropole")
    st.header('Selectionner dans le menu déroulant la ressource fiscale')
    a = st.selectbox("Choix de l'indicateur",('CFE', 'CVAE', 'TAFNB', 'IFER', 'TASCOM','FNB','FB','TH'))
    poids_rousset()

#st.title("Outils pour la Ville de Rousset")
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
expander_bar = st.sidebar.beta_expander("A propos")
expander_bar.markdown("""
* **Auteur :** olivier Boylaud  (olivier@boylaud.eu)
* **Sources des données : ** DGCL et DGFIP.
""")


