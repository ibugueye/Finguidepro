import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="FinGuide Pro - Prototype",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
    }
    .module-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #3B82F6;
    }
    .financial-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .ratio-good { color: #10B981; font-weight: bold; }
    .ratio-warning { color: #F59E0B; font-weight: bold; }
    .ratio-danger { color: #EF4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
def create_balance_sheet_template():
    return {
        'Actif': {
            'Actif Immobilisé': {
                'Immobilisations incorporelles': 0.0,
                'Immobilisations corporelles': 0.0,
                'Immobilisations financières': 0.0
            },
            'Actif Circulant': {
                'Stocks': 0.0,
                'Créances clients': 0.0,
                'Disponibilités': 0.0,
                'Autres actifs circulants': 0.0
            }
        },
        'Passif': {
            'Capitaux Propres': {
                'Capital social': 0.0,
                'Réserves': 0.0,
                'Résultat de l\'exercice': 0.0
            },
            'Dettes': {
                'Dettes financières': 0.0,
                'Dettes fournisseurs': 0.0,
                'Autres dettes': 0.0
            }
        }
    }

def create_income_statement_template():
    return {
        'Chiffre_affaires': 0.0,
        'Achats_marchandises': 0.0,
        'Variation_stocks': 0.0,
        'Autres_achats_charges_externes': 0.0,
        'Impots_taxes': 0.0,
        'Charges_personnel': 0.0,
        'Dotations_amortissements': 0.0,
        'Autres_charges': 0.0,
        'Produits_financiers': 0.0,
        'Charges_financieres': 0.0,
        'Impot_benefices': 0.0
    }

def calculate_ratios(balance_sheet, income_statement):
    ratios = {}
    
    try:
        if not balance_sheet or not income_statement:
            return ratios
            
        actif_circulant = sum(balance_sheet['Actif']['Actif Circulant'].values())
        passif_circulant = sum(balance_sheet['Passif']['Dettes'].values())
        total_actif = sum([sum(v.values()) for v in balance_sheet['Actif'].values()])
        total_passif = sum([sum(v.values()) for v in balance_sheet['Passif'].values()])
        
        # Calcul des ratios
        if passif_circulant > 0:
            ratios['Fond_de_Roulement'] = actif_circulant - passif_circulant
            ratios['Ratio_de_Liquidite'] = actif_circulant / passif_circulant
        else:
            ratios['Fond_de_Roulement'] = actif_circulant
            ratios['Ratio_de_Liquidite'] = float('inf')
            
        ca = income_statement.get('Chiffre_affaires', 0.0)
        resultat_net = ca - sum([v for k, v in income_statement.items() 
                               if k not in ['Chiffre_affaires', 'Produits_financiers']])
        
        if total_actif > 0:
            ratios['ROA'] = (resultat_net / total_actif) * 100
            
    except Exception as e:
        st.error(f"Erreur dans le calcul des ratios: {e}")
        
    return ratios

def generate_excel_report(balance_sheet, income_statement, ratios):
    # Création d'un DataFrame Excel
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Feuille Bilan
        bilan_data = []
        for category, items in balance_sheet.items():
            for subcategory, values in items.items():
                for item, amount in values.items():
                    bilan_data.append({
                        'Catégorie': category,
                        'Sous-catégorie': subcategory,
                        'Poste': item,
                        'Montant (€)': amount
                    })
        
        if bilan_data:
            df_bilan = pd.DataFrame(bilan_data)
            df_bilan.to_excel(writer, sheet_name='Bilan', index=False)
        
        # Feuille Compte de résultat
        if income_statement:
            df_income = pd.DataFrame(list(income_statement.items()), columns=['Poste', 'Valeur (€)'])
            df_income.to_excel(writer, sheet_name='Compte de résultat', index=False)
        
        # Feuille Ratios
        if ratios:
            df_ratios = pd.DataFrame(list(ratios.items()), columns=['Ratio', 'Valeur'])
            df_ratios.to_excel(writer, sheet_name='Ratios', index=False)
    
    return output.getvalue()

# Interface principale
def main():
    # Initialisation des données de session
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'balance_sheet' not in st.session_state:
        st.session_state.balance_sheet = create_balance_sheet_template()
    if 'income_statement' not in st.session_state:
        st.session_state.income_statement = create_income_statement_template()
    
    # En-tête
    st.markdown('<h1 class="main-header">📊 FinGuide Pro - Prototype</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 2rem;'>
    Application didactique d'analyse financière - Learning by Doing
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Navigation
    with st.sidebar:
        st.markdown("### 📚 Modules")
        
        module = st.radio(
            "Choisissez un module:",
            ["🏠 Dashboard", "📑 Bilan Comptable", "💰 Compte de Résultat", 
             "📈 Analyse Financière", "🎯 Budget & Prévisions", "⚙️ Paramètres"]
        )
        
        st.markdown("---")
        st.markdown("### 🎓 Niveau")
        niveau = st.select_slider(
            "Complexité:",
            options=["Débutant", "Intermédiaire", "Expert"]
        )
        
        st.markdown("---")
        st.markdown("### 🏢 Secteur")
        secteur = st.selectbox(
            "Votre secteur d'activité:",
            ["Commerce", "Industrie", "Services", "Technologie", "Construction"]
        )
        
        if st.button("🔁 Réinitialiser les données"):
            st.session_state.balance_sheet = create_balance_sheet_template()
            st.session_state.income_statement = create_income_statement_template()
            st.session_state.current_step = 0
            st.rerun()
    
    # Contenu principal selon le module sélectionné
    if module == "🏠 Dashboard":
        show_dashboard()
    elif module == "📑 Bilan Comptable":
        show_balance_sheet()
    elif module == "💰 Compte de Résultat":
        show_income_statement()
    elif module == "📈 Analyse Financière":
        show_financial_analysis()
    elif module == "🎯 Budget & Prévisions":
        show_budgeting()
    elif module == "⚙️ Paramètres":
        show_settings()

def show_dashboard():
    st.markdown('<h2 class="sub-header">Tableau de Bord</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Progression", "25%", "5%")
    with col2:
        st.metric("Exercices complétés", "3", "1")
    with col3:
        st.metric("Ratios calculés", "12", "3")
    
    # Statistiques rapides
    st.markdown("### 🎯 Objectifs d'apprentissage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="module-card">
        <h4>📑 Comprendre le Bilan</h4>
        <ul>
        <li>Structure Actif/Passif</li>
        <li>Équilibre comptable</li>
        <li>Postes clés</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>💰 Analyser la Rentabilité</h4>
        <ul>
        <li>Calcul des marges</li>
        <li>Soldes intermédiaires</li>
        <li>ROE/ROA</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="module-card">
        <h4>📈 Maîtriser les Ratios</h4>
        <ul>
        <li>Liquidité & Solvabilité</li>
        <li>Efficacité opérationnelle</li>
        <li>Benchmarks sectoriels</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🎯 Créer des Prévisions</h4>
        <ul>
        <li>Budget de trésorerie</li>
        <li>Scénarios what-if</li>
        <li>Plan de financement</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Progression visuelle
    st.markdown("### 📊 Progression de l'apprentissage")
    
    progress_data = {
        'Module': ['Bilan', 'Compte Résultat', 'Ratios', 'Budget', 'Reporting'],
        'Progression (%)': [80, 60, 40, 20, 10]
    }
    
    fig = px.bar(progress_data, x='Module', y='Progression (%)',
                 color='Progression (%)',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

def show_balance_sheet():
    st.markdown('<h2 class="sub-header">📑 Assistant Bilan Comptable</h2>', unsafe_allow_html=True)
    
    # Initialiser le bilan si vide
    if not st.session_state.balance_sheet:
        st.session_state.balance_sheet = create_balance_sheet_template()
    
    # Assistant pas-à-pas
    steps = [
        "Définition des immobilisations",
        "Saisie des actifs circulants",
        "Structure des capitaux propres",
        "Enregistrement des dettes",
        "Vérification de l'équilibre"
    ]
    
    # Convertir current_step en int pour le selectbox
    current_step_index = int(st.session_state.current_step)
    
    # Créer le selectbox avec index entier
    current_step = st.selectbox("Étape en cours:", steps, index=current_step_index)
    
    # Mettre à jour l'étape courante (stockée comme int)
    st.session_state.current_step = steps.index(current_step)
    
    # Afficher la progression
    st.progress((st.session_state.current_step + 1) / len(steps))
    
    # Aide contextuelle
    with st.expander("💡 Aide - " + current_step):
        if current_step == steps[0]:
            st.info("""
            **Immobilisations**: Biens durables détenus par l'entreprise pour son activité.
            - Incorporelles: Brevets, logiciels, fonds commercial
            - Corporelles: Bâtiments, machines, véhicules
            - Financières: Participations, prêts à long terme
            """)
        elif current_step == steps[1]:
            st.info("""
            **Actif circulant**: Biens et créances transformables en liquidités à court terme.
            - Stocks: Marchandises, matières premières
            - Créances: Factures clients en attente de paiement
            - Disponibilités: Comptes bancaires, caisse
            """)
        elif current_step == steps[2]:
            st.info("""
            **Capitaux propres**: Ressources stables de l'entreprise appartenant aux actionnaires.
            - Capital social: Apports des actionnaires
            - Réserves: Bénéfices non distribués des années antérieures
            - Résultat de l'exercice: Bénéfice ou perte de l'année
            """)
        elif current_step == steps[3]:
            st.info("""
            **Dettes**: Ressources externes que l'entreprise devra rembourser.
            - Dettes financières: Emprunts bancaires
            - Dettes fournisseurs: Factures à payer aux fournisseurs
            - Autres dettes: Charges à payer, dettes fiscales
            """)
        elif current_step == steps[4]:
            st.info("""
            **Équilibre du bilan**: L'actif doit toujours égaler le passif.
            - Vérifiez que Total Actif = Total Passif
            - Un déséquilibre indique une erreur de saisie
            """)
    
    # Interface de saisie par catégorie
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 ACTIF")
        
        # Actif Immobilisé
        st.markdown("#### Actif Immobilisé")
        for item in st.session_state.balance_sheet['Actif']['Actif Immobilisé']:
            st.session_state.balance_sheet['Actif']['Actif Immobilisé'][item] = st.number_input(
                f"{item}:", 
                value=float(st.session_state.balance_sheet['Actif']['Actif Immobilisé'][item]),
                step=1000.0,
                format="%.2f",
                key=f"ai_{item}"
            )
        
        # Actif Circulant
        st.markdown("#### Actif Circulant")
        for item in st.session_state.balance_sheet['Actif']['Actif Circulant']:
            st.session_state.balance_sheet['Actif']['Actif Circulant'][item] = st.number_input(
                f"{item}:",
                value=float(st.session_state.balance_sheet['Actif']['Actif Circulant'][item]),
                step=1000.0,
                format="%.2f",
                key=f"ac_{item}"
            )
    
    with col2:
        st.markdown("### 📋 PASSIF")
        
        # Capitaux Propres
        st.markdown("#### Capitaux Propres")
        for item in st.session_state.balance_sheet['Passif']['Capitaux Propres']:
            st.session_state.balance_sheet['Passif']['Capitaux Propres'][item] = st.number_input(
                f"{item}:",
                value=float(st.session_state.balance_sheet['Passif']['Capitaux Propres'][item]),
                step=1000.0,
                format="%.2f",
                key=f"cp_{item}"
            )
        
        # Dettes
        st.markdown("#### Dettes")
        for item in st.session_state.balance_sheet['Passif']['Dettes']:
            st.session_state.balance_sheet['Passif']['Dettes'][item] = st.number_input(
                f"{item}:",
                value=float(st.session_state.balance_sheet['Passif']['Dettes'][item]),
                step=1000.0,
                format="%.2f",
                key=f"d_{item}"
            )
    
    # Navigation entre étapes
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    
    with col_nav1:
        if st.button("◀️ Étape précédente"):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
                st.rerun()
    
    with col_nav3:
        if st.button("Étape suivante ▶️"):
            if st.session_state.current_step < len(steps) - 1:
                st.session_state.current_step += 1
                st.rerun()
    
    # Calcul et vérification
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
    total_passif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Passif'].values()])
    
    with col1:
        st.metric("Total Actif", f"{total_actif:,.2f} €")
    with col2:
        st.metric("Total Passif", f"{total_passif:,.2f} €")
    with col3:
        difference = total_actif - total_passif
        status = "✅ Équilibré" if abs(difference) < 0.01 else "⚠️ Déséquilibre"
        st.metric("Équilibre", status, f"{difference:,.2f} €")
    
    # Visualisation
    st.markdown("### 📊 Visualisation du Bilan")
    
    # Préparation des données pour le graphique
    categories = []
    values = []
    
    for category, items in st.session_state.balance_sheet.items():
        for subcategory, values_dict in items.items():
            for item, value in values_dict.items():
                if value > 0:
                    categories.append(f"{category} - {item}")
                    values.append(value)
    
    if values:
        fig = px.pie(names=categories, values=values, 
                     title="Structure du Bilan",
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Export Excel
    if st.button("📥 Exporter vers Excel"):
        excel_data = generate_excel_report(
            st.session_state.balance_sheet,
            st.session_state.income_statement,
            {}
        )
        
        st.download_button(
            label="💾 Télécharger le bilan Excel",
            data=excel_data,
            file_name=f"bilan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def show_income_statement():
    st.markdown('<h2 class="sub-header">💰 Assistant Compte de Résultat</h2>', unsafe_allow_html=True)
    
    # Initialiser le compte de résultat si vide
    if not st.session_state.income_statement:
        st.session_state.income_statement = create_income_statement_template()
    
    # Aide contextuelle
    with st.expander("💡 Aide - Concepts clés"):
        st.info("""
        **Compte de résultat**: Document qui présente les produits et charges de l'exercice.
        - Chiffre d'affaires: Ventes de biens et services
        - Achats: Coût des marchandises vendues
        - Charges de personnel: Salaires et charges sociales
        - Dotations: Amortissements et provisions
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Produits")
        
        # Chiffre d'affaires
        st.session_state.income_statement['Chiffre_affaires'] = st.number_input(
            "Chiffre d'affaires HT:",
            value=float(st.session_state.income_statement['Chiffre_affaires']),
            step=1000.0,
            format="%.2f",
            help="Montant total des ventes de l'exercice"
        )
        
        # Produits financiers
        st.session_state.income_statement['Produits_financiers'] = st.number_input(
            "Produits financiers:",
            value=float(st.session_state.income_statement['Produits_financiers']),
            step=1000.0,
            format="%.2f",
            help="Intérêts perçus, revenus de placements"
        )
    
    with col2:
        st.markdown("### 📉 Charges")
        
        # Achats et stocks
        st.session_state.income_statement['Achats_marchandises'] = st.number_input(
            "Achats de marchandises:",
            value=float(st.session_state.income_statement['Achats_marchandises']),
            step=1000.0,
            format="%.2f"
        )
        
        st.session_state.income_statement['Variation_stocks'] = st.number_input(
            "Variation de stocks:",
            value=float(st.session_state.income_statement['Variation_stocks']),
            step=1000.0,
            format="%.2f",
            help="Stock initial - Stock final (positif si diminution)"
        )
        
        # Charges externes
        st.session_state.income_statement['Autres_achats_charges_externes'] = st.number_input(
            "Autres achats et charges externes:",
            value=float(st.session_state.income_statement['Autres_achats_charges_externes']),
            step=1000.0,
            format="%.2f"
        )
        
        st.session_state.income_statement['Impots_taxes'] = st.number_input(
            "Impôts et taxes:",
            value=float(st.session_state.income_statement['Impots_taxes']),
            step=1000.0,
            format="%.2f"
        )
        
        # Charges de personnel
        st.session_state.income_statement['Charges_personnel'] = st.number_input(
            "Charges de personnel:",
            value=float(st.session_state.income_statement['Charges_personnel']),
            step=1000.0,
            format="%.2f"
        )
        
        # Dotations
        st.session_state.income_statement['Dotations_amortissements'] = st.number_input(
            "Dotations aux amortissements:",
            value=float(st.session_state.income_statement['Dotations_amortissements']),
            step=1000.0,
            format="%.2f"
        )
        
        # Autres charges
        st.session_state.income_statement['Autres_charges'] = st.number_input(
            "Autres charges:",
            value=float(st.session_state.income_statement['Autres_charges']),
            step=1000.0,
            format="%.2f"
        )
        
        # Charges financières
        st.session_state.income_statement['Charges_financieres'] = st.number_input(
            "Charges financières:",
            value=float(st.session_state.income_statement['Charges_financieres']),
            step=1000.0,
            format="%.2f"
        )
        
        # Impôt sur les bénéfices
        st.session_state.income_statement['Impot_benefices'] = st.number_input(
            "Impôt sur les bénéfices:",
            value=float(st.session_state.income_statement['Impot_benefices']),
            step=1000.0,
            format="%.2f"
        )
    
    # Calcul des soldes intermédiaires de gestion
    st.markdown("---")
    st.markdown("### 🧮 Soldes Intermédiaires de Gestion")
    
    # Récupération des valeurs
    CA = st.session_state.income_statement.get('Chiffre_affaires', 0.0)
    achats = st.session_state.income_statement.get('Achats_marchandises', 0.0)
    var_stocks = st.session_state.income_statement.get('Variation_stocks', 0.0)
    autres_charges = st.session_state.income_statement.get('Autres_achats_charges_externes', 0.0)
    charges_personnel = st.session_state.income_statement.get('Charges_personnel', 0.0)
    dotations = st.session_state.income_statement.get('Dotations_amortissements', 0.0)
    produits_financiers = st.session_state.income_statement.get('Produits_financiers', 0.0)
    charges_financieres = st.session_state.income_statement.get('Charges_financieres', 0.0)
    impot = st.session_state.income_statement.get('Impot_benefices', 0.0)
    
    # Calculs
    marge_commerciale = CA - achats + var_stocks if CA > 0 else 0.0
    valeur_ajoutee = marge_commerciale - autres_charges
    ebe = valeur_ajoutee - charges_personnel
    resultat_exploitation = ebe - dotations
    resultat_courant = resultat_exploitation + produits_financiers - charges_financieres
    resultat_net = resultat_courant - impot
    
    # Affichage des SIG
    sig_data = {
        'Solde': ['Marge Commerciale', 'Valeur Ajoutée', 'EBE', 'Résultat Exploitation', 'Résultat Courant', 'Résultat Net'],
        'Valeur (€)': [marge_commerciale, valeur_ajoutee, ebe, resultat_exploitation, resultat_courant, resultat_net]
    }
    
    df_sig = pd.DataFrame(sig_data)
    st.dataframe(df_sig.style.format({'Valeur (€)': '{:,.2f} €'}), use_container_width=True)
    
    # Graphique des SIG
    if any([abs(v) > 0 for v in [marge_commerciale, valeur_ajoutee, ebe, resultat_exploitation, resultat_courant, resultat_net]]):
        fig = px.bar(df_sig, x='Solde', y='Valeur (€)', 
                     title="Évolution des Soldes Intermédiaires",
                     color='Valeur (€)',
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

def show_financial_analysis():
    st.markdown('<h2 class="sub-header">📈 Analyse Financière Interactive</h2>', unsafe_allow_html=True)
    
    # Vérification des données disponibles
    if not st.session_state.balance_sheet or not st.session_state.income_statement:
        st.warning("⚠️ Veuillez d'abord compléter le bilan et le compte de résultat")
        return
    
    # Calcul des ratios
    ratios = calculate_ratios(st.session_state.balance_sheet, st.session_state.income_statement)
    
    # Affichage des ratios par catégorie
    tabs = st.tabs(["📊 Ratios Clés", "📈 Tendances", "🏢 Benchmark Sectoriel", "🎯 Recommandations"])
    
    with tabs[0]:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 💧 Liquidité")
            fr = ratios.get('Fond_de_Roulement', 0.0)
            liquidite = ratios.get('Ratio_de_Liquidite', 0.0)
            
            st.metric("Fond de Roulement", f"{fr:,.2f} €")
            st.metric("Ratio de Liquidité", f"{liquidite:.2f}")
            
            if liquidite > 1.5:
                st.success("✅ Excellente liquidité")
            elif liquidite > 1:
                st.warning("⚠️ Liquidité à surveiller")
            else:
                st.error("❌ Risque de liquidité")
        
        with col2:
            st.markdown("##### 🏦 Solvabilité")
            total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
            total_dettes = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
            
            if total_actif > 0:
                taux_endettement = (total_dettes / total_actif) * 100
                st.metric("Taux d'endettement", f"{taux_endettement:.1f}%")
                
                if taux_endettement < 50:
                    st.success("✅ Structure financière saine")
                elif taux_endettement < 70:
                    st.warning("⚠️ Endettement modéré")
                else:
                    st.error("❌ Endettement élevé")
        
        with col3:
            st.markdown("##### 📈 Rentabilité")
            CA = st.session_state.income_statement.get('Chiffre_affaires', 0.0)
            
            # Calcul du résultat net
            charges_totales = sum([v for k, v in st.session_state.income_statement.items() 
                                  if k not in ['Chiffre_affaires', 'Produits_financiers']])
            resultat_net = CA - charges_totales
            
            if CA > 0:
                marge_nette = (resultat_net / CA) * 100
                st.metric("Marge Nette", f"{marge_nette:.1f}%")
                
                total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
                if total_actif > 0:
                    roa = (resultat_net / total_actif) * 100
                    st.metric("ROA", f"{roa:.1f}%")
    
    with tabs[1]:
        # Simulation de données historiques
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun']
        ca_data = [100000 * (1 + i * 0.05) for i in range(len(months))]
        marge_data = [ca_data[i] * 0.15 * (0.95 + i * 0.01) for i in range(len(months))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=ca_data, mode='lines+markers', 
                                name='Chiffre d\'affaires', yaxis='y1'))
        fig.add_trace(go.Bar(x=months, y=marge_data, name='Marge brute', yaxis='y2'))
        
        fig.update_layout(
            title='Évolution du CA et des Marges',
            yaxis=dict(title='CA (€)', side='left'),
            yaxis2=dict(title='Marge (€)', side='right', overlaying='y'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        # Benchmarks fictifs par secteur
        secteur_benchmarks = {
            'Commerce': {'marge_nette': 3.5, 'roa': 8.2, 'liquidite': 1.8},
            'Industrie': {'marge_nette': 6.2, 'roa': 9.5, 'liquidite': 1.5},
            'Services': {'marge_nette': 12.5, 'roa': 11.3, 'liquidite': 1.9},
            'Technologie': {'marge_nette': 18.7, 'roa': 15.2, 'liquidite': 2.3},
            'Construction': {'marge_nette': 4.1, 'roa': 7.8, 'liquidite': 1.4}
        }
        
        selected_sector = st.selectbox("Choisissez un secteur de comparaison:", 
                                      list(secteur_benchmarks.keys()))
        
        benchmark = secteur_benchmarks[selected_sector]
        
        # Calcul des valeurs actuelles
        CA = st.session_state.income_statement.get('Chiffre_affaires', 1.0)
        charges_totales = sum([v for k, v in st.session_state.income_statement.items() 
                              if k not in ['Chiffre_affaires', 'Produits_financiers']])
        resultat_net = CA - charges_totales
        marge_nette_perso = (resultat_net / CA) * 100 if CA > 0 else 0
        
        total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
        roa_perso = (resultat_net / total_actif) * 100 if total_actif > 0 else 0
        
        actif_circulant = sum(st.session_state.balance_sheet['Actif']['Actif Circulant'].values())
        passif_circulant = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
        liquidite_perso = actif_circulant / passif_circulant if passif_circulant > 0 else 0
        
        comparison_data = {
            'Ratio': ['Marge Nette (%)', 'ROA (%)', 'Ratio de Liquidité'],
            'Votre entreprise': [marge_nette_perso, roa_perso, liquidite_perso],
            'Secteur': [benchmark['marge_nette'], benchmark['roa'], benchmark['liquidite']]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison.style.format({
            'Votre entreprise': '{:.1f}',
            'Secteur': '{:.1f}'
        }), use_container_width=True)
        
        # Graphique de comparaison
        fig = px.bar(df_comparison.melt(id_vars=['Ratio']), 
                    x='Ratio', y='value', color='variable',
                    barmode='group', title=f"Comparaison avec le secteur {selected_sector}")
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown("### 🎯 Recommandations Personnalisées")
        
        # Analyse et recommandations basées sur les ratios
        recommendations = []
        
        # Calcul des ratios pour analyse
        actif_circulant = sum(st.session_state.balance_sheet['Actif']['Actif Circulant'].values())
        passif_circulant = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
        liquidite = actif_circulant / passif_circulant if passif_circulant > 0 else 0
        
        if liquidite < 1:
            recommendations.append({
                'Priorité': 'Haute',
                'Recommandation': 'Améliorer la liquidité : réduire le BFR, renégocier les délais fournisseurs',
                'Impact': 'Réduction du risque de défaut'
            })
        
        # Calcul d'autres indicateurs
        total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
        ca = st.session_state.income_statement.get('Chiffre_affaires', 0.0)
        
        if ca > 0 and total_actif > 0:
            rotation_actif = ca / total_actif
            if rotation_actif < 0.5:
                recommendations.append({
                    'Priorité': 'Moyenne',
                    'Recommandation': 'Améliorer la rotation des actifs : optimiser l\'utilisation des immobilisations',
                    'Impact': 'Augmentation de la rentabilité'
                })
        
        if recommendations:
            for rec in recommendations:
                priority_color = {
                    'Haute': '🔴',
                    'Moyenne': '🟡',
                    'Basse': '🟢'
                }.get(rec['Priorité'], '⚪')
                
                st.markdown(f"""
                <div class="financial-card">
                <h5>{priority_color} {rec['Priorité']} - {rec['Recommandation']}</h5>
                <p><em>Impact : {rec['Impact']}</em></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Votre situation financière semble saine. Continuez sur cette lancée!")

def show_budgeting():
    st.markdown('<h2 class="sub-header">🎯 Module Budget & Prévisions</h2>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 Budget des Ventes", "💰 Budget de Trésorerie", "📊 Scénarios What-If"])
    
    with tabs[0]:
        st.markdown("### 📋 Budget des Ventes")
        
        # Saisie des prévisions
        months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        
        budget_data = {}
        
        with st.form("budget_ventes_form"):
            st.markdown("#### Prévisions mensuelles")
            
            cols = st.columns(4)
            for i, month in enumerate(months):
                with cols[i % 4]:
                    budget_data[month] = st.number_input(
                        month,
                        value=10000.0,
                        step=1000.0,
                        format="%.2f",
                        key=f"budget_{month}"
                    )
            
            if st.form_submit_button("💾 Calculer le budget"):
                st.success("Budget calculé!")
        
        # Affichage du budget
        if budget_data:
            df_budget = pd.DataFrame({
                'Mois': list(budget_data.keys()),
                'Ventes Prévues': list(budget_data.values())
            })
            
            # Ajout de tendances
            df_budget['Cumul'] = df_budget['Ventes Prévues'].cumsum()
            df_budget['Variation %'] = df_budget['Ventes Prévues'].pct_change() * 100
            
            st.dataframe(df_budget.style.format({
                'Ventes Prévues': '{:,.2f} €',
                'Cumul': '{:,.2f} €',
                'Variation %': '{:.1f}%'
            }), use_container_width=True)
            
            # Graphique
            fig = px.line(df_budget, x='Mois', y=['Ventes Prévues', 'Cumul'],
                         title='Budget des Ventes - Prévisions Annuelle',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### 💰 Budget de Trésorerie Simplifié")
        
        # Saisie des flux
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Entrées de trésorerie")
            ca_encaisse = st.number_input("CA encaissé (€):", value=50000.0, step=1000.0, format="%.2f")
            autres_entrees = st.number_input("Autres entrées (€):", value=5000.0, step=1000.0, format="%.2f")
        
        with col2:
            st.markdown("#### Sorties de trésorerie")
            achats = st.number_input("Achats (€):", value=30000.0, step=1000.0, format="%.2f")
            charges_personnel = st.number_input("Charges personnel (€):", value=15000.0, step=1000.0, format="%.2f")
            autres_charges = st.number_input("Autres charges (€):", value=5000.0, step=1000.0, format="%.2f")
        
        # Calcul
        total_entrees = ca_encaisse + autres_entrees
        total_sorties = achats + charges_personnel + autres_charges
        solde_tresorerie = total_entrees - total_sorties
        
        # Affichage des résultats
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Entrées", f"{total_entrees:,.2f} €")
        with col2:
            st.metric("Total Sorties", f"{total_sorties:,.2f} €")
        with col3:
            st.metric("Solde Trésorerie", f"{solde_tresorerie:,.2f} €",
                     delta_color="inverse" if solde_tresorerie < 0 else "normal")
        
        # Recommandations
        if solde_tresorerie < 0:
            st.error("⚠️ Déficit de trésorerie prévisionnel. Actions recommandées:")
            st.markdown("""
            - Renégocier les délais de paiement avec les fournisseurs
            - Accélérer l'encaissement des créances clients
            - Échelonner les investissements
            - Rechercher des financements à court terme
            """)
    
    with tabs[2]:
        st.markdown("### 📊 Simulateur What-If")
        
        # Variables ajustables
        col1, col2 = st.columns(2)
        
        with col1:
            ca_base = st.slider("Chiffre d'affaires de base (€)", 50000, 200000, 100000, 5000)
            taux_marge = st.slider("Taux de marge brute (%)", 10.0, 50.0, 30.0, 1.0)
        
        with col2:
            evolution_ca = st.slider("Évolution du CA (%)", -20.0, 50.0, 10.0, 5.0)
            evolution_charges = st.slider("Évolution des charges fixes (%)", -10.0, 30.0, 5.0, 5.0)
        
        # Calcul des scénarios
        scenarios = {
            'Pessimiste': {'ca_mult': 0.8, 'marge_mult': 0.9},
            'Réaliste': {'ca_mult': 1.0, 'marge_mult': 1.0},
            'Optimiste': {'ca_mult': 1.2, 'marge_mult': 1.1}
        }
        
        scenario_results = []
        for scenario, params in scenarios.items():
            ca_scenario = ca_base * params['ca_mult'] * (1 + evolution_ca/100)
            marge_scenario = taux_marge * params['marge_mult']
            marge_brute = ca_scenario * marge_scenario / 100
            charges_fixes = 30000 * (1 + evolution_charges/100)
            resultat = marge_brute - charges_fixes
            
            scenario_results.append({
                'Scénario': scenario,
                'CA (€)': ca_scenario,
                'Marge Brute (€)': marge_brute,
                'Résultat (€)': resultat
            })
        
        df_scenarios = pd.DataFrame(scenario_results)
        st.dataframe(df_scenarios.style.format({
            'CA (€)': '{:,.2f} €',
            'Marge Brute (€)': '{:,.2f} €',
            'Résultat (€)': '{:,.2f} €'
        }), use_container_width=True)
        
        # Graphique comparatif
        fig = px.bar(df_scenarios, x='Scénario', y='Résultat (€)',
                    color='Résultat (€)', color_continuous_scale='RdYlGn',
                    title='Comparaison des scénarios')
        st.plotly_chart(fig, use_container_width=True)

def show_settings():
    st.markdown('<h2 class="sub-header">⚙️ Paramètres & Personnalisation</h2>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 Profil", "🎯 Préférences", "🔄 Intégrations", "💾 Données"])
    
    with tabs[0]:
        st.markdown("### 📋 Votre Profil")
        
        with st.form("profil_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom", value="John")
                prenom = st.text_input("Prénom", value="Doe")
                role = st.selectbox("Rôle", ["Comptable", "Contrôleur de Gestion", "Manager", "Étudiant", "Autre"])
            
            with col2:
                experience = st.selectbox("Expérience en finance", ["Débutant (< 1 an)", "Intermédiaire (1-3 ans)", "Confirmé (3-5 ans)", "Expert (> 5 ans)"])
                entreprise_taille = st.selectbox("Taille d'entreprise", ["TPE (< 10 salariés)", "PME (10-250)", "ETI (250-5000)", "Grand Groupe (> 5000)"])
                objectif = st.selectbox("Objectif principal", ["Apprentissage", "Analyse réelle", "Préparation certification", "Autre"])
            
            if st.form_submit_button("💾 Sauvegarder le profil"):
                st.success("Profil mis à jour!")
    
    with tabs[1]:
        st.markdown("### 🎯 Préférences d'apprentissage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mode_guide = st.checkbox("Mode guidé (recommandé)", value=True)
            show_tips = st.checkbox("Afficher les astuces contextuelles", value=True)
            auto_check = st.checkbox("Vérification automatique", value=True)
        
        with col2:
            difficulty = st.select_slider("Niveau de détail", 
                                         options=["Basique", "Standard", "Avancé", "Expert"])
            default_currency = st.selectbox("Devise par défaut", ["EUR €", "USD $", "GBP £", "CHF CHF"])
            language = st.selectbox("Langue", ["Français", "Anglais", "Espagnol"])
        
        if st.button("💾 Appliquer les préférences"):
            st.success("Préférences appliquées!")
    
    with tabs[2]:
        st.markdown("### 🔄 Intégrations")
        
        st.info("Connectez FinGuide Pro à vos outils existants")
        
        integration_options = st.multiselect(
            "Sélectionnez les intégrations à activer:",
            ["Excel/CSV Import", "Sage", "Cegid", "Quadratus", "QuickBooks", "SAP (version Entreprise)"]
        )
        
        if integration_options:
            st.write("**Intégrations sélectionnées:**")
            for option in integration_options:
                st.write(f"- ✅ {option}")
            
            if st.button("🔗 Configurer les intégrations"):
                st.info("Fonctionnalité en développement - Disponible dans la version Pro")
    
    with tabs[3]:
        st.markdown("### 💾 Gestion des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Exporter toutes les données"):
                # Générer un rapport complet
                if st.session_state.balance_sheet:
                    excel_data = generate_excel_report(
                        st.session_state.balance_sheet,
                        st.session_state.income_statement,
                        calculate_ratios(st.session_state.balance_sheet, st.session_state.income_statement)
                    )
                    
                    st.download_button(
                        label="💾 Télécharger le rapport complet",
                        data=excel_data,
                        file_name=f"finguide_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("Aucune donnée à exporter")
            
            if st.button("🗑️ Supprimer les données d'entraînement"):
                if st.checkbox("Je confirme la suppression"):
                    st.session_state.balance_sheet = create_balance_sheet_template()
                    st.session_state.income_statement = create_income_statement_template()
                    st.session_state.current_step = 0
                    st.success("Données d'entraînement supprimées!")
        
        with col2:
            uploaded_file = st.file_uploader("Importer des données", type=['xlsx', 'csv'])
            if uploaded_file is not None:
                st.success(f"Fichier {uploaded_file.name} importé avec succès!")
            
            # Créer un template Excel simple
            if st.button("📝 Générer template Excel"):
                # Créer un DataFrame simple pour le template
                template_data = pd.DataFrame({
                    'Poste': ['Immobilisations corporelles', 'Stocks', 'Créances clients', 
                             'Capital social', 'Dettes fournisseurs'],
                    'Valeur': [0.0, 0.0, 0.0, 0.0, 0.0]
                })
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    template_data.to_excel(writer, sheet_name='Template', index=False)
                
                st.download_button(
                    label="📥 Télécharger template Excel",
                    data=output.getvalue(),
                    file_name="template_finguide.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# Point d'entrée
if __name__ == "__main__":
    main()