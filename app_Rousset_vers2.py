import os
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import mapclassify
import seaborn as sns
sns.set(style="ticks")
import contextily as ctx
import streamlit as st




# configuration page

#st.set_page_config(layout="wide")
st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 




STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""







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


# fonction specifique AMP
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
    plt.figtext(.54,.47,'Cabries',fontsize=9,ha='left')
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
    plt.figtext(.53,.59,'Eguilles',fontsize=8,ha='left')
    plt.figtext(.52,.56,'Ventabren',fontsize=8,ha='left')
    plt.figtext(.49,.58,'Coudoux',fontsize=8,ha='left')

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
    plt.figtext(.47,.42,'Gignac',fontsize=8,ha='left')
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
    plt.figtext(.43,.69,'Venergues',fontsize=8,ha='left')
    plt.figtext(.41,.68,'Aurons',fontsize=8,ha='left')
    plt.figtext(.47,.72,"Charleval",fontsize=8,ha='left')
    plt.figtext(.42,.65,'Pelissanne',fontsize=8,ha='left')
    plt.figtext(.47,.63,'La',fontsize=8,ha='left')
    plt.figtext(.47,.62,'Barden',fontsize=8,ha='left')

def presentation_cet():
	st.write('La contribution économique territoriale (CET) est  un impôt qui concerne toute les entreprises. Il est composé de la cotisation foncière des entreprises (CFE) et de la cotisation sur la valeur ajoutée des entreprises (CVAE)')

def presentation_cvae():
    st.write("La Cotisation sur la valeur ajoutée des entrepises -CVAE- est due par les entreprises et les travailleurs indépendants à partir d'un chiffre d'affaires de 152 500 € et est calculée en fonction de la valeur ajoutée produite par l'entreprise.")
    st.write("Les entreprises dont le chiffre d’affaires est strictement inférieur à 500 000 € bénéficient, lorsqu’elles ne sont pas membres, sous certaines conditions, d’un groupe fiscal intégré, d’un dégrèvement total de cette cotisation. Il est égal à la différence entre le montant de cette cotisation calculée au taux de 1,5 % et l’application à la base d’imposition du taux d’imposition effectif. Il est précisé que les entreprises dont le chiffres d’affaires est inférieur à 2 M€ bénéficient d’un dégrèvement supplémentaire de 1 000 € et que la CVAE due par toute entreprise réalisant un chiffre d’affaires supérieur à 500 000 € ne peut être inférieur à 250 € à la suite de l’application de ce dégrèvement.")

def presentation_cfe():
    st.write("La cotisation foncière des entreprises (CFE) est due chaque année par les personnes physiques ou morales ou par les sociétés non dotées de la personnalité morale qui exercent à titre habituel une activité professionnelle non salariées. Elle est calculée sur la valeur locative des biens immobiliers soumis à la taxe foncière que l'entreprise a utilisé pour son activité professionnelle au cours de l'année N-2. La liste des activités exonérées de CFE est consacrée par les articles 1449 et suivants du code général des impôts. ")

def presentation_tascom():
    st.write("Un commerce qui exploite une surface de vente au détail de plus de 400 m² et réalisant un chiffre d'affaires hors taxe à partir de 460 000 €, est soumis à la taxe sur les surfaces commerciales (Tascom). La taxe est déductible du résultat fiscal de l'entreprise.")
    st.write("La taxe est due par les établissements commerciaux permanents, de stockage et de logistique, quels que soient les produits vendus au détail, situés en France, qui répondent aux conditions suivantes :")
    st.write("   - Chiffre d'affaires annuel (CAHT imposable de l'année précédente) supérieur ou égal à 460 000 € hors taxes")
    st.write("   - Surface de vente dépassant 400 m²")
    st.write("   - Ouverture en 1960 ou après")
    st.write("Les données présentés concernent pour une partie des communes l'année 2019. Elles sont de source DGFIP (2020) ou DGCL (2019)")

def presentation_ifer():
    st.write("L’imposition forfaitaire des entreprises de réseaux (IFER) est une taxe perçue au profit des collectivités territoriales.L’IFER concerne les entreprises exerçant leur activité dans le secteur de l’énergie, du transport ferroviaire et des télécommunications.")
    st.write("L'IFER se divise en plusieurs composantes. Les données de la DGFIP permettent de disposer de la valeur de l'IFER 2020 seulement pour une partie des composantes. Les dernières données de la DGCL permettent de disposer du montant de l'IFER seulement jusqu'en 2019. ")
    st.write("L'indicateur proposé est la valeur de l'IFER 2019 (source DGCL) plus l'évolution de l'IFER entre 2019 et 2020 pour les composantes connues (source DGFIP)")

def presentation_compensation_TP():
    st.write("Jusqu’en 2009, la principale ressource des EPCI à fiscalité professionnelle unique était la taxe professionnelle. La réforme de la taxe professionnelle s’est traduite par un nouveau schéma de financement qui repose sur :")
    st.write("• Une répartition de nouvelles impositions constituées par les différentes composantes de la contribution économique territoriale (CET) et de l’imposition forfaitaire sur les entreprises de réseaux (IFER) ;")
    st.write("• Une réallocation des impôts locaux existants : taxe d’habitation et taxes foncières avec le transfert des frais de gestion associés ;")
    st.write("• Un transfert de ressources fiscales existantes : taxe sur les surfaces commerciales (TaSCom), taxe sur les conventions d’assurance (TSCA) et droits de mutation à titre onéreux (DTMO).")
    st.write("Les pertes de produits TP non compensés par les nouveaux impôts sont particulièrement élevées sur Rousset et les communes industrielles de l’Étang de Berre")
    st.write("Pour garantir le niveau de ressources de chaque collectivité avant et après la réforme, deux mécanismes ont été mis en place par l’État : une dotation de compensation de la réforme de la taxe professionnelle (DCRTP) financée par l’État et la garantie individuelle de ressources (GIR) fonctionnant par abondement d’un fonds par les collectivités qui ont plus de ressources fiscales après réforme au profit des collectivités qui en ont moins.")
    st.write("Le montant par commune peut être apréhendé à travers la différence entre les ressources 2009 (avant la réforme de la TP) et en 2011 (après la réforme")

def presentation_total_avec_ajus():
    st.write("L'indicateur est construit comme la somme de la CVAE, de la CFE, de la Tascom, de l'IFER et de la taxe additionnelle à la taxe foncière sur les propriétés non bâties plus la quote part de la dotation de compensation de la réforme de la taxe professionnelle (DCRTP) et du GIR rattachable à la commune.")
    st.write(" Cette quote part est calculé comme la différence entre les ressources de la fiscalité économique rattachable à la commune en 2011 et celle en 2009.")

def presentation_total():
    st.write("L'indicateur est construit comme la somme de la CVAE, de la CFE, de la Tascom, de l'IFER et de la taxe additionnelle à la taxe foncière sur les propriétés non bâties.")
    st.write("Il ne prend pas en compte les compensations de la réforme de la TP")
    st.write("")


def description_indic():
	with st.beta_expander("En savoir plus"):
            if code_var1 == 'CET_GFP_2020':
                presentation_cet()
            if code_var1 == 'CVAE_GFP_2020':
                presentation_cvae()
            if code_var1 == 'CFE_BASE_GFP_2020':
                presentation_cfe()
            if code_var1 == 'CFE_PROD_GFP_2020':
                presentation_cfe()
            if code_var1 == 'IFER_2020':
                presentation_ifer() 
            if code_var1 == 'CVAE_DUE_GFP_2020':
                presentation_cvae()
            if code_var1 == 'CVAE_DEG_GFP_2020':
                presentation_cvae()
            if code_var1 == 'IFER_2020':
                presentation_ifer()
            if code_var1 == 'TASCOM_2020':
                presentation_tascom()
            if code_var1 == 'Compensation_reforme_TP':
                presentation_compensation_TP()
            if code_var1 == "Total2020_cor":
                presentation_total_avec_ajus()
            if code_var1 == "Total_2020":
                presentation_total()
            if carac =="Oui" :
            	st.write('Source : critères de répartition des dotations 2020, DGCL')



    

def cartographie_classe():
    #c1a, c2a = st.beta_columns((4, 1))
    #st.sidebar.write(" ")
    #st.sidebar.write(" ")
    #couleur = 'Oranges'
    #transparence = 0.95
    #source = "Source : calculs sur données DGFIP et DGCL"
    titre = titreindic1
    
    mycol=['codgeo','commune',indic1]
    tab = data_carte[mycol]
    tab[indic1]=tab[indic1].round()
    #c3a, c4a = st.beta_columns((1, 1))
    #c3a, c4a = st.beta_columns((1, 1))
    with c2:
        with st.beta_expander("Afficher le tableau avec les données"):
            st.write(titre+', '+choix_unit1)
            st.dataframe(tab)
    with c1 :
    	description_indic()
    st.write(' ')
    #c1a, c2a = st.beta_columns((6, 1)) 
    with c3 :            
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" Métropole Aix-Marseille-Provence par commune")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        #st.write(" ")
        #st.write(" ")
        #st.write(" ")
        st.write(" ")
        st.write(" ")
        with st.beta_expander("Paramètres"):
            #st.write('Paramètres')
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
            couleur =st.selectbox('Couleur',('Oranges','Blues','Greens','YlOrRd','magma'))
            list_fonds_carte =[
            'CartoDB.Positron',
            'Pas de fonds de carte',
            'OpenStreetMap.France',
            'CartoDB.Voyager',
            'Stamen.Toner',
            'Stamen.TonerLite',
            'Stamen.TonerLabels',
            'Stamen.Terrain',
            'Stamen.TerrainBackground',
            'Stamen.Watercolor',
            'OpenStreetMap.HOT',
            'OpenStreetMap.BlackAndWhite',
            'Esri.NatGeoWorldMap', 
            'Esri.WorldTopoMap',
            'Esri.DeLorme',
            'Esri.WorldImagery',
            'Esri.WorldStreetMap',
            'OpenTopoMap',
            'HikeBike.HikeBike',
            'NASAGIBS.ViirsEarthAtNight2012']
            select_map = st.selectbox('Fonds de carte',list_fonds_carte)
            transparence = st.slider('Transparence',0,100,95)
            transparence = transparence/100
            #couleur = 'Oranges'
            #transparence = 0.95
            #source = "Source : calculs sur données DGFIP et DGCL"                  
    with c2:
        q10 = m(data_carte[indic1],k=kl)
        mapping = dict([(i,s) for i,s in enumerate(q10.get_legend_classes(fmt="{:.0f}"))])
        f, ax = plt.subplots(1, figsize=(14, 14))
        data_carte.assign(cl=q10.yb).plot(column='cl', categorical=True, k=kl, cmap=couleur, alpha=transparence, linewidth=0.9, ax=ax, edgecolor='black', legend=True, legend_kwds={'loc': 'upper left'})
        ax.set_axis_off()
        replace_legend_items(ax.get_legend(), mapping)
        #ax.set_suptitle(choix_unit)
        ax.set_title(titre+', '+choix_unit1,fontsize=14, weight = 'bold')
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        if select_map =='Pas de fonds de carte':
            f.patch.set_facecolor('lightgray')
        if select_map =='CartoDB.Positron':
            ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron)
        if select_map =='CartoDB.Voyager':
            ctx.add_basemap(ax,source=ctx.providers.CartoDB.Voyager)
        if select_map =='Stamen.Toner':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.Toner)
        if select_map =='Stamen.TonerLite':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.TonerLite)
        if select_map =='Stamen.TonerLabels':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.TonerLabels)
        if select_map =='Stamen.Terrain':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.Terrain)
        if select_map =='Stamen.TerrainBackground':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.TerrainBackground)
        if select_map =='Stamen.Watercolor':
            ctx.add_basemap(ax,source=ctx.providers.Stamen.Watercolor)
        if select_map =='OpenStreetMap.France':
            ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.France)
        if select_map =='OpenStreetMap.HOT':
            ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.HOT)
        if select_map =='OpenStreetMap.BlackAndWhite':
            ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.BlackAndWhite)
        if select_map =='Esri.NatGeoWorldMap':
            ctx.add_basemap(ax,source=ctx.providers.Esri.NatGeoWorldMap)
        if select_map =='Esri.WorldTopoMap':
            ctx.add_basemap(ax,source=ctx.providers.Esri.WorldTopoMap)
        if select_map =='Esri.DeLorme':
            ctx.add_basemap(ax,source=ctx.providers.Esri.DeLorme)
        if select_map =='Esri.WorldImagery':
            ctx.add_basemap(ax,source=ctx.providers.Esri.WorldImagery)
        if select_map =='Esri.WorldStreetMap':
            ctx.add_basemap(ax,source=ctx.providers.Esri.WorldStreetMap)
        if select_map =='OpenTopoMap':
            ctx.add_basemap(ax,source=ctx.providers.OpenTopoMap)
        if select_map =='HikeBike.HikeBike':
            ctx.add_basemap(ax,source=ctx.providers.HikeBike.HikeBike)
        if select_map =='NASAGIBS.ViirsEarthAtNight2012':
            ctx.add_basemap(ax,source=ctx.providers.NASAGIBS.ViirsEarthAtNight2012)
        #ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #carte(indic)
        #plt.savefig(indic+'.jpg')
        #f.savefig(indic+".pdf", bbox_inches='tight')
        #st.header(titre+' (en €, 2019)')
        ensemble_des_communes()
        # label des communes
        #for x,y,label in zip(data_carte.xcl3857, data_carte.ycl3857,data_carte['commune']):
        #    ax.annotate(label, xy=(x,y), xytext=(5,5),textcoords="offset points",size=8, horizontalalignment='center',verticalalignment='baseline')

        st.pyplot(f)
    #st.write('méthode de construction des classes : ',meth)
    

def titre_2020():
	fig = plt.figure(figsize=(1, 1))
	text = fig.text(0.5, 0.5, "Contributions des 92 communes aux impôts économiques \n de la Métropole Aix-Marseille-Provence (2020)", color='brown',ha='center', va='center', size=16)
	text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	st.pyplot(fig)

def titre_evo_2016_2020():
	fig = plt.figure(figsize=(1, 1))
	text = fig.text(0.5, 0.5, "Evolution entre 2016 et 2020 de la CET des communes \n de la Métropole Aix-Marseille-Provence", color='brown',ha='center', va='center', size=16)
	text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	st.pyplot(fig)
	
def titre_caracteristiques_communes():
	fig = plt.figure(figsize=(1, 1))
	text = fig.text(0.5, 0.5, "Quelques caractéristiques des communes \n de la Métropole Aix-Marseille-Provence", color='brown',ha='center', va='center', size=16)
	text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	st.pyplot(fig) 

def titre_rev_ac():
	fig = plt.figure(figsize=(1, 1))
	text = fig.text(0.5, 0.5, "Simulation pour les communes de la Métropole Aix-Marseille-Provence \n de l'impact d'une révision de l'attribution de compensation", color='brown',ha='center', va='center', size=16)
	text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	st.pyplot(fig) 

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


# TITRE
#fig = plt.figure(figsize=(1, 1))
#text = fig.text(0.5, 0.5, "Contributions des 92 communes aux impôts économiques \n de la métropole Aix-Marseille-Provence (2016-2020)", color='brown',ha='center', va='center', size=16)
#text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
#st.pyplot(fig)


st.sidebar.header("CHOISIR L'APPLICATION")
choix = st.sidebar.radio("",('Contributions des 92 communes aux impôts économiques de la Métropole Aix-Marseille-Provence (2020)','Evolution entre 2016 et 2020 des composantes de la CET des communes de la Métropole Aix-Marseille-Provence',"Caractéristiques des communes","Mesurer l'impact d'une révision de l'attribution de compensation pour les communes de la Métropole"))





if choix == 'Contributions des 92 communes aux impôts économiques de la Métropole Aix-Marseille-Provence (2020)':
    titre_2020()
    data_carte=chargement_data_carte_base().copy()
    #st.sidebar.title('Contributions des 92 communes à la Métropole')
    #c1, c2 = st.beta_columns((4, 1))
    #st.header('Selectionner dans le menu déroulant la ressource fiscale')
    #st.sidebar.header('INDICATEURS')
    data_carte['Total_2020']=data_carte['Total_2020']-data_carte['TAFNB_PROD_GFP_2020']
    data_carte['Total2020_cor']=data_carte['Total2020_cor']-data_carte['TAFNB_PROD_GFP_2020']
    data_carte['CET_GFP_2020']=data_carte['CVAE_GFP_2020']+data_carte['CFE_PROD_GFP_2020']
    c1, c2,c3 = st.beta_columns((2, 8,2))
    with c1:
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	selec = st.selectbox("Choix de l'impôt",('CET','CVAE : total','CVAE : due','CVAE : dégrevements', 'CFE : base','CFE : produit', 'IFER','Tascom', 'Total (sans ajustement)',"ajustement TP","Total (avec ajustement)"))
    if selec == 'CET':
        code_var1 = 'CET_GFP_2020'
        titreindic1 = "Contribution économique térritoriale (CET), 2020"
    if selec == 'CFE : base':
        code_var1 = 'CFE_BASE_GFP_2020'
        titreindic1 = "Base 2020 de la Cotisation foncière des entreprises (CFE)"
    if selec == 'CFE : produit':
        code_var1 = 'CFE_PROD_GFP_2020'
        titreindic1 = "Produit 2020 de la Cotisation foncière des entreprises (CFE)" 
    if selec == 'CVAE : total':
        code_var1 = 'CVAE_GFP_2020'
        titreindic1 = "Cotisation sur la valeur ajoutée des entreprises, 2020" 
    if selec == 'CVAE : due':
        code_var1 = 'CVAE_DUE_GFP_2020'
        titreindic1 = "Cotisation sur la valeur ajoutée des entreprises due (payée par les entreprises), 2020" 
    if selec == 'CVAE : dégrevements':
        code_var1 = 'CVAE_DEG_GFP_2020'
        titreindic1 = "Dégrévements de la Cotisation sur la valeur ajoutée des entreprises, 2020"
    if selec == 'Tascom':
        code_var1 = 'TASCOM_2020'
        titreindic1 = "Taxe sur les surfaces commerciales (Tascom) -2019 ou 2020-"
    if selec == 'IFER':
        code_var1 = 'IFER_2020'
        titreindic1 = "Imposition forfaitaire des entreprises de réseaux (IFER) -provisoire-"
    if selec == 'ajustement TP':
        code_var1 = 'Compensation_reforme_TP'
        titreindic1 = "Ajustement réforme de la taxe professionnelle* (impact sur les dotations perçues)"
    if selec == 'Total (sans ajustement)':
        code_var1 = 'Total_2020'
        titreindic1 = "Fiscalité économique locale (sans ajustement réforme TP)"
    if selec == 'Total (avec ajustement)':
        code_var1 = 'Total2020_cor'
        titreindic1 = "Fiscalité économique locale (avec ajustement réforme TP)"    
    if selec == 'TAFNB':
        code_var1 = 'TAFNB_PROD_GFP_2020'
        titreindic1 = "Taxe foncière additionne sur les propriétés non bâties, 2020"
    data_carte['poids_dans_amp']=data_carte[code_var1]/(data_carte[code_var1].sum())*1000
    data_carte['ecart']=((data_carte[code_var1]/(data_carte[code_var1].sum())/(data_carte['POP_INSEE']/(data_carte['POP_INSEE'].sum())))*100)-100
    data_carte['en_euros_par_habitant']=data_carte[code_var1]/data_carte['POP_INSEE']
    data_carte['en_milliers']=data_carte[code_var1]/1000
    with c1 :
    	choix_unit1 = st.selectbox("Choix de l'unité",('en € par habitant','en 1000 €', 'écart la moyenne par hab.','en 0/00 de la Métropole'))
    if choix_unit1 =='en € par habitant':
        indic1 = 'en_euros_par_habitant'
    if choix_unit1 == 'écart à la moyenne par hab.':
        indic1='ecart'
    if choix_unit1 =='en 0/00 de la Métropole':
        indic1 = 'poids_dans_amp'
    if choix_unit1 =='en 1000 €':
        indic1 = 'en_milliers'
    source = "Source : calculs sur données DGFIP et DGCL"
    carac="Non"
    cartographie_classe()


if choix == 'Evolution entre 2016 et 2020 des composantes de la CET des communes de la Métropole Aix-Marseille-Provence':
    titre_evo_2016_2020()
    data_carte=chargement_data_carte_base().copy()
    data_carte['CET_GFP_2020']=data_carte['CVAE_GFP_2020']+data_carte['CFE_PROD_GFP_2020']
    data_carte['CET_GFP_2016']=data_carte['CVAE_GFP_2016']+data_carte['CFE_PROD_GFP_2016']
    #st.title('Contributions des 92 communes à la Métropole')
    #st.header('Selectionner dans le menu déroulant la ressource fiscale')
    #code_var1="att1"
    #code_var2="att2"
    c1, c2,c3 = st.beta_columns((2, 8,2))
    with c1:
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	selec2 = st.selectbox("Choix de l'impôt",('CVAE','CFE : base','CFE : produit'))
    if selec2 == 'CVAE':
        code_var1 = 'CVAE_GFP_2020'
        code_var2 = 'CVAE_GFP_2016'
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
    with c1 :
    	choix_unit1 = st.selectbox("Choix de l'unité",('en € par habitant',"taux de croissance",'en K€'))
    if choix_unit1 =='taux de croissance':
       	indic1 = 'TC'
    if choix_unit1 == 'en K€':
       	indic1='ecart en k€'
    if choix_unit1 == 'en € par habitant':
       	indic1='ecart en euro par hab'
    source = "Source : calculs sur données DGFIP et DGCL"
    carac="Non"
    cartographie_classe()
    #st.dataframe(data_carte)



if choix == 'Caractéristiques des communes':
    titre_caracteristiques_communes()
    data_carte=chargement_data_carte_base().copy()
    #st.sidebar.title('Contributions des 92 communes à la Métropole')
    #c1, c2 = st.beta_columns((4, 1))
    #st.header('Selectionner dans le menu déroulant la ressource fiscale')
    #st.sidebar.header('INDICATEURS')
    c1, c2,c3 = st.beta_columns((2, 8,2))
    with c1:
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	st.write(" ")
    	selec3 = st.radio(" ",('Part des logements sociaux', 'Revenu imposable par habitant','Potentiel financier par habitant','Recettes réelles de fonctionnement par habitant','Allocation de compensation sur recettes réelles de fonctionnement'))
    if selec3 == 'Part des logements sociaux':
        code_var1 = 'PART_LOGEMENT_SOCIAUX'
        titreindic1 = "Part des logements sociaux dans les logements soumis à la taxe d'habitation, en %"
    if selec3 == 'Revenu imposable par habitant':
        code_var1 = 'REV_IMPOSABLE_PAR_HAB'
        titreindic1 = "Revenu imposable par habitant, en €"
    if selec3 == 'Recettes réelles de fonctionnement par habitant':
        data_carte['RRF_PAR_HAB']=data_carte['RRF']/data_carte['POP_DGF']
        code_var1 = 'RRF_PAR_HAB'
        titreindic1 = "Recettes réelles de fonctionnement par habitant, en €" 
    if selec3 == 'Potentiel financier par habitant':
        code_var1 = 'POTENTIEL_FINANCIER_PAR_HAB'
        titreindic1 = "Potentiel financier par habitant, 2020, en €" 
    if selec3 == 'Allocation de compensation sur recettes réelles de fonctionnement':
        code_var1 = 'AC_RRF'
        titreindic1 = "Poids de l'allocation de compensation dans les recettes réelles de fonctionnement, en %" 
    with c1 :
    	choix_unit1 = " "
    indic1 = code_var1
    carac="Oui"
    source = "Source : calculs sur données DGCL"
    cartographie_classe()



# module simulation AC
if choix == "Mesurer l'impact d'une révision de l'attribution de compensation pour les communes de la Métropole":
    titre_rev_ac()
    data_carte=chargement_data_carte_base().copy()
    data_carte['RRF_5pc']=data_carte['5pc_RFF']*1
    data_carte['PF_hab_com / PF_hab_mpm']=data_carte['RATIO_PF']/100
    data_carte['Attribution de compensation de la commune']=data_carte['AC']
    data_carte["Recettes réelles de fonctionnement des communes N-2"]=data_carte["RRF"]*1
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
        pfsup = st.number_input("Ecart avec le potentiel financier moyen de la Métropole (20 % ou plus) ", min_value=20, value=20, step=1)
        pfsup = 1+pfsup/100
        taux_reduc_pf = st.number_input("Objectif de % de réduction de l'AC", max_value=5, value=5, step=1)
        data_carte["AC_PFsup"] = np.where(data_carte["PF_hab_com / PF_hab_mpm"] >pfsup, data_carte['Attribution de compensation de la commune'],0)
        data_carte['AC_PFsup_reduc']=data_carte['AC_PFsup']*taux_reduc_pf/100
        data_carte["AC_PFsup_reduc_max"] = np.where(data_carte["AC_PFsup_reduc"] > data_carte["RRF_5pc"], data_carte["RRF_5pc"],data_carte["AC_PFsup_reduc"])
        indic1 = "AC_PFsup_reduc_max"
        eco_mpm = data_carte["AC_PFsup_reduc_max"].sum()
        eco_mpm=int(eco_mpm)
        titre = "Montant de la réduction des AC en tenant compte de la limite maximale de 5 % des recettes de fonctionnement, en € "
        source = "calculs sur données DGCL"
        st.set_option('deprecation.showPyplotGlobalUse', False)
        data_carte = data_carte.to_crs(epsg=3857)
        unite = 1000 #mettre 1 si on maintient l'unité
        centroids = data_carte.copy()
        centroids.geometry =data_carte.centroid
        centroids['size'] = centroids[indic1] / unite  # to get reasonable plotable number
        ax = data_carte.plot(facecolor='beige', alpha=0.9, edgecolor='k',figsize=(14, 14))
        ax.set_title(titre)
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #centroids.plot(markersize='size', color = '#FFE4B5',ax=ax)
        centroids.plot(markersize='size', color = 'blue',alpha=0.4, ax=ax)
        gl = plt.scatter([],[], s=10, marker='o', color='#555555')
        ga = plt.scatter([],[], s=100, marker='o', color='#555555')
        ensemble_des_communes()
        #principales_communes()
        plt.legend((gl,ga),('10 000', '100 000'),scatterpoints=1,loc='upper left',ncol=1,fontsize=12)
        #plt.savefig(indic1+'_circle.jpg')
        #plt.savefig(indic1+"_circle.pdf", bbox_inches='tight')
        st.pyplot()
        st.write('gain pour la métropole :',eco_mpm)
        mycol=['codgeo','commune',indic1]
        tab = data_carte[mycol]
        tab[indic1]=tab[indic1].round()
        with st.beta_expander("Afficher le tableau avec les données"):
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
        taux_reduc = st.number_input("% de réduction de l'AC (dans la limite de 30%)", max_value=30, value=10, step=1)
        data_carte['reduc1']=data_carte['Attribution de compensation de la commune']*taux_reduc/100
        data_carte["reduc_max1"] = np.where(data_carte["reduc1"] > data_carte["RRF_5pc"], data_carte["RRF_5pc"],data_carte["reduc1"])
        data_carte["reduc_max1"] = np.where(data_carte["reduc_max1"] <0, 0,data_carte["reduc_max1"])
        data_carte["en % des RRF"]=data_carte["reduc_max1"]/data_carte["Recettes réelles de fonctionnement des communes N-2"]*100
        indic2 = "reduc_max1"
        eco_mpm2 = data_carte["reduc_max1"].sum()
        eco_mpm2=int(eco_mpm2)
        titre = "Montant de la réduction des AC en tenant compte de la limite maximale de 5 % des recettes de fonctionnement, € "
        source = "calculs sur données DGCL"
        st.set_option('deprecation.showPyplotGlobalUse', False)
        data_carte = data_carte.to_crs(epsg=3857)
        unite = 1000 #mettre 1 si on maintient l'unité
        centroids = data_carte.copy()
        centroids.geometry =data_carte.centroid
        centroids['size'] = centroids[indic2] / unite  # to get reasonable plotable number
        ax = data_carte.plot(facecolor='beige', alpha=0.9, edgecolor='k',figsize=(14, 14))
        ax.set_title(titre)
        plt.figtext(.15,.22,source,fontsize=12,ha='left')
        ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron) # fonds de carte
        #centroids.plot(markersize='size', color = '#FFE4B5',ax=ax)
        centroids.plot(markersize='size', color = 'blue',alpha=0.4, ax=ax)
        gl = plt.scatter([],[], s=10, marker='o', color='#555555')
        ga = plt.scatter([],[], s=100, marker='o', color='#555555')
        ensemble_des_communes()
        #plt.savefig(indic2+'_circle.jpg')
        #plt.savefig(indic2+"_circle.pdf", bbox_inches='tight')
        #principales_communes()
        plt.legend((gl,ga),('10 000', '100 000'),scatterpoints=1,loc='upper left',ncol=1,fontsize=12)
        st.pyplot()
        st.write('gain pour la métropole :',eco_mpm2)
        mycol=['codgeo','commune',indic2,"en % des RRF"]
        tab = data_carte[mycol]
        tab[indic2]=tab[indic2].round()
        tab["en % des RRF"]=tab["en % des RRF"].round(1)
        with st.beta_expander("Afficher le tableau avec les données"):
            st.dataframe(tab)




st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
st.sidebar.write(' ')
expander_bar = st.sidebar.beta_expander("A propos")
expander_bar.markdown("""
* **Auteur :** olivier Boylaud  (olivier@boylaud.eu)
* **Sources des données : ** DGCL et DGFIP.
""")



