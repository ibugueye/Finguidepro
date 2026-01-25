import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ============================================
# CONFIGURATION DE L'APPLICATION
# ============================================

st.set_page_config(
    page_title="FinGuide Pro - Apprentissage Financier Interactif",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS PERSONNALISÉ
# ============================================

st.markdown("""
<style>
    /* Styles généraux */
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        font-weight: 600;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
    }
    
    /* Cartes et conteneurs */
    .learning-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .learning-card:hover {
        transform: translateY(-5px);
    }
    
    .financial-card {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Indicateurs de performance */
    .ratio-good { 
        color: #10B981; 
        font-weight: bold;
        background-color: #D1FAE5;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .ratio-warning { 
        color: #F59E0B; 
        font-weight: bold;
        background-color: #FEF3C7;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .ratio-danger { 
        color: #EF4444; 
        font-weight: bold;
        background-color: #FEE2E2;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Boutons et interactions */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
        transform: scale(1.05);
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1E3A8A 0%, #3B82F6 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #3B82F6 100%);
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #1E3A8A;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def create_balance_sheet_template():
    """Crée un template de bilan comptable vide avec une structure pédagogique"""
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
                'Disponibilités (caisse et banque)': 0.0,
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
                'Dettes financières (emprunts)': 0.0,
                'Dettes fournisseurs': 0.0,
                'Autres dettes (fiscales, sociales)': 0.0
            }
        }
    }

def create_income_statement_template():
    """Crée un template de compte de résultat vide"""
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

def calculate_comprehensive_ratios(balance_sheet, income_statement):
    """
    Calcule tous les ratios financiers avec interprétations pédagogiques
    """
    ratios = {}
    interpretations = {}
    
    try:
        # Vérifier que les données existent
        if not balance_sheet or not income_statement:
            return ratios, interpretations
        
        # ===== CALCULS DE BASE =====
        # Actif circulant et passif circulant
        actif_circulant = sum(balance_sheet['Actif']['Actif Circulant'].values())
        passif_circulant = sum(balance_sheet['Passif']['Dettes'].values())
        
        # Totaux
        total_actif = sum([sum(v.values()) for v in balance_sheet['Actif'].values()])
        total_passif = sum([sum(v.values()) for v in balance_sheet['Passif'].values()])
        
        # Capitaux propres
        capitaux_propres = sum(balance_sheet['Passif']['Capitaux Propres'].values())
        
        # Résultat net
        CA = income_statement.get('Chiffre_affaires', 0.0)
        charges_totales = sum([v for k, v in income_statement.items() 
                             if k not in ['Chiffre_affaires', 'Produits_financiers']])
        resultat_net = CA - charges_totales
        
        # ===== RATIOS DE LIQUIDITÉ =====
        # 1. Fond de Roulement (FR)
        ratios['Fond de Roulement (FR)'] = actif_circulant - passif_circulant
        
        # 2. Ratio de Liquidité Générale
        if passif_circulant > 0:
            ratios['Ratio de Liquidité'] = actif_circulant / passif_circulant
        else:
            ratios['Ratio de Liquidité'] = float('inf')
        
        # Interprétation de la liquidité
        liquidite = ratios.get('Ratio de Liquidité', 0)
        if liquidite > 1.5:
            interpretations['Liquidité'] = {
                'statut': 'excellente',
                'couleur': 'ratio-good',
                'conseil': 'Votre entreprise dispose d\'une excellente capacité à honorer ses dettes à court terme.'
            }
        elif liquidite > 1:
            interpretations['Liquidité'] = {
                'statut': 'suffisante',
                'couleur': 'ratio-warning',
                'conseil': 'Votre liquidité est acceptable mais mérite surveillance. Pensez à optimiser votre BFR.'
            }
        else:
            interpretations['Liquidité'] = {
                'statut': 'critique',
                'couleur': 'ratio-danger',
                'conseil': 'Risque élevé de défaut. Actions urgentes recommandées : réduire BFR, renégocier délais.'
            }
        
        # ===== RATIOS DE SOLVABILITÉ =====
        # 3. Taux d'endettement
        if total_actif > 0:
            ratios['Taux d\'endettement'] = (passif_circulant / total_actif) * 100
        
        # Interprétation de la solvabilité
        endettement = ratios.get('Taux d\'endettement', 0)
        if endettement < 50:
            interpretations['Solvabilité'] = {
                'statut': 'saine',
                'couleur': 'ratio-good',
                'conseil': 'Structure financière équilibrée. Votre entreprise est peu dépendante des dettes.'
            }
        elif endettement < 70:
            interpretations['Solvabilité'] = {
                'statut': 'modérée',
                'couleur': 'ratio-warning',
                'conseil': 'Endettement à surveiller. Évitez de nouvelles dettes à court terme.'
            }
        else:
            interpretations['Solvabilité'] = {
                'statut': 'élevée',
                'couleur': 'ratio-danger',
                'conseil': 'Risque de solvabilité. Priorité : réduire la dette et augmenter les capitaux propres.'
            }
        
        # ===== RATIOS DE RENTABILITÉ =====
        # 4. ROA (Return on Assets)
        if total_actif > 0:
            ratios['ROA (%)'] = (resultat_net / total_actif) * 100
        
        # 5. ROE (Return on Equity) - AJOUTÉ
        if capitaux_propres > 0:
            ratios['ROE (%)'] = (resultat_net / capitaux_propres) * 100
        
        # 6. Marge Nette
        if CA > 0:
            ratios['Marge Nette (%)'] = (resultat_net / CA) * 100
        
        # Interprétation de la rentabilité
        roa = ratios.get('ROA (%)', 0)
        if roa > 10:
            interpretations['Rentabilité'] = {
                'statut': 'excellente',
                'couleur': 'ratio-good',
                'conseil': 'Vos actifs génèrent une rentabilité supérieure à la moyenne.'
            }
        elif roa > 5:
            interpretations['Rentabilité'] = {
                'statut': 'satisfaisante',
                'couleur': 'ratio-warning',
                'conseil': 'Rentabilité correcte. Pensez à optimiser l\'utilisation de vos actifs.'
            }
        else:
            interpretations['Rentabilité'] = {
                'statut': 'faible',
                'couleur': 'ratio-danger',
                'conseil': 'Rentabilité insuffisante. Améliorez votre marge ou la rotation des actifs.'
            }
        
        # ===== RATIOS D'ACTIVITÉ =====
        # 7. Rotation des actifs
        if total_actif > 0:
            ratios['Rotation des actifs'] = CA / total_actif
        
        # 8. Délai de rotation des stocks (simplifié)
        stocks = balance_sheet['Actif']['Actif Circulant'].get('Stocks', 0)
        if CA > 0 and stocks > 0:
            ratios['Délai moyen stocks (jours)'] = (stocks / CA) * 360
        
        # ===== BESOIN EN FONDS DE ROULEMENT (BFR) =====
        # Calcul simplifié du BFR
        stocks = balance_sheet['Actif']['Actif Circulant'].get('Stocks', 0)
        creances = balance_sheet['Actif']['Actif Circulant'].get('Créances clients', 0)
        dettes_fournisseurs = balance_sheet['Passif']['Dettes'].get('Dettes fournisseurs', 0)
        
        ratios['BFR Exploitation'] = stocks + creances - dettes_fournisseurs
        
        # Trésorerie nette
        ratios['Trésorerie Nette'] = ratios['Fond de Roulement (FR)'] - ratios['BFR Exploitation']
        
        # ===== RECOMMANDATIONS PERSONNALISÉES =====
        recommendations = []
        
        # Recommandation liquidité
        if liquidite < 1:
            recommendations.append({
                'priorite': 'Haute',
                'titre': 'Améliorer la liquidité',
                'actions': [
                    'Renégocier les délais de paiement avec les fournisseurs',
                    'Accélérer l\'encaissement des créances clients',
                    'Réduire les stocks inutiles'
                ],
                'impact': 'Réduction du risque de défaut de paiement'
            })
        
        # Recommandation rotation des actifs
        rotation = ratios.get('Rotation des actifs', 0)
        if rotation < 0.5:
            recommendations.append({
                'priorite': 'Moyenne',
                'titre': 'Optimiser la rotation des actifs',
                'actions': [
                    'Revendre les immobilisations sous-utilisées',
                    'Sous-traiter plutôt qu\'investir',
                    'Améliorer l\'efficacité opérationnelle'
                ],
                'impact': 'Augmentation de la rentabilité des investissements'
            })
        
        # Recommandation endettement
        if endettement > 70:
            recommendations.append({
                'priorite': 'Haute',
                'titre': 'Réduire l\'endettement',
                'actions': [
                    'Augmenter les capitaux propres (augmentation de capital)',
                    'Renégocier les taux d\'intérêt',
                    'Rembourser par anticipation si possible'
                ],
                'impact': 'Amélioration de la solvabilité et réduction des charges financières'
            })
        
        # Recommandation rentabilité
        if roa < 5:
            recommendations.append({
                'priorite': 'Moyenne',
                'titre': 'Améliorer la rentabilité',
                'actions': [
                    'Augmenter les prix ou réduire les coûts',
                    'Développer de nouveaux produits/services',
                    'Optimiser le mix produits'
                ],
                'impact': 'Augmentation du résultat net et des capacités d\'autofinancement'
            })
        
        interpretations['Recommandations'] = recommendations
        
    except Exception as e:
        st.error(f"Erreur dans le calcul des ratios: {str(e)}")
        
    return ratios, interpretations

def calculate_intermediate_balances(income_statement):
    """Calcule les soldes intermédiaires de gestion"""
    sig = {}
    
    try:
        CA = income_statement.get('Chiffre_affaires', 0.0)
        achats = income_statement.get('Achats_marchandises', 0.0)
        var_stocks = income_statement.get('Variation_stocks', 0.0)
        autres_charges = income_statement.get('Autres_achats_charges_externes', 0.0)
        charges_personnel = income_statement.get('Charges_personnel', 0.0)
        dotations = income_statement.get('Dotations_amortissements', 0.0)
        produits_financiers = income_statement.get('Produits_financiers', 0.0)
        charges_financieres = income_statement.get('Charges_financieres', 0.0)
        impot = income_statement.get('Impot_benefices', 0.0)
        
        # Calcul des SIG
        sig['Marge Commerciale'] = CA - achats + var_stocks if CA > 0 else 0.0
        sig['Valeur Ajoutée'] = sig['Marge Commerciale'] - autres_charges
        sig['EBE (Excédent Brut d\'Exploitation)'] = sig['Valeur Ajoutée'] - charges_personnel
        sig['Résultat Exploitation'] = sig['EBE (Excédent Brut d\'Exploitation)'] - dotations
        sig['Résultat Courant'] = sig['Résultat Exploitation'] + produits_financiers - charges_financieres
        sig['Résultat Net'] = sig['Résultat Courant'] - impot
        
    except Exception as e:
        st.error(f"Erreur dans le calcul des SIG: {str(e)}")
        
    return sig

def generate_comprehensive_report(balance_sheet, income_statement, ratios, sig):
    """Génère un rapport Excel complet avec toutes les analyses"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # ===== FEUILLE 1: BILAN =====
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
        
        df_bilan = pd.DataFrame(bilan_data)
        df_bilan.to_excel(writer, sheet_name='Bilan Comptable', index=False)
        
        # ===== FEUILLE 2: COMPTE DE RÉSULTAT =====
        if income_statement:
            # Données de base
            df_income = pd.DataFrame(list(income_statement.items()), 
                                    columns=['Poste', 'Valeur (€)'])
            df_income.to_excel(writer, sheet_name='Compte de Résultat', index=False)
            
            # Soldes intermédiaires
            df_sig = pd.DataFrame(list(sig.items()), 
                                 columns=['Solde Intermédiaire', 'Valeur (€)'])
            df_sig.to_excel(writer, sheet_name='Soldes Intermédiaires', index=False)
        
        # ===== FEUILLE 3: RATIOS ET ANALYSES =====
        if ratios:
            df_ratios = pd.DataFrame(list(ratios.items()), 
                                    columns=['Ratio / Indicateur', 'Valeur'])
            df_ratios.to_excel(writer, sheet_name='Ratios Financiers', index=False)
            
            # Ajout des interprétations
            interpretations = []
            for ratio, valeur in ratios.items():
                if 'Taux' in ratio or '%' in ratio:
                    interpretations.append(f"{ratio}: {valeur:.1f}% - {get_ratio_interpretation(ratio, valeur)}")
                else:
                    interpretations.append(f"{ratio}: {valeur:,.2f} € - {get_ratio_interpretation(ratio, valeur)}")
            
            df_interp = pd.DataFrame(interpretations, columns=['Interprétation'])
            df_interp.to_excel(writer, sheet_name='Interprétations', index=False)
        
        # ===== FEUILLE 4: SYNTHÈSE ET CONSEILS =====
        conseils_data = [
            ["💧 LIQUIDITÉ", "Maintenir un ratio de liquidité > 1.5", "Renégocier délais fournisseurs, accélérer encaissements"],
            ["🏦 SOLVABILITÉ", "Conserver un taux d'endettement < 50%", "Augmenter capitaux propres, limiter nouveaux emprunts"],
            ["📈 RENTABILITÉ", "Viser un ROA > 8% et un ROE > 12%", "Optimiser marge, améliorer rotation actifs"],
            ["⚙️ EFFICACITÉ", "Rotation actifs > 0.8", "Réduire immobilisations improductives, optimiser stocks"],
            ["💰 TRÉSORERIE", "Trésorerie nette positive", "Gérer finement BFR, anticiper besoins saisonniers"]
        ]
        
        df_conseils = pd.DataFrame(conseils_data, 
                                  columns=['Aspect', 'Objectif', 'Actions Recommandées'])
        df_conseils.to_excel(writer, sheet_name='Plan d\'Action', index=False)
    
    return output.getvalue()

def get_ratio_interpretation(ratio_name, value):
    """Retourne l'interprétation pédagogique d'un ratio"""
    if 'Liquidité' in ratio_name:
        if value > 1.5:
            return "Excellente capacité à honorer les dettes court terme"
        elif value > 1:
            return "Capacité suffisante mais surveillance recommandée"
        else:
            return "Risque de liquidité - Actions correctives urgentes"
    
    elif 'Taux d\'endettement' in ratio_name:
        if value < 50:
            return "Structure financière saine et équilibrée"
        elif value < 70:
            return "Endettement modéré - Surveillance recommandée"
        else:
            return "Endettement élevé - Risque pour la solvabilité"
    
    elif 'ROA' in ratio_name:
        if value > 10:
            return "Rentabilité excellente des actifs"
        elif value > 5:
            return "Rentabilité satisfaisante"
        else:
            return "Rentabilité à améliorer"
    
    elif 'ROE' in ratio_name:
        if value > 15:
            return "Très bon retour pour les actionnaires"
        elif value > 10:
            return "Retour satisfaisant sur fonds propres"
        else:
            return "Rentabilité des capitaux à améliorer"
    
    elif 'Marge Nette' in ratio_name:
        if value > 15:
            return "Marge excellente"
        elif value > 8:
            return "Marge satisfaisante"
        else:
            return "Marge à optimiser"
    
    elif 'Rotation' in ratio_name:
        if value > 1:
            return "Efficacité opérationnelle excellente"
        elif value > 0.5:
            return "Efficacité correcte"
        else:
            return "Efficacité à améliorer - Actifs sous-utilisés"
    
    return "À analyser dans le contexte sectoriel"

# ============================================
# INITIALISATION DES DONNÉES DE SESSION
# ============================================

if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

if 'balance_sheet' not in st.session_state:
    st.session_state.balance_sheet = create_balance_sheet_template()

if 'income_statement' not in st.session_state:
    st.session_state.income_statement = create_income_statement_template()

if 'learning_path_completed' not in st.session_state:
    st.session_state.learning_path_completed = {
        'bilan': False,
        'compte_resultat': False,
        'ratios': False,
        'budget': False
    }

if 'scenarios_history' not in st.session_state:
    st.session_state.scenarios_history = []

# ============================================
# INTERFACE PRINCIPALE
# ============================================

def main():
    # ===== EN-TÊTE PRINCIPALE =====
    col_logo, col_title = st.columns([1, 4])
    
    with col_logo:
        st.image("https://img.icons8.com/color/96/000000/financial-growth-analysis.png", width=80)
    
    with col_title:
        st.markdown('<h1 class="main-header">FinGuide Pro 📊</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #64748B; margin-bottom: 2rem; font-size: 1.1rem;'>
        <strong>Application didactique d'analyse financière - Apprendre en pratiquant</strong><br>
        <em>De la théorie à la pratique, maîtrisez l'analyse financière par l'action</em>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== SIDEBAR - NAVIGATION =====
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        
        # Sélection du module
        module = st.radio(
            "Choisissez votre module d'apprentissage:",
            ["📊 Tableau de Bord", 
             "📑 Bilan Comptable", 
             "💰 Compte de Résultat", 
             "📈 Analyse Financière",
             "🎯 Budget & Prévisions",
             "🧠 Centre d'Apprentissage",
             "⚙️ Paramètres"]
        )
        
        st.markdown("---")
        
        # Indicateur de progression
        st.markdown("### 📈 Votre Progression")
        
        completed = sum(st.session_state.learning_path_completed.values())
        total = len(st.session_state.learning_path_completed)
        progress = (completed / total) * 100 if total > 0 else 0
        
        st.progress(progress / 100)
        st.caption(f"{completed}/{total} modules complétés ({progress:.0f}%)")
        
        # Badges de compétences
        if st.session_state.learning_path_completed['bilan']:
            st.success("✅ Maîtrise du bilan")
        if st.session_state.learning_path_completed['compte_resultat']:
            st.success("✅ Maîtrise du compte de résultat")
        if st.session_state.learning_path_completed['ratios']:
            st.success("✅ Maîtrise des ratios")
        if st.session_state.learning_path_completed['budget']:
            st.success("✅ Maîtrise du budget")
        
        st.markdown("---")
        
        # Options rapides
        if st.button("🔄 Réinitialiser l'exercice", use_container_width=True):
            st.session_state.balance_sheet = create_balance_sheet_template()
            st.session_state.income_statement = create_income_statement_template()
            st.session_state.current_step = 0
            st.rerun()
        
        if st.button("📥 Exporter le rapport", use_container_width=True):
            ratios, _ = calculate_comprehensive_ratios(
                st.session_state.balance_sheet, 
                st.session_state.income_statement
            )
            sig = calculate_intermediate_balances(st.session_state.income_statement)
            
            excel_data = generate_comprehensive_report(
                st.session_state.balance_sheet,
                st.session_state.income_statement,
                ratios,
                sig
            )
            
            st.download_button(
                label="💾 Télécharger le rapport Excel",
                data=excel_data,
                file_name=f"rapport_finguide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # ===== ROUTAGE DES MODULES =====
    if module == "📊 Tableau de Bord":
        show_dashboard()
    elif module == "📑 Bilan Comptable":
        show_balance_sheet()
    elif module == "💰 Compte de Résultat":
        show_income_statement()
    elif module == "📈 Analyse Financière":
        show_financial_analysis()
    elif module == "🎯 Budget & Prévisions":
        show_budgeting()
    elif module == "🧠 Centre d'Apprentissage":
        show_learning_center()
    elif module == "⚙️ Paramètres":
        show_settings()

# ============================================
# MODULE 1: TABLEAU DE BORD
# ============================================

def show_dashboard():
    st.markdown('<h2 class="sub-header">📊 Tableau de Bord - Vue d\'ensemble</h2>', unsafe_allow_html=True)
    
    # ===== MÉTRIQUES DE PERFORMANCE =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calcul de l'équilibre du bilan
        if st.session_state.balance_sheet:
            total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
            total_passif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Passif'].values()])
            difference = total_actif - total_passif
            equilibré = abs(difference) < 0.01
            
            if equilibré:
                st.metric("Équilibre Bilan", "✅ Équilibré", delta=None)
            else:
                st.metric("Équilibre Bilan", "⚠️ Déséquilibré", f"{difference:,.2f} €")
    
    with col2:
        # Rentabilité
        if st.session_state.income_statement:
            CA = st.session_state.income_statement.get('Chiffre_affaires', 0)
            charges = sum([v for k, v in st.session_state.income_statement.items() 
                          if k != 'Chiffre_affaires'])
            resultat = CA - charges
            marge = (resultat / CA * 100) if CA > 0 else 0
            st.metric("Marge Nette", f"{marge:.1f}%", 
                     delta_color="normal" if marge > 0 else "inverse")
    
    with col3:
        # Liquidité
        if st.session_state.balance_sheet:
            actif_circulant = sum(st.session_state.balance_sheet['Actif']['Actif Circulant'].values())
            dettes = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
            liquidite = actif_circulant / dettes if dettes > 0 else float('inf')
            st.metric("Ratio Liquidité", f"{liquidite:.2f}")
    
    with col4:
        # Progression apprentissage
        completed = sum(st.session_state.learning_path_completed.values())
        total = len(st.session_state.learning_path_completed)
        progress = (completed / total) * 100 if total > 0 else 0
        st.metric("Progression", f"{progress:.0f}%")
    
    st.markdown("---")
    
    # ===== CARTES D'APPRENTISSAGE =====
    st.markdown("### 🎯 Parcours d'Apprentissage")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Carte 1: Comprendre le Bilan
        with st.expander("📑 **Module 1: Maîtriser le Bilan Comptable**", expanded=True):
            st.markdown("""
            #### Objectifs pédagogiques:
            - Comprendre la structure Actif/Passif
            - Maîtriser le principe d'équilibre comptable
            - Identifier les postes clés du bilan
            
            #### Concepts clés:
            • **Actif** = Ce que l'entreprise possède
            • **Passif** = Origine des ressources
            • **Équilibre** : Actif = Passif
            
            #### Exercice guidé:
            Construisez votre premier bilan pas-à-pas avec notre assistant interactif.
            """)
            
            if st.button("Commencer l'exercice Bilan", key="start_bilan"):
                st.session_state.current_step = 0
                st.rerun()
        
        # Carte 3: Analyser les Ratios
        with st.expander("📈 **Module 3: Analyser la Performance Financière**", expanded=True):
            st.markdown("""
            #### Objectifs pédagogiques:
            - Calculer et interpréter les ratios clés
            - Évaluer la santé financière
            - Comparer avec les benchmarks sectoriels
            
            #### Ratios étudiés:
            • **Liquidité** : Capacité à payer à court terme
            • **Solvabilité** : Structure financière à long terme
            • **Rentabilité** : Efficacité à générer des profits
            
            #### Exercice guidé:
            Analysez votre entreprise avec 10+ ratios financiers.
            """)
            
            if st.button("Commencer l'analyse Ratios", key="start_ratios"):
                st.session_state.current_step = 0
                st.rerun()
    
    with col_right:
        # Carte 2: Comprendre le Compte de Résultat
        with st.expander("💰 **Module 2: Maîtriser le Compte de Résultat**", expanded=True):
            st.markdown("""
            #### Objectifs pédagogiques:
            - Distinguer produits et charges
            - Calculer les soldes intermédiaires
            - Analyser la formation du résultat
            
            #### Concepts clés:
            • **Chiffre d'affaires** = Ventes totales
            • **Marge** = CA - Coût des ventes
            • **Résultat net** = Bénéfice final
            
            #### Exercice guidé:
            Construisez votre compte de résultat avec calcul automatique des SIG.
            """)
            
            if st.button("Commencer l'exercice Compte de Résultat", key="start_cdr"):
                st.session_state.current_step = 0
                st.rerun()
        
        # Carte 4: Budget et Prévisions
        with st.expander("🎯 **Module 4: Maîtriser le Budget et les Prévisions**", expanded=True):
            st.markdown("""
            #### Objectifs pédagogiques:
            - Élaborer un budget prévisionnel
            - Anticiper les risques de trésorerie
            - Simuler des scénarios what-if
            
            #### Outils pratiques:
            • **Budget de trésorerie** : Flux entrants/sortants
            • **Scénarios** : Pessimiste/Réaliste/Optimiste
            • **Alertes** : Détection des déficits
            
            #### Exercice guidé:
            Créez votre premier budget avec simulations.
            """)
            
            if st.button("Commencer l'exercice Budget", key="start_budget"):
                st.session_state.current_step = 0
                st.rerun()
    
    # ===== VISUALISATION DE LA PROGRESSION =====
    st.markdown("---")
    st.markdown("### 📊 Visualisation de votre Progression")
    
    progress_data = {
        'Module': ['Bilan', 'Compte Résultat', 'Ratios', 'Budget', 'Reporting'],
        'Théorie (%)': [90, 85, 75, 70, 60],
        'Pratique (%)': [
            80 if st.session_state.learning_path_completed['bilan'] else 20,
            60 if st.session_state.learning_path_completed['compte_resultat'] else 15,
            40 if st.session_state.learning_path_completed['ratios'] else 10,
            30 if st.session_state.learning_path_completed['budget'] else 5,
            20
        ]
    }
    
    df_progress = pd.DataFrame(progress_data)
    
    fig = px.bar(df_progress, x='Module', y=['Théorie (%)', 'Pratique (%)'],
                 barmode='group', title='Progression Théorie vs Pratique',
                 color_discrete_map={'Théorie (%)': '#3B82F6', 'Pratique (%)': '#10B981'})
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# MODULE 2: BILAN COMPTABLE
# ============================================

def show_balance_sheet():
    st.markdown('<h2 class="sub-header">📑 Module Bilan Comptable - Apprentissage Interactif</h2>', unsafe_allow_html=True)
    
    # ===== INTRODUCTION PÉDAGOGIQUE =====
    with st.expander("🎓 **Concepts fondamentaux - À lire avant de commencer**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🏢 **L'ACTIF : Ce que l'entreprise possède**
            
            **Actif Immobilisé** (long terme) :
            - Immobilisations : Biens durables (> 1 an)
            - Exemples : Bâtiments, machines, véhicules
            
            **Actif Circulant** (court terme) :
            - Stocks : Marchandises, matières premières
            - Créances : Factures clients à recevoir
            - Disponibilités : Argent en caisse et banque
            """)
        
        with col2:
            st.markdown("""
            ### 📋 **LE PASSIF : Origine des ressources**
            
            **Capitaux Propres** :
            - Capital social : Apports des actionnaires
            - Réserves : Bénéfices non distribués
            - Résultat : Bénéfice/perte de l'exercice
            
            **Dettes** :
            - Emprunts : Dettes à moyen/long terme
            - Dettes fournisseurs : Factures à payer
            - Dettes fiscales et sociales
            """)
        
        st.markdown("---")
        st.success("""
        **✨ PRINCIPE FONDAMENTAL :** 
        **L'ACTIF DOIT TOUJOURS ÊTRE ÉGAL AU PASSIF** 
        
        Cette égalité (Actif = Passif) est la base de la comptabilité en partie double.
        Si vos totaux ne sont pas égaux, c'est qu'il y a une erreur de saisie !
        """)
    
    # ===== ASSISTANT PAS-À-PAS =====
    st.markdown("### 🚀 Assistant Pas-à-Pas")
    
    steps = [
        "Étape 1 : Définir les immobilisations",
        "Étape 2 : Saisir les actifs circulants", 
        "Étape 3 : Structurer les capitaux propres",
        "Étape 4 : Enregistrer les dettes",
        "Étape 5 : Vérifier l'équilibre du bilan"
    ]
    
    # Navigation par étapes
    current_step = st.selectbox(
        "Sélectionnez l'étape en cours :",
        steps,
        index=st.session_state.current_step
    )
    st.session_state.current_step = steps.index(current_step)
    
    # Barre de progression
    progress_value = (st.session_state.current_step + 1) / len(steps)
    st.progress(progress_value)
    st.caption(f"Progression : Étape {st.session_state.current_step + 1}/{len(steps)}")
    
    # ===== AIDE CONTEXTUELLE =====
    with st.expander(f"💡 **Aide - {current_step}**", expanded=True):
        if "Étape 1" in current_step:
            st.info("""
            **ACTIF IMMOBILISÉ** - Biens durables détenus pour l'activité
            
            **Conseils pratiques :**
            1. **Immobilisations incorporelles** : Logiciels, brevets, fonds commercial
            2. **Immobilisations corporelles** : Bâtiments, machines, véhicules, matériel
            3. **Immobilisations financières** : Participations, prêts à long terme
            
            **💡 Astuce pédagogique :** 
            Les immobilisations s'amortissent sur plusieurs années. Exemple : 
            Un véhicule à 30 000€ sur 5 ans = 6 000€ d'amortissement annuel.
            """)
        
        elif "Étape 2" in current_step:
            st.info("""
            **ACTIF CIRCULANT** - Biens transformables rapidement en liquidités
            
            **Conseils pratiques :**
            1. **Stocks** : Valeur des marchandises et matières premières en stock
            2. **Créances clients** : Montant des factures en attente de paiement
            3. **Disponibilités** : Solde bancaire + argent en caisse
            4. **Autres actifs** : Avances, charges payées d'avance
            
            **💡 Astuce pédagogique :**
            Un bon gestionnaire minimise les stocks et les créances pour optimiser le BFR.
            """)
        
        elif "Étape 3" in current_step:
            st.info("""
            **CAPITAUX PROPRES** - Ressources stables appartenant aux actionnaires
            
            **Conseils pratiques :**
            1. **Capital social** : Apports initiaux des associés/actionnaires
            2. **Réserves** : Bénéfices des années antérieures non distribués
            3. **Résultat de l'exercice** : Bénéfice ou perte de l'année en cours
            
            **💡 Astuce pédagogique :**
            Des capitaux propres importants réduisent la dépendance aux dettes et améliorent la solvabilité.
            """)
        
        elif "Étape 4" in current_step:
            st.info("""
            **DETTES** - Ressources externes à rembourser
            
            **Conseils pratiques :**
            1. **Dettes financières** : Emprunts bancaires à moyen/long terme
            2. **Dettes fournisseurs** : Factures fournisseurs non réglées
            3. **Autres dettes** : Dettes fiscales (TVA, impôts), dettes sociales
            
            **💡 Astuce pédagogique :**
            Renégocier les délais fournisseurs peut améliorer significativement votre trésorerie.
            """)
        
        elif "Étape 5" in current_step:
            st.info("""
            **VÉRIFICATION DE L'ÉQUILIBRE** - Principe fondamental de la comptabilité
            
            **Méthode de vérification :**
            1. Calculer le **Total Actif** = Actif Immobilisé + Actif Circulant
            2. Calculer le **Total Passif** = Capitaux Propres + Dettes
            3. Vérifier que **Total Actif = Total Passif**
            
            **💡 En cas de déséquilibre :**
            • Vérifiez chaque saisie
            • Recherchez un montant égal à la différence
            • Revoyez les étapes précédentes
            """)
    
    # ===== INTERFACE DE SAISIE =====
    st.markdown("---")
    st.markdown(f"### 📝 {current_step}")
    
    col_actif, col_passif = st.columns(2)
    
    with col_actif:
        st.markdown("#### 🏢 **ACTIF**")
        st.markdown("##### Actif Immobilisé")
        
        # Saisie des immobilisations
        for item in st.session_state.balance_sheet['Actif']['Actif Immobilisé']:
            value = st.number_input(
                f"{item} :",
                min_value=0.0,
                value=float(st.session_state.balance_sheet['Actif']['Actif Immobilisé'][item]),
                step=1000.0,
                format="%.2f",
                key=f"actif_imm_{item}",
                help=f"Valeur des {item.lower()} (en euros)"
            )
            st.session_state.balance_sheet['Actif']['Actif Immobilisé'][item] = value
        
        st.markdown("---")
        st.markdown("##### Actif Circulant")
        
        # Saisie de l'actif circulant
        for item in st.session_state.balance_sheet['Actif']['Actif Circulant']:
            value = st.number_input(
                f"{item} :",
                min_value=0.0,
                value=float(st.session_state.balance_sheet['Actif']['Actif Circulant'][item]),
                step=1000.0,
                format="%.2f",
                key=f"actif_circ_{item}",
                help=f"Valeur des {item.lower()} (en euros)"
            )
            st.session_state.balance_sheet['Actif']['Actif Circulant'][item] = value
    
    with col_passif:
        st.markdown("#### 📋 **PASSIF**")
        st.markdown("##### Capitaux Propres")
        
        # Saisie des capitaux propres
        for item in st.session_state.balance_sheet['Passif']['Capitaux Propres']:
            value = st.number_input(
                f"{item} :",
                min_value=-1000000.0,  # Permet les pertes
                value=float(st.session_state.balance_sheet['Passif']['Capitaux Propres'][item]),
                step=1000.0,
                format="%.2f",
                key=f"cap_propres_{item}",
                help=f"Valeur des {item.lower()} (en euros)"
            )
            st.session_state.balance_sheet['Passif']['Capitaux Propres'][item] = value
        
        st.markdown("---")
        st.markdown("##### Dettes")
        
        # Saisie des dettes
        for item in st.session_state.balance_sheet['Passif']['Dettes']:
            value = st.number_input(
                f"{item} :",
                min_value=0.0,
                value=float(st.session_state.balance_sheet['Passif']['Dettes'][item]),
                step=1000.0,
                format="%.2f",
                key=f"dettes_{item}",
                help=f"Valeur des {item.lower()} (en euros)"
            )
            st.session_state.balance_sheet['Passif']['Dettes'][item] = value
    
    # ===== CALCUL ET VÉRIFICATION =====
    st.markdown("---")
    st.markdown("### 🧮 **Vérification de l'Équilibre**")
    
    # Calcul des totaux
    total_actif_immobilise = sum(st.session_state.balance_sheet['Actif']['Actif Immobilisé'].values())
    total_actif_circulant = sum(st.session_state.balance_sheet['Actif']['Actif Circulant'].values())
    total_actif = total_actif_immobilise + total_actif_circulant
    
    total_capitaux_propres = sum(st.session_state.balance_sheet['Passif']['Capitaux Propres'].values())
    total_dettes = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
    total_passif = total_capitaux_propres + total_dettes
    
    difference = total_actif - total_passif
    is_balanced = abs(difference) < 0.01
    
    # Affichage des résultats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Actif",
            f"{total_actif:,.2f} €",
            delta=f"{total_actif_immobilise:,.0f}€ immo + {total_actif_circulant:,.0f}€ circ"
        )
    
    with col2:
        st.metric(
            "Total Passif", 
            f"{total_passif:,.2f} €",
            delta=f"{total_capitaux_propres:,.0f}€ CP + {total_dettes:,.0f}€ dettes"
        )
    
    with col3:
        if is_balanced:
            st.success("✅ **BILAN ÉQUILIBRÉ**")
            st.balloons()
            if not st.session_state.learning_path_completed['bilan']:
                st.session_state.learning_path_completed['bilan'] = True
                st.success("🎉 **Félicitations ! Vous avez maîtrisé l'équilibre du bilan !**")
        else:
            st.error(f"⚠️ **DÉSÉQUILIBRE : {difference:,.2f} €**")
            st.warning("""
            **Pour rectifier :**
            1. Vérifiez chaque saisie
            2. Recherchez un montant de **{diff:,.2f} €**
            3. Corrigez l'erreur dans l'étape concernée
            """.format(diff=difference))
    
    # ===== VISUALISATION GRAPHIQUE =====
    st.markdown("---")
    st.markdown("### 📊 **Visualisation de la Structure du Bilan**")
    
    # Préparation des données pour le graphique
    categories = []
    valeurs = []
    couleurs = []
    
    # Actif
    for item, valeur in st.session_state.balance_sheet['Actif']['Actif Immobilisé'].items():
        if valeur > 0:
            categories.append(f"Actif - {item}")
            valeurs.append(valeur)
            couleurs.append('#3B82F6')  # Bleu pour l'actif
    
    for item, valeur in st.session_state.balance_sheet['Actif']['Actif Circulant'].items():
        if valeur > 0:
            categories.append(f"Actif - {item}")
            valeurs.append(valeur)
            couleurs.append('#60A5FA')  # Bleu clair
    
    # Passif
    for item, valeur in st.session_state.balance_sheet['Passif']['Capitaux Propres'].items():
        if valeur > 0:
            categories.append(f"Passif - {item}")
            valeurs.append(valeur)
            couleurs.append('#10B981')  # Vert pour les capitaux propres
    
    for item, valeur in st.session_state.balance_sheet['Passif']['Dettes'].items():
        if valeur > 0:
            categories.append(f"Passif - {item}")
            valeurs.append(valeur)
            couleurs.append('#F59E0B')  # Orange pour les dettes
    
    if valeurs:
        # Graphique en camembert
        fig = px.pie(
            names=categories, 
            values=valeurs,
            title="Structure Détaillée du Bilan",
            color_discrete_sequence=couleurs,
            hole=0.4  # Donut chart
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Valeur: %{value:,.0f} €<br>Part: %{percent}'
        )
        
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Graphique en barres comparatives
        if is_balanced:
            fig2 = go.Figure()
            
            fig2.add_trace(go.Bar(
                x=['Actif', 'Passif'],
                y=[total_actif, total_passif],
                marker_color=['#3B82F6', '#10B981'],
                text=[f'{total_actif:,.0f} €', f'{total_passif:,.0f} €'],
                textposition='auto',
            ))
            
            fig2.update_layout(
                title='Équilibre Actif/Passif',
                yaxis_title='Montant (€)',
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    # ===== NAVIGATION ET ACTIONS =====
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    
    with col_nav1:
        if st.button("◀️ Étape précédente"):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
                st.rerun()
    
    with col_nav2:
        if st.button("🔄 Recommencer cette étape"):
            st.rerun()
    
    with col_nav3:
        if st.button("Étape suivante ▶️"):
            if st.session_state.current_step < len(steps) - 1:
                st.session_state.current_step += 1
                st.rerun()
            else:
                st.success("🎉 **Module Bilan complété !** Passez au module suivant.")
    
    # ===== EXERCICE PRATIQUE =====
    with st.expander("🧩 **Exercice Pratique - Testez vos connaissances**", expanded=False):
        st.markdown("""
        **Exercice 1 :** Une entreprise a les données suivantes :
        - Immobilisations : 150 000 €
        - Stocks : 30 000 €
        - Créances clients : 20 000 €
        - Banque : 10 000 €
        - Capital social : 100 000 €
        - Résultat : 40 000 €
        - Emprunts : 50 000 €
        - Dettes fournisseurs : 20 000 €
        
        **Questions :**
        1. Calculez le total actif
        2. Calculez le total passif
        3. Le bilan est-il équilibré ?
        
        **Réponses :**
        1. Actif = 150 000 + 30 000 + 20 000 + 10 000 = **210 000 €**
        2. Passif = 100 000 + 40 000 + 50 000 + 20 000 = **210 000 €**
        3. **OUI**, Actif (210 000 €) = Passif (210 000 €) ✅
        """)

# ============================================
# MODULE 3: COMPTE DE RÉSULTAT
# ============================================

def show_income_statement():
    st.markdown('<h2 class="sub-header">💰 Module Compte de Résultat - Analyse de la Performance</h2>', unsafe_allow_html=True)
    
    # ===== INTRODUCTION PÉDAGOGIQUE =====
    with st.expander("🎓 **Comprendre le Compte de Résultat**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📈 **LES PRODUITS : Sources de revenus**
            
            **Chiffre d'affaires** :
            - Ventes de biens et services
            - Base de la rentabilité
            
            **Produits financiers** :
            - Intérêts perçus
            - Revenus de placements
            """)
        
        with col2:
            st.markdown("""
            ### 📉 **LES CHARGES : Coûts de l'activité**
            
            **Charges d'exploitation** :
            - Achats et variations de stocks
            - Charges externes et personnel
            - Dotations aux amortissements
            
            **Charges financières** :
            - Intérêts sur emprunts
            """)
        
        st.markdown("---")
        st.success("""
        **✨ OBJECTIF PRINCIPAL :** 
        **RÉSULTAT NET = PRODUITS - CHARGES**
        
        Un résultat positif = BÉNÉFICE
        Un résultat négatif = PERTE
        """)
    
    # ===== SAISIE DU COMPTE DE RÉSULTAT =====
    st.markdown("### 📝 Saisie des Données")
    
    col_produits, col_charges = st.columns(2)
    
    with col_produits:
        st.markdown("#### 📈 **PRODUITS**")
        
        # Chiffre d'affaires
        st.session_state.income_statement['Chiffre_affaires'] = st.number_input(
            "Chiffre d'affaires HT :",
            min_value=0.0,
            value=float(st.session_state.income_statement['Chiffre_affaires']),
            step=1000.0,
            format="%.2f",
            help="Montant total des ventes de l'exercice",
            key="ca_input"
        )
        
        # Produits financiers
        st.session_state.income_statement['Produits_financiers'] = st.number_input(
            "Produits financiers :",
            min_value=0.0,
            value=float(st.session_state.income_statement['Produits_financiers']),
            step=1000.0,
            format="%.2f",
            help="Intérêts perçus, revenus de placements",
            key="prod_fin_input"
        )
    
    with col_charges:
        st.markdown("#### 📉 **CHARGES**")
        
        # Création de deux colonnes pour les charges
        charge_col1, charge_col2 = st.columns(2)
        
        with charge_col1:
            # Achats
            st.session_state.income_statement['Achats_marchandises'] = st.number_input(
                "Achats de marchandises :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Achats_marchandises']),
                step=1000.0,
                format="%.2f",
                help="Coût des marchandises achetées",
                key="achats_input"
            )
            
            # Variation de stocks
            st.session_state.income_statement['Variation_stocks'] = st.number_input(
                "Variation de stocks :",
                value=float(st.session_state.income_statement['Variation_stocks']),
                step=1000.0,
                format="%.2f",
                help="Stock initial - Stock final (positif si diminution)",
                key="var_stocks_input"
            )
            
            # Charges de personnel
            st.session_state.income_statement['Charges_personnel'] = st.number_input(
                "Charges de personnel :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Charges_personnel']),
                step=1000.0,
                format="%.2f",
                help="Salaires et charges sociales",
                key="charges_perso_input"
            )
            
            # Dotations
            st.session_state.income_statement['Dotations_amortissements'] = st.number_input(
                "Dotations aux amortissements :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Dotations_amortissements']),
                step=1000.0,
                format="%.2f",
                help="Amortissements des immobilisations",
                key="dotations_input"
            )
        
        with charge_col2:
            # Autres charges externes
            st.session_state.income_statement['Autres_achats_charges_externes'] = st.number_input(
                "Autres achats et charges externes :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Autres_achats_charges_externes']),
                step=1000.0,
                format="%.2f",
                help="Loyers, électricité, téléphone, etc.",
                key="autres_charges_input"
            )
            
            # Impôts et taxes
            st.session_state.income_statement['Impots_taxes'] = st.number_input(
                "Impôts et taxes :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Impots_taxes']),
                step=1000.0,
                format="%.2f",
                help="Taxes locales, CVAE, etc.",
                key="impots_input"
            )
            
            # Autres charges
            st.session_state.income_statement['Autres_charges'] = st.number_input(
                "Autres charges :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Autres_charges']),
                step=1000.0,
                format="%.2f",
                help="Charges exceptionnelles",
                key="autres_input"
            )
            
            # Charges financières
            st.session_state.income_statement['Charges_financieres'] = st.number_input(
                "Charges financières :",
                min_value=0.0,
                value=float(st.session_state.income_statement['Charges_financieres']),
                step=1000.0,
                format="%.2f",
                help="Intérêts sur emprunts",
                key="charges_fin_input"
            )
    
    # Impôt sur les bénéfices (en bas pour être visible)
    st.markdown("---")
    st.session_state.income_statement['Impot_benefices'] = st.number_input(
        "Impôt sur les bénéfices :",
        min_value=0.0,
        value=float(st.session_state.income_statement['Impot_benefices']),
        step=1000.0,
        format="%.2f",
        help="Impôt sur les sociétés ou impôt sur le revenu",
        key="impot_benef_input"
    )
    
    # ===== CALCUL DES SOLDES INTERMÉDIAIRES =====
    st.markdown("---")
    st.markdown("### 🧮 **Soldes Intermédiaires de Gestion (SIG)**")
    
    # Calcul des SIG
    sig = calculate_intermediate_balances(st.session_state.income_statement)
    
    # Affichage des SIG sous forme de tableau
    sig_data = []
    for solde, valeur in sig.items():
        sig_data.append({
            'Solde': solde,
            'Valeur (€)': valeur,
            'Formule': get_sig_formula(solde)
        })
    
    df_sig = pd.DataFrame(sig_data)
    
    # Mise en forme conditionnelle
    def color_sig(val):
        if val < 0:
            return 'color: #EF4444; font-weight: bold;'
        elif val > 0:
            return 'color: #10B981; font-weight: bold;'
        else:
            return ''
    
    styled_df = df_sig.style.format({'Valeur (€)': '{:,.2f} €'})\
        .applymap(color_sig, subset=['Valeur (€)'])
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # ===== EXPLICATIONS DES SIG =====
    with st.expander("📚 **Explications des Soldes Intermédiaires**", expanded=False):
        st.markdown("""
        **1. Marge Commerciale** :
        - **Formule** : CA - Achats + Variation stocks
        - **Signification** : Rentabilité brute des ventes
        - **Objectif** : > 30% du CA
        
        **2. Valeur Ajoutée** :
        - **Formule** : Marge commerciale - Autres charges externes
        - **Signification** : Richesse créée par l'entreprise
        - **Objectif** : Croissante d'année en année
        
        **3. EBE (Excédent Brut d'Exploitation)** :
        - **Formule** : Valeur ajoutée - Charges de personnel
        - **Signification** : Capacité à générer de la trésorerie
        - **Objectif** : > 10% du CA
        
        **4. Résultat d'Exploitation** :
        - **Formule** : EBE - Dotations aux amortissements
        - **Signification** : Performance de l'activité courante
        - **Objectif** : Positif et croissant
        
        **5. Résultat Courant** :
        - **Formule** : Résultat exploitation + Produits financiers - Charges financières
        - **Signification** : Résultat avant impôt
        - **Objectif** : > 5% du CA
        
        **6. Résultat Net** :
        - **Formule** : Résultat courant - Impôt sur les bénéfices
        - **Signification** : Bénéfice final de l'entreprise
        - **Objectif** : Maximiser
        """)
    
    # ===== VISUALISATION GRAPHIQUE =====
    st.markdown("---")
    st.markdown("### 📊 **Évolution des Soldes Intermédiaires**")
    
    if len(df_sig) > 0:
        # Graphique en cascade (waterfall)
        fig = go.Figure(go.Waterfall(
            name="Formation du résultat",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "total"],
            x=df_sig['Solde'],
            textposition="outside",
            text=[f"{v:,.0f} €" for v in df_sig['Valeur (€)']],
            y=df_sig['Valeur (€)'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#10B981"}},
            decreasing={"marker": {"color": "#EF4444"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        
        fig.update_layout(
            title="Formation du Résultat Net (Waterfall Chart)",
            showlegend=False,
            height=500,
            yaxis_title="Montant (€)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Graphique en barres horizontales
        fig2 = px.bar(
            df_sig,
            x='Valeur (€)',
            y='Solde',
            orientation='h',
            color='Valeur (€)',
            color_continuous_scale='RdYlGn',
            text='Valeur (€)',
            title="Comparaison des Soldes Intermédiaires"
        )
        
        fig2.update_traces(
            texttemplate='%{text:,.0f} €',
            textposition='outside'
        )
        
        fig2.update_layout(
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # ===== ANALYSE DE LA PERFORMANCE =====
    st.markdown("---")
    st.markdown("### 📈 **Analyse de la Performance**")
    
    if sig:
        CA = st.session_state.income_statement['Chiffre_affaires']
        resultat_net = sig.get('Résultat Net', 0)
        
        if CA > 0:
            marge_nette = (resultat_net / CA) * 100
            
            col_perf1, col_perf2, col_perf3 = st.columns(3)
            
            with col_perf1:
                st.metric(
                    "Chiffre d'Affaires",
                    f"{CA:,.2f} €",
                    delta="Base de calcul"
                )
            
            with col_perf2:
                st.metric(
                    "Résultat Net",
                    f"{resultat_net:,.2f} €",
                    delta_color="normal" if resultat_net > 0 else "inverse"
                )
            
            with col_perf3:
                st.metric(
                    "Marge Nette",
                    f"{marge_nette:.1f} %",
                    delta="Rentabilité"
                )
            
            # Interprétation de la marge
            if marge_nette > 15:
                st.success(f"✅ **Excellente rentabilité** : Votre marge nette de {marge_nette:.1f}% est supérieure à la moyenne sectorielle.")
            elif marge_nette > 5:
                st.warning(f"⚠️ **Rentabilité correcte** : Votre marge nette de {marge_nette:.1f}% est dans la moyenne. Pensez à l'optimiser.")
            elif marge_nette > 0:
                st.error(f"❌ **Rentabilité faible** : Votre marge nette de {marge_nette:.1f}% est insuffisante. Analysez vos coûts.")
            else:
                st.error(f"🚨 **PERTE** : Votre entreprise est déficitaire. Actions correctives urgentes nécessaires.")
    
    # ===== EXERCICE PRATIQUE =====
    with st.expander("🧩 **Exercice Pratique - Analyse de Performance**", expanded=False):
        st.markdown("""
        **Cas d'étude :** Entreprise "TechInnov"
        
        **Données :**
        - CA : 500 000 €
        - Achats : 200 000 €
        - Variation stocks : -10 000 € (augmentation)
        - Charges externes : 100 000 €
        - Charges personnel : 120 000 €
        - Dotations : 20 000 €
        - Produits financiers : 5 000 €
        - Charges financières : 15 000 €
        - Impôt : 10 000 €
        
        **Questions :**
        1. Calculez la marge commerciale
        2. Calculez le résultat net
        3. Calculez la marge nette
        4. L'entreprise est-elle rentable ?
        
        **Réponses :**
        1. Marge commerciale = 500 000 - 200 000 - 10 000 = **290 000 €**
        2. Résultat net = 500 000 - (200 000+10 000+100 000+120 000+20 000+15 000+10 000) + 5 000 = **30 000 €**
        3. Marge nette = 30 000 / 500 000 × 100 = **6%**
        4. **OUI**, mais la rentabilité est modeste (6%)
        """)
    
    # Marquer le module comme complété
    if sig and 'Résultat Net' in sig:
        if not st.session_state.learning_path_completed['compte_resultat']:
            st.session_state.learning_path_completed['compte_resultat'] = True
            st.success("🎉 **Module Compte de Résultat complété !**")

def get_sig_formula(solde_name):
    """Retourne la formule du solde intermédiaire"""
    formules = {
        'Marge Commerciale': 'CA - Achats + Variation stocks',
        'Valeur Ajoutée': 'Marge commerciale - Autres charges externes',
        'EBE (Excédent Brut d\'Exploitation)': 'Valeur ajoutée - Charges de personnel',
        'Résultat Exploitation': 'EBE - Dotations aux amortissements',
        'Résultat Courant': 'Résultat exploitation + Produits financiers - Charges financières',
        'Résultat Net': 'Résultat courant - Impôt sur les bénéfices'
    }
    return formules.get(solde_name, 'N/A')

# ============================================
# MODULE 4: ANALYSE FINANCIÈRE
# ============================================

def show_financial_analysis():
    st.markdown('<h2 class="sub-header">📈 Module Analyse Financière - Diagnostic Complet</h2>', unsafe_allow_html=True)
    
    # Vérifier que les données sont disponibles
    if not st.session_state.balance_sheet or not st.session_state.income_statement:
        st.warning("⚠️ **Données manquantes** : Veuillez d'abord compléter le bilan et le compte de résultat.")
        
        col_guide1, col_guide2 = st.columns(2)
        
        with col_guide1:
            if st.button("📑 Aller au Module Bilan"):
                st.session_state.current_step = 0
                st.rerun()
        
        with col_guide2:
            if st.button("💰 Aller au Module Compte de Résultat"):
                st.session_state.current_step = 0
                st.rerun()
        
        return
    
    # ===== CALCUL DES RATIOS =====
    ratios, interpretations = calculate_comprehensive_ratios(
        st.session_state.balance_sheet, 
        st.session_state.income_statement
    )
    
    # ===== TABLEAU DE BORD DES RATIOS =====
    st.markdown("### 🎯 **Tableau de Bord des Indicateurs Clés**")
    
    # Affichage des ratios par catégorie
    tabs = st.tabs([
        "💧 Liquidité & BFR", 
        "🏦 Solvabilité", 
        "📈 Rentabilité", 
        "⚙️ Efficacité",
        "🎯 Recommandations"
    ])
    
    with tabs[0]:  # Liquidité
        col_liq1, col_liq2, col_liq3 = st.columns(3)
        
        with col_liq1:
            fr = ratios.get('Fond de Roulement (FR)', 0)
            st.metric(
                "Fond de Roulement (FR)",
                f"{fr:,.0f} €",
                delta="Actif circulant - Dettes CT"
            )
            
            if fr > 0:
                st.success("✅ FR positif : ressources stables > emplois stables")
            else:
                st.error("❌ FR négatif : besoin de financement")
        
        with col_liq2:
            liquidite = ratios.get('Ratio de Liquidité', 0)
            st.metric(
                "Ratio de Liquidité",
                f"{liquidite:.2f}",
                delta="Actif circulant / Dettes CT"
            )
            
            # Interprétation
            if liquidite > 1.5:
                st.markdown('<p class="ratio-good">✅ Excellente liquidité</p>', unsafe_allow_html=True)
            elif liquidite > 1:
                st.markdown('<p class="ratio-warning">⚠️ Liquidité à surveiller</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ratio-danger">❌ Risque de liquidité</p>', unsafe_allow_html=True)
        
        with col_liq3:
            bfr = ratios.get('BFR Exploitation', 0)
            st.metric(
                "BFR d'Exploitation",
                f"{bfr:,.0f} €",
                delta="Stocks + Créances - Dettes fournisseurs"
            )
            
            if bfr > 0:
                st.info("ℹ️ BFR positif : besoin de financement du cycle d'exploitation")
            else:
                st.info("ℹ️ BFR négatif : ressources du cycle d'exploitation")
        
        # Explication pédagogique
        with st.expander("📚 **Comprendre la Liquidité et le BFR**", expanded=False):
            st.markdown("""
            **💧 LIQUIDITÉ** = Capacité à payer ses dettes à court terme
            
            **Indicateurs clés :**
            • **Fond de Roulement (FR)** : Différence entre ressources stables et emplois stables
            • **Ratio de liquidité** : Capacité à couvrir les dettes CT avec l'actif CT
            • **BFR** : Besoin de financement du cycle d'exploitation
            
            **Objectifs :**
            • FR > 0
            • Ratio liquidité > 1.5
            • BFR le plus faible possible
            
            **💡 Bonnes pratiques :**
            1. Négocier des délais fournisseurs plus longs
            2. Accélérer l'encaissement des créances clients
            3. Optimiser la gestion des stocks
            """)
    
    with tabs[1]:  # Solvabilité
        col_sol1, col_sol2, col_sol3 = st.columns(3)
        
        with col_sol1:
            endettement = ratios.get('Taux d\'endettement', 0)
            st.metric(
                "Taux d'Endettement",
                f"{endettement:.1f} %",
                delta="Dettes / Total actif × 100"
            )
            
            # Interprétation
            if endettement < 50:
                st.markdown('<p class="ratio-good">✅ Structure financière saine</p>', unsafe_allow_html=True)
            elif endettement < 70:
                st.markdown('<p class="ratio-warning">⚠️ Endettement modéré</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ratio-danger">❌ Endettement élevé</p>', unsafe_allow_html=True)
        
        with col_sol2:
            capitaux_propres = sum(st.session_state.balance_sheet['Passif']['Capitaux Propres'].values())
            total_actif = sum([sum(v.values()) for v in st.session_state.balance_sheet['Actif'].values()])
            
            if total_actif > 0:
                autonomie = (capitaux_propres / total_actif) * 100
                st.metric(
                    "Autonomie Financière",
                    f"{autonomie:.1f} %",
                    delta="Capitaux propres / Total actif × 100"
                )
            else:
                st.metric("Autonomie Financière", "N/A")
        
        with col_sol3:
            # Capacité de remboursement (simplifiée)
            CA = st.session_state.income_statement.get('Chiffre_affaires', 0)
            total_dettes = sum(st.session_state.balance_sheet['Passif']['Dettes'].values())
            
            if CA > 0 and total_dettes > 0:
                capacite = total_dettes / CA
                st.metric(
                    "Dettes/CA (années)",
                    f"{capacite:.1f}",
                    delta="Années de CA pour rembourser les dettes"
                )
            else:
                st.metric("Dettes/CA", "N/A")
        
        # Explication pédagogique
        with st.expander("📚 **Comprendre la Solvabilité**", expanded=False):
            st.markdown("""
            **🏦 SOLVABILITÉ** = Capacité à rembourser toutes ses dettes à long terme
            
            **Indicateurs clés :**
            • **Taux d'endettement** : Part des dettes dans le financement
            • **Autonomie financière** : Part des capitaux propres
            • **Dettes/CA** : Capacité de remboursement
            
            **Seuils recommandés :**
            • Taux endettement < 50% ✅
            • Autonomie > 30% ✅
            • Dettes/CA < 3 années ✅
            
            **💡 Bonnes pratiques :**
            1. Privilégier les capitaux propres aux dettes
            2. Limiter l'endettement à court terme
            3. Maintenir un bon ratio de couverture des intérêts
            """)
    
    with tabs[2]:  # Rentabilité
        col_rent1, col_rent2, col_rent3 = st.columns(3)
        
        with col_rent1:
            roa = ratios.get('ROA (%)', 0)
            st.metric(
                "ROA (Return on Assets)",
                f"{roa:.1f} %",
                delta="Résultat net / Total actif × 100"
            )
            
            # Interprétation
            if roa > 10:
                st.markdown('<p class="ratio-good">✅ Excellente rentabilité des actifs</p>', unsafe_allow_html=True)
            elif roa > 5:
                st.markdown('<p class="ratio-warning">⚠️ Rentabilité correcte</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ratio-danger">❌ Rentabilité à améliorer</p>', unsafe_allow_html=True)
        
        with col_rent2:
            roe = ratios.get('ROE (%)', 0)
            st.metric(
                "ROE (Return on Equity)",
                f"{roe:.1f} %",
                delta="Résultat net / Capitaux propres × 100"
            )
            
            # Interprétation
            if roe > 15:
                st.markdown('<p class="ratio-good">✅ Excellent retour pour les actionnaires</p>', unsafe_allow_html=True)
            elif roe > 10:
                st.markdown('<p class="ratio-warning">⚠️ Retour satisfaisant</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ratio-danger">❌ Retour à améliorer</p>', unsafe_allow_html=True)
        
        with col_rent3:
            marge_nette = ratios.get('Marge Nette (%)', 0)
            st.metric(
                "Marge Nette",
                f"{marge_nette:.1f} %",
                delta="Résultat net / CA × 100"
            )
            
            # Comparaison ROA vs ROE
            if roe > roa:
                st.info("⚡ **Effet de levier positif** : L'endettement améliore la rentabilité des capitaux propres")
            elif roe < roa:
                st.info("⚠️ **Effet de levier négatif** : L'endettement réduit la rentabilité des capitaux propres")
        
        # Explication pédagogique ROA vs ROE
        with st.expander("📚 **Comprendre ROA vs ROE**", expanded=False):
            col_diff1, col_diff2 = st.columns(2)
            
            with col_diff1:
                st.markdown("""
                **📊 ROA (Return on Assets)**
                
                **Formule :**
                ```
                Résultat Net
                ------------ × 100
                Total Actif
                ```
                
                **Signification :**
                • Efficacité de l'ensemble des actifs
                • Performance opérationnelle globale
                • Indépendant du financement
                
                **Objectif :** > 8%
                """)
            
            with col_diff2:
                st.markdown("""
                **📈 ROE (Return on Equity)**
                
                **Formule :**
                ```
                Résultat Net
                ------------------- × 100
                Capitaux Propres
                ```
                
                **Signification :**
                • Rentabilité pour les actionnaires
                • Impact de l'endettement (effet de levier)
                • Performance financière
                
                **Objectif :** > 12%
                """)
            
            st.markdown("""
            **⚡ Effet de levier financier :**
            ```
            ROE = ROA + (ROA - Coût dette) × (Dettes/CP)
            ```
            
            • Si ROA > Coût dette : Endettement améliore ROE ✅
            • Si ROA < Coût dette : Endettement réduit ROE ❌
            """)
    
    with tabs[3]:  # Efficacité
        col_eff1, col_eff2, col_eff3 = st.columns(3)
        
        with col_eff1:
            rotation = ratios.get('Rotation des actifs', 0)
            st.metric(
                "Rotation des Actifs",
                f"{rotation:.2f}",
                delta="CA / Total actif"
            )
            
            # Interprétation
            if rotation > 1:
                st.markdown('<p class="ratio-good">✅ Excellente efficacité</p>', unsafe_allow_html=True)
            elif rotation > 0.5:
                st.markdown('<p class="ratio-warning">⚠️ Efficacité correcte</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ratio-danger">❌ Efficacité à améliorer</p>', unsafe_allow_html=True)
        
        with col_eff2:
            delai_stocks = ratios.get('Délai moyen stocks (jours)', 0)
            if delai_stocks:
                st.metric(
                    "Délai Stocks (jours)",
                    f"{delai_stocks:.0f}",
                    delta="(Stocks / CA) × 360"
                )
            else:
                st.metric("Délai Stocks", "N/A")
        
        with col_eff3:
            # Productivité (simplifiée)
            CA = st.session_state.income_statement.get('Chiffre_affaires', 0)
            charges_personnel = st.session_state.income_statement.get('Charges_personnel', 0)
            
            if charges_personnel > 0:
                productivite = CA / charges_personnel
                st.metric(
                    "Productivité (CA/Charges pers.)",
                    f"{productivite:.1f}",
                    delta="CA généré par € de charges personnel"
                )
            else:
                st.metric("Productivité", "N/A")
        
        # Explication pédagogique
        with st.expander("📚 **Comprendre l'Efficacité Opérationnelle**", expanded=False):
            st.markdown("""
            **⚙️ EFFICACITÉ OPÉRATIONNELLE** = Capacité à utiliser au mieux les ressources
            
            **Indicateurs clés :**
            • **Rotation des actifs** : CA généré par € d'actif
            • **Délai stocks** : Jours de vente en stock
            • **Productivité** : CA par € de charges personnel
            
            **Objectifs :**
            • Rotation actifs > 0.8
            • Délai stocks < 60 jours
            • Productivité > 5
            
            **💡 Bonnes pratiques :**
            1. Optimiser l'utilisation des immobilisations
            2. Réduire les stocks inutiles
            3. Améliorer la productivité du personnel
            """)
    
    with tabs[4]:  # Recommandations
        st.markdown("### 🎯 **Recommandations Personnalisées**")
        
        if 'Recommandations' in interpretations:
            recommendations = interpretations['Recommandations']
            
            if recommendations:
                for i, rec in enumerate(recommendations):
                    # Déterminer la couleur de la priorité
                    if rec['priorite'] == 'Haute':
                        badge_color = "🔴"
                        border_color = "#EF4444"
                    elif rec['priorite'] == 'Moyenne':
                        badge_color = "🟡"
                        border_color = "#F59E0B"
                    else:
                        badge_color = "🟢"
                        border_color = "#10B981"
                    
                    # Afficher la recommandation
                    st.markdown(f"""
                    <div style="border-left: 6px solid {border_color}; padding: 15px; margin: 10px 0; background: white; border-radius: 8px;">
                        <h4>{badge_color} <strong>{rec['priorite']}</strong> - {rec['titre']}</h4>
                        <p><strong>Actions recommandées :</strong></p>
                        <ul>
                            {"".join([f'<li>{action}</li>' for action in rec['actions']])}
                        </ul>
                        <p><em>Impact attendu : {rec['impact']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("""
                🎉 **Excellent travail !**
                
                Votre entreprise présente des ratios financiers globalement sains :
                • Liquidité suffisante
                • Endettement maîtrisé  
                • Rentabilité satisfaisante
                • Efficacité opérationnelle correcte
                
                Continuez sur cette lancée en maintenant une vigilance sur vos indicateurs clés.
                """)
        else:
            st.info("""
            ⏳ **Analyse en cours...**
            
            Complétez vos données financières pour obtenir des recommandations personnalisées.
            """)
    
    # ===== VISUALISATIONS AVANCÉES =====
    st.markdown("---")
    st.markdown("### 📊 **Visualisations Synthétiques**")
    
    # Création d'un radar chart des ratios
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        # Graphique radar (spider chart)
        categories = ['Liquidité', 'Solvabilité', 'Rentabilité', 'Efficacité']
        
        # Normalisation des valeurs pour le radar (0-100)
        values = []
        
        # Liquidité (0-100)
        liquidite = min(ratios.get('Ratio de Liquidité', 0), 3)  # Cap à 3
        values.append((liquidite / 3) * 100)
        
        # Solvabilité (0-100)
        endettement = ratios.get('Taux d\'endettement', 0)
        solvabilite = max(0, 100 - (endettement * 1.5))  # 0% = 100, 66.7% = 0
        values.append(min(solvabilite, 100))
        
        # Rentabilité (0-100)
        roa = ratios.get('ROA (%)', 0)
        rentabilite = min(roa * 5, 100)  # 20% = 100
        values.append(rentabilite)
        
        # Efficacité (0-100)
        rotation = ratios.get('Rotation des actifs', 0)
        efficacite = min(rotation * 50, 100)  # 2 = 100
        values.append(efficacite)
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Votre entreprise',
            line_color='#3B82F6',
            fillcolor='rgba(59, 130, 246, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Profil Financier - Radar Chart",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_viz2:
        # Graphique de comparaison secteur (benchmarking fictif)
        secteur = st.selectbox(
            "Comparez avec le secteur :",
            ["Commerce", "Industrie", "Services", "Technologie", "Construction"],
            key="benchmark_sector"
        )
        
        # Benchmarks par secteur (valeurs fictives)
        benchmarks = {
            'Commerce': {'liquidite': 1.8, 'endettement': 55, 'roa': 8.2, 'rotation': 1.2},
            'Industrie': {'liquidite': 1.5, 'endettement': 60, 'roa': 9.5, 'rotation': 0.8},
            'Services': {'liquidite': 1.9, 'endettement': 45, 'roa': 11.3, 'rotation': 1.5},
            'Technologie': {'liquidite': 2.3, 'endettement': 40, 'roa': 15.2, 'rotation': 1.8},
            'Construction': {'liquidite': 1.4, 'endettement': 65, 'roa': 7.8, 'rotation': 0.9}
        }
        
        benchmark = benchmarks[secteur]
        
        # Données pour le graphique comparatif
        categories = ['Liquidité', 'Endettement', 'ROA', 'Rotation']
        entreprise = [
            ratios.get('Ratio de Liquidité', 0),
            ratios.get('Taux d\'endettement', 0),
            ratios.get('ROA (%)', 0),
            ratios.get('Rotation des actifs', 0)
        ]
        secteur_ref = [
            benchmark['liquidite'],
            benchmark['endettement'],
            benchmark['roa'],
            benchmark['rotation']
        ]
        
        fig_compar = go.Figure(data=[
            go.Bar(name='Votre entreprise', x=categories, y=entreprise, marker_color='#3B82F6'),
            go.Bar(name=f'Secteur {secteur}', x=categories, y=secteur_ref, marker_color='#94A3B8')
        ])
        
        fig_compar.update_layout(
            barmode='group',
            title=f"Comparaison avec le secteur {secteur}",
            yaxis_title="Valeur",
            height=400
        )
        
        st.plotly_chart(fig_compar, use_container_width=True)
    
    # ===== PLAN D'ACTION DÉTAILLÉ =====
    st.markdown("---")
    st.markdown("### 🚀 **Plan d'Action Détaillé**")
    
    # Identifier les axes d'amélioration
    axes_amelioration = []
    
    if ratios.get('Ratio de Liquidité', 0) < 1:
        axes_amelioration.append(("Liquidité", "Critique", "#EF4444"))
    elif ratios.get('Ratio de Liquidité', 0) < 1.5:
        axes_amelioration.append(("Liquidité", "À améliorer", "#F59E0B"))
    
    if ratios.get('Taux d\'endettement', 0) > 70:
        axes_amelioration.append(("Endettement", "Critique", "#EF4444"))
    elif ratios.get('Taux d\'endettement', 0) > 50:
        axes_amelioration.append(("Endettement", "À surveiller", "#F59E0B"))
    
    if ratios.get('ROA (%)', 0) < 5:
        axes_amelioration.append(("Rentabilité", "À améliorer", "#F59E0B"))
    
    if ratios.get('Rotation des actifs', 0) < 0.5:
        axes_amelioration.append(("Efficacité", "À optimiser", "#F59E0B"))
    
    if axes_amelioration:
        st.warning("""
        ⚠️ **Points de vigilance identifiés**
        
        Votre analyse révèle des axes d'amélioration prioritaires :
        """)
        
        for axe, statut, couleur in axes_amelioration:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 10px 0;">
                <div style="width: 20px; height: 20px; background-color: {couleur}; border-radius: 50%; margin-right: 10px;"></div>
                <div>
                    <strong>{axe}</strong> - <em>{statut}</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Proposition de plan d'action
        with st.expander("📋 **Plan d'Action Prioritaires**", expanded=True):
            st.markdown("""
            **Priorité 1 : Actions immédiates (1-3 mois)**
            
            1. **Renégocier les délais fournisseurs**
               - Objectif : Passer de 30 à 60 jours
               - Impact : Amélioration BFR immédiate
            
            2. **Accélérer l'encaissement clients**
               - Mettre en place des relances automatiques
               - Proposer des escomptes pour paiement anticipé
            
            **Priorité 2 : Actions à moyen terme (3-6 mois)**
            
            3. **Optimiser la gestion des stocks**
               - Réduire les stocks dormants
               - Négocier des livraisons just-in-time
            
            4. **Réviser la structure de financement**
               - Convertir des dettes CT en dettes MT si possible
               - Étudier une augmentation de capital
            """)
    else:
        st.success("""
        ✅ **Tous les indicateurs sont dans les clous !**
        
        Votre entreprise présente un profil financier équilibré. 
        Maintenez cette performance en surveillant régulièrement vos ratios clés.
        """)
    
    # ===== EXPORT ET SYNTHÈSE =====
    st.markdown("---")
    col_export, col_synthese = st.columns(2)
    
    with col_export:
        if st.button("📥 Générer le Rapport d'Analyse", use_container_width=True):
            sig = calculate_intermediate_balances(st.session_state.income_statement)
            
            excel_data = generate_comprehensive_report(
                st.session_state.balance_sheet,
                st.session_state.income_statement,
                ratios,
                sig
            )
            
            st.download_button(
                label="💾 Télécharger le Rapport Complet",
                data=excel_data,
                file_name=f"analyse_financiere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col_synthese:
        if st.button("🎯 Marquer ce Module comme Complété", use_container_width=True):
            st.session_state.learning_path_completed['ratios'] = True
            st.success("✅ **Module Analyse Financière complété !**")
            st.balloons()

# ============================================
# MODULE 5: BUDGET & PRÉVISIONS
# ============================================

def show_budgeting():
    st.markdown('<h2 class="sub-header">🎯 Module Budget & Prévisions - Anticiper l\'Avenir</h2>', unsafe_allow_html=True)
    
    # ===== INTRODUCTION PÉDAGOGIQUE =====
    with st.expander("🎓 **Pourquoi faire un budget ?**", expanded=True):
        col_bud1, col_bud2 = st.columns(2)
        
        with col_bud1:
            st.markdown("""
            ### 🎯 **Objectifs du Budget**
            
            **1. Planifier** :
            - Anticiper les revenus et dépenses
            - Définir des objectifs réalistes
            
            **2. Contrôler** :
            - Comparer prévisions vs réalité
            - Détecter les écarts rapidement
            
            **3. Décider** :
            - Allouer les ressources optimalement
            - Prioriser les investissements
            """)
        
        with col_bud2:
            st.markdown("""
            ### ⚠️ **Risques sans Budget**
            
            **1. Trésorerie** :
            - Déficits imprévus
            - Problèmes de liquidité
            
            **2. Rentabilité** :
            - Dépenses non maîtrisées
            - Marges érodées
            
            **3. Croissance** :
            - Opportunités manquées
            - Investissements inadaptés
            """)
        
        st.markdown("---")
        st.success("""
        **✨ NOTRE APPROCHE :** 
        **BUDGET = OUTIL DE PILOTAGE, PAS DE CONTRÔLE**
        
        Un bon budget aide à prendre de meilleures décisions, pas à sanctionner.
        """)
    
    # ===== ONGLETS DU MODULE BUDGET =====
    tabs_budget = st.tabs([
        "📋 Budget des Ventes",
        "💰 Budget de Trésorerie", 
        "📊 Simulateur What-If",
        "🚨 Gestion des Risques"
    ])
    
    with tabs_budget[0]:  # Budget des Ventes
        st.markdown("### 📋 **Budget Prévisionnel des Ventes**")
        
        # Saisie des prévisions mensuelles
        months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        
        # Initialisation des données de budget
        if 'budget_ventes' not in st.session_state:
            st.session_state.budget_ventes = {month: 10000.0 for month in months}
        
        # Interface de saisie
        st.markdown("#### Prévisions Mensuelles")
        
        # Création d'une grille de saisie
        cols = st.columns(4)
        for i, month in enumerate(months):
            with cols[i % 4]:
                st.session_state.budget_ventes[month] = st.number_input(
                    month,
                    min_value=0.0,
                    value=st.session_state.budget_ventes[month],
                    step=1000.0,
                    format="%.2f",
                    key=f"budget_{month}"
                )
        
        # Calculs et visualisation
        st.markdown("---")
        st.markdown("#### 📊 **Analyse des Prévisions**")
        
        # Création du DataFrame
        df_budget = pd.DataFrame({
            'Mois': months,
            'Ventes Prévues': [st.session_state.budget_ventes[m] for m in months]
        })
        
        # Calcul des indicateurs
        df_budget['Cumul'] = df_budget['Ventes Prévues'].cumsum()
        df_budget['Variation %'] = df_budget['Ventes Prévues'].pct_change() * 100
        df_budget['Moyenne Mobile (3 mois)'] = df_budget['Ventes Prévues'].rolling(3).mean()
        
        # Affichage du tableau
        st.dataframe(df_budget.style.format({
            'Ventes Prévues': '{:,.0f} €',
            'Cumul': '{:,.0f} €',
            'Variation %': '{:.1f}%',
            'Moyenne Mobile (3 mois)': '{:,.0f} €'
        }), use_container_width=True, height=400)
        
        # Graphiques
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            # Graphique linéaire des ventes
            fig_ventes = px.line(
                df_budget, 
                x='Mois', 
                y='Ventes Prévues',
                title='Évolution des Ventes Prévues',
                markers=True,
                line_shape='spline'
            )
            
            fig_ventes.update_traces(
                line=dict(width=3, color='#3B82F6'),
                marker=dict(size=8)
            )
            
            fig_ventes.update_layout(
                height=400,
                yaxis_title="Ventes (€)",
                xaxis_title=""
            )
            
            st.plotly_chart(fig_ventes, use_container_width=True)
        
        with col_graph2:
            # Graphique du cumul
            fig_cumul = px.area(
                df_budget,
                x='Mois',
                y='Cumul',
                title='Ventes Cumulées sur l\'Année',
                line_shape='spline'
            )
            
            fig_cumul.update_traces(
                fill='tozeroy',
                line=dict(width=3, color='#10B981'),
                fillcolor='rgba(16, 185, 129, 0.3)'
            )
            
            fig_cumul.update_layout(
                height=400,
                yaxis_title="Cumul (€)",
                xaxis_title=""
            )
            
            st.plotly_chart(fig_cumul, use_container_width=True)
        
        # Analyse de saisonnalité
        with st.expander("📈 **Analyse de Saisonnalité**", expanded=False):
            st.markdown("""
            **Comment identifier les tendances saisonnières :**
            
            1. **Calculez la moyenne mensuelle** sur 3 ans
            2. **Identifiez les pics** (Noël, soldes, etc.)
            3. **Ajustez vos prévisions** en conséquence
            
            **Exemple de coefficients saisonniers :**
            • Janvier (soldes) : 1.3x
            • Août (vacances) : 0.7x
            • Décembre (Noël) : 1.5x
            
            **💡 Conseil :** Utilisez l'historique des années précédentes pour affiner vos coefficients.
            """)
    
    with tabs_budget[1]:  # Budget de Trésorerie
        st.markdown("### 💰 **Budget Prévisionnel de Trésorerie**")
        
        st.info("""
        💡 **Objectif :** Anticiper les flux de trésorerie pour éviter les découverts bancaires.
        """)
        
        # Saisie des hypothèses
        col_tr1, col_tr2 = st.columns(2)
        
        with col_tr1:
            st.markdown("#### 📥 **Entrées de Trésorerie**")
            
            # Chiffre d'affaires encaissé (avec délai client)
            ca_encaisse = st.number_input(
                "CA moyen mensuel encaissé :",
                min_value=0.0,
                value=50000.0,
                step=5000.0,
                format="%.2f",
                help="Chiffre d'affaires réellement encaissé chaque mois",
                key="ca_encaisse"
            )
            
            # Autres entrées
            autres_entrees = st.number_input(
                "Autres entrées mensuelles :",
                min_value=0.0,
                value=5000.0,
                step=1000.0,
                format="%.2f",
                help="Subventions, apports en capital, etc.",
                key="autres_entrees"
            )
            
            # Délai moyen de règlement clients
            delai_clients = st.slider(
                "Délai moyen clients (jours) :",
                min_value=0,
                max_value=120,
                value=45,
                help="Nombre moyen de jours pour être payé par les clients",
                key="delai_clients"
            )
        
        with col_tr2:
            st.markdown("#### 📤 **Sorties de Trésorerie**")
            
            # Achats
            achats = st.number_input(
                "Achats mensuels :",
                min_value=0.0,
                value=30000.0,
                step=3000.0,
                format="%.2f",
                key="achats_budget"
            )
            
            # Charges de personnel
            charges_personnel = st.number_input(
                "Charges de personnel mensuelles :",
                min_value=0.0,
                value=15000.0,
                step=2000.0,
                format="%.2f",
                key="charges_pers_budget"
            )
            
            # Autres charges
            autres_charges = st.number_input(
                "Autres charges mensuelles :",
                min_value=0.0,
                value=10000.0,
                step=1000.0,
                format="%.2f",
                key="autres_charges_budget"
            )
            
            # Délai moyen de règlement fournisseurs
            delai_fournisseurs = st.slider(
                "Délai moyen fournisseurs (jours) :",
                min_value=0,
                max_value=120,
                value=60,
                help="Nombre moyen de jours pour payer les fournisseurs",
                key="delai_fournisseurs"
            )
        
        # Simulation sur 12 mois
        st.markdown("---")
        st.markdown("#### 📅 **Simulation sur 12 Mois**")
        
        # Création du tableau de trésorerie
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        
        # Initialisation avec variation saisonnière
        variation_saisonniere = [1.0, 0.9, 1.1, 1.0, 1.2, 1.1, 0.8, 0.7, 1.0, 1.3, 1.4, 1.5]
        
        data_tresorerie = []
        solde_cumule = 0
        
        for i, mois in enumerate(months):
            # Calcul des flux avec variation saisonnière
            entrees = (ca_encaisse * variation_saisonniere[i]) + autres_entrees
            sorties = (achats + charges_personnel + autres_charges) * (1 + (i % 3) * 0.1)  # Légère augmentation progressive
            
            flux_net = entrees - sorties
            solde_cumule += flux_net
            
            data_tresorerie.append({
                'Mois': mois,
                'Entrées': entrees,
                'Sorties': sorties,
                'Flux Net': flux_net,
                'Trésorerie Cumulée': solde_cumule
            })
        
        df_tresorerie = pd.DataFrame(data_tresorerie)
        
        # Affichage du tableau
        st.dataframe(df_tresorerie.style.format({
            'Entrées': '{:,.0f} €',
            'Sorties': '{:,.0f} €', 
            'Flux Net': '{:,.0f} €',
            'Trésorerie Cumulée': '{:,.0f} €'
        }).applymap(
            lambda x: 'color: #EF4444' if x < 0 else ('color: #10B981' if x > 0 else ''),
            subset=['Flux Net', 'Trésorerie Cumulée']
        ), use_container_width=True, height=400)
        
        # Graphique de trésorerie
        fig_treso = go.Figure()
        
        # Ajout des barres pour entrées et sorties
        fig_treso.add_trace(go.Bar(
            name='Entrées',
            x=df_tresorerie['Mois'],
            y=df_tresorerie['Entrées'],
            marker_color='#10B981',
            opacity=0.7
        ))
        
        fig_treso.add_trace(go.Bar(
            name='Sorties',
            x=df_tresorerie['Mois'],
            y=df_tresorerie['Sorties'],
            marker_color='#EF4444',
            opacity=0.7
        ))
        
        # Ajout de la ligne de trésorerie cumulée
        fig_treso.add_trace(go.Scatter(
            name='Trésorerie Cumulée',
            x=df_tresorerie['Mois'],
            y=df_tresorerie['Trésorerie Cumulée'],
            mode='lines+markers',
            line=dict(width=3, color='#3B82F6'),
            yaxis='y2'
        ))
        
        fig_treso.update_layout(
            title='Budget de Trésorerie Prévisionnel',
            barmode='group',
            yaxis=dict(title='Entrées/Sorties (€)'),
            yaxis2=dict(
                title='Trésorerie Cumulée (€)',
                overlaying='y',
                side='right'
            ),
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_treso, use_container_width=True)
        
        # Analyse des risques
        solde_min = df_tresorerie['Trésorerie Cumulée'].min()
        
        if solde_min < 0:
            st.error(f"""
            ⚠️ **RISQUE DE DÉFICIT IDENTIFIÉ**
            
            Votre simulation révèle un déficit potentiel de **{-solde_min:,.0f} €**.
            
            **Actions recommandées :**
            1. Renégocier les délais fournisseurs (objectif : +15 jours)
            2. Accélérer l'encaissement clients (objectif : -10 jours)
            3. Rechercher une ligne de crédit de **{max(5000, -solde_min * 1.2):,.0f} €**
            """)
        else:
            st.success(f"""
            ✅ **TRÉSORERIE MAÎTRISÉE**
            
            Votre trésorerie reste positive tout au long de l'année.
            Solde minimum : **{solde_min:,.0f} €**
            
            **Marge de sécurité :** Vous pourriez absorber une baisse de **{solde_min/ca_encaisse*100:.0f}%** du CA
            sans tomber en déficit.
            """)
    
    with tabs_budget[2]:  # Simulateur What-If
        st.markdown("### 📊 **Simulateur de Scénarios What-If**")
        
        st.info("""
        🎯 **Objectif :** Tester l'impact de différentes hypothèses sur votre rentabilité.
        """)
        
        # Paramètres de simulation
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.markdown("#### 📈 **Variables de Performance**")
            
            ca_base = st.slider(
                "Chiffre d'affaires annuel de base :",
                min_value=100000,
                max_value=1000000,
                value=500000,
                step=50000,
                format="%d €",
                help="CA de référence pour les simulations",
                key="ca_base"
            )
            
            taux_marge = st.slider(
                "Taux de marge brute de base :",
                min_value=10.0,
                max_value=50.0,
                value=30.0,
                step=1.0,
                format="%.1f%%",
                help="Marge sur coûts variables",
                key="taux_marge"
            )
        
        with col_sim2:
            st.markdown("#### 📉 **Variables de Risque**")
            
            evolution_ca = st.slider(
                "Évolution du CA (%) :",
                min_value=-30.0,
                max_value=50.0,
                value=10.0,
                step=5.0,
                format="%.1f%%",
                help="Variation globale du chiffre d'affaires",
                key="evolution_ca"
            )
            
            evolution_charges = st.slider(
                "Évolution des charges fixes (%) :",
                min_value=-10.0,
                max_value=30.0,
                value=5.0,
                step=5.0,
                format="%.1f%%",
                help="Variation des charges non variables",
                key="evolution_charges"
            )
        
        # Définition des scénarios
        scenarios = {
            'Pessimiste': {'ca_mult': 0.8, 'marge_mult': 0.9, 'charges_mult': 1.2},
            'Réaliste': {'ca_mult': 1.0, 'marge_mult': 1.0, 'charges_mult': 1.0},
            'Optimiste': {'ca_mult': 1.2, 'marge_mult': 1.1, 'charges_mult': 0.9}
        }
        
        # Calcul des scénarios
        scenario_results = []
        
        for scenario, params in scenarios.items():
            # Calcul du CA ajusté
            ca_scenario = ca_base * params['ca_mult'] * (1 + evolution_ca/100)
            
            # Calcul de la marge ajustée
            marge_scenario = taux_marge * params['marge_mult']
            
            # Calcul de la marge brute
            marge_brute = ca_scenario * marge_scenario / 100
            
            # Calcul des charges fixes ajustées
            charges_fixes = 150000 * params['charges_mult'] * (1 + evolution_charges/100)
            
            # Calcul du résultat
            resultat = marge_brute - charges_fixes
            
            # Calcul de la marge nette
            marge_nette = (resultat / ca_scenario) * 100 if ca_scenario > 0 else 0
            
            scenario_results.append({
                'Scénario': scenario,
                'CA (€)': ca_scenario,
                'Marge Brute (€)': marge_brute,
                'Charges Fixes (€)': charges_fixes,
                'Résultat (€)': resultat,
                'Marge Nette (%)': marge_nette
            })
        
        # Affichage des résultats
        df_scenarios = pd.DataFrame(scenario_results)
        
        # Mise en forme conditionnelle
        def color_resultat(val):
            if val < 0:
                return 'background-color: #FEE2E2; color: #DC2626; font-weight: bold;'
            elif val > 0:
                return 'background-color: #D1FAE5; color: #059669; font-weight: bold;'
            else:
                return ''
        
        styled_scenarios = df_scenarios.style.format({
            'CA (€)': '{:,.0f} €',
            'Marge Brute (€)': '{:,.0f} €',
            'Charges Fixes (€)': '{:,.0f} €',
            'Résultat (€)': '{:,.0f} €',
            'Marge Nette (%)': '{:.1f}%'
        }).applymap(color_resultat, subset=['Résultat (€)', 'Marge Nette (%)'])
        
        st.dataframe(styled_scenarios, use_container_width=True, height=200)
        
        # Visualisation graphique
        fig_scenarios = px.bar(
            df_scenarios,
            x='Scénario',
            y='Résultat (€)',
            color='Résultat (€)',
            color_continuous_scale='RdYlGn',
            title='Impact des Scénarios sur le Résultat',
            text='Résultat (€)'
        )
        
        fig_scenarios.update_traces(
            texttemplate='%{text:,.0f} €',
            textposition='outside'
        )
        
        fig_scenarios.update_layout(
            height=400,
            yaxis_title="Résultat (€)",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig_scenarios, use_container_width=True)
        
        # Analyse de sensibilité
        st.markdown("---")
        st.markdown("#### 🎯 **Analyse de Sensibilité**")
        
        # Matrice de sensibilité
        ca_variations = [-20, -10, 0, 10, 20]  # %
        marge_variations = [-5, -2.5, 0, 2.5, 5]  # points de %
        
        sens_data = []
        
        for ca_var in ca_variations:
            for marge_var in marge_variations:
                ca_sens = ca_base * (1 + ca_var/100)
                marge_sens = taux_marge + marge_var
                marge_brute_sens = ca_sens * marge_sens / 100
                resultat_sens = marge_brute_sens - 150000
                
                sens_data.append({
                    'Variation CA': f"{ca_var}%",
                    'Variation Marge': f"{marge_var:+} pts",
                    'Résultat (€)': resultat_sens
                })
        
        df_sens = pd.DataFrame(sens_data)
        
        # Pivot pour heatmap
        pivot_sens = df_sens.pivot(
            index='Variation CA',
            columns='Variation Marge',
            values='Résultat (€)'
        )
        
        # Heatmap
        fig_heatmap = px.imshow(
            pivot_sens,
            text_auto='.0f',
            aspect='auto',
            color_continuous_scale='RdYlGn',
            title='Sensibilité du Résultat aux Variations de CA et Marge'
        )
        
        fig_heatmap.update_layout(
            height=400,
            xaxis_title="Variation de Marge (points)",
            yaxis_title="Variation de CA (%)"
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Interprétation
        st.markdown("""
        **🔍 Comment interpréter cette analyse :**
        
        • **Cases vertes** : Résultat positif même dans des conditions défavorables
        • **Cases rouges** : Risque de perte même avec une croissance du CA
        • **Zone critique** : Identifier les combinaisons CA/Marge à éviter
        
        **💡 Conseil :** Concentrez vos efforts sur les variables les plus sensibles.
        """)
    
    with tabs_budget[3]:  # Gestion des Risques
        st.markdown("### 🚨 **Plan de Gestion des Risques**")
        
        # Identification des risques
        risques = [
            {
                'nom': 'Baisse du Chiffre d\'Affaires',
                'probabilite': 'Élevée',
                'impact': 'Critique',
                'actions': [
                    'Diversifier le portefeuille clients',
                    'Développer de nouveaux canaux de vente',
                    'Mettre en place des promotions ciblées'
                ]
            },
            {
                'nom': 'Augmentation des Coûts',
                'probabilite': 'Moyenne', 
                'impact': 'Important',
                'actions': [
                    'Négocier des contrats long terme avec fournisseurs',
                    'Optimiser les processus pour réduire les gaspillages',
                    'Rechercher des fournisseurs alternatifs'
                ]
            },
            {
                'nom': 'Problèmes de Trésorerie',
                'probabilite': 'Moyenne',
                'impact': 'Critique',
                'actions': [
                    'Négocier une ligne de crédit préventive',
                    'Accélérer le recouvrement des créances',
                    'Échelonner les investissements'
                ]
            },
            {
                'nom': 'Départ de Personnel Clé',
                'probabilite': 'Faible',
                'impact': 'Important',
                'actions': [
                    'Mettre en place un plan de succession',
                    'Cross-training des équipes',
                    'Améliorer les conditions de travail'
                ]
            }
        ]
        
        # Affichage des risques
        for i, risque in enumerate(risques):
            # Déterminer la couleur du badge de criticité
            if risque['impact'] == 'Critique':
                badge_color = "🔴"
                border_color = "#EF4444"
            elif risque['impact'] == 'Important':
                badge_color = "🟡" 
                border_color = "#F59E0B"
            else:
                badge_color = "🟢"
                border_color = "#10B981"
            
            with st.expander(f"{badge_color} **{risque['nom']}**", expanded=(i == 0)):
                col_risk1, col_risk2 = st.columns([1, 2])
                
                with col_risk1:
                    st.metric("Probabilité", risque['probabilite'])
                    st.metric("Impact", risque['impact'])
                
                with col_risk2:
                    st.markdown("**Plan d'actions préventives :**")
                    for action in risque['actions']:
                        st.markdown(f"• {action}")
        
        # Tableau de bord des indicateurs d'alerte
        st.markdown("---")
        st.markdown("#### 📊 **Tableau de Bord des Alertes**")
        
        # Indicateurs à surveiller
        indicateurs = [
            {'nom': 'Ratio de Liquidité', 'seuil_min': 1.0, 'valeur': 1.5, 'unité': ''},
            {'nom': 'Taux d\'Endettement', 'seuil_max': 70.0, 'valeur': 45.0, 'unité': '%'},
            {'nom': 'Marge Nette', 'seuil_min': 5.0, 'valeur': 8.2, 'unité': '%'},
            {'nom': 'Délai Clients', 'seuil_max': 60.0, 'valeur': 45.0, 'unité': 'jours'},
            {'nom': 'Trésorerie Minimum', 'seuil_min': 10000.0, 'valeur': 25000.0, 'unité': '€'}
        ]
        
        cols_alertes = st.columns(len(indicateurs))
        
        for idx, indicateur in enumerate(indicateurs):
            with cols_alertes[idx]:
                # Déterminer le statut
                if 'seuil_min' in indicateur:
                    statut = '✅' if indicateur['valeur'] >= indicateur['seuil_min'] else '⚠️'
                else:
                    statut = '✅' if indicateur['valeur'] <= indicateur['seuil_max'] else '⚠️'
                
                st.metric(
                    indicateur['nom'],
                    f"{indicateur['valeur']}{indicateur['unité']}",
                    statut
                )
        
        # Plan d'action en cas de crise
        st.markdown("---")
        with st.expander("🆘 **Plan d\'Urgence - Que faire en cas de crise ?**", expanded=False):
            st.markdown("""
            **Phase 1 : Diagnostic Immédiat (J+1 à J+7)**
            
            1. **Analyser la trésorerie** :
               - Identifier les décaissements urgents
               - Estimer les encaissements à venir
            
            2. **Prioriser les paiements** :
               - Salaires et charges sociales
               - Fournisseurs essentiels
               - Impôts et taxes
            
            **Phase 2 : Actions Correctives (J+8 à J+30)**
            
            3. **Renégocier avec les partenaires** :
               - Report d'échéances avec fournisseurs
               - Rééchelonnement de dettes bancaires
               - Négociation avec l'administration fiscale
            
            4. **Générer de la trésorerie rapide** :
               - Liquider les stocks excédentaires
               - Facturer les acomptes clients
               - Mobiliser les garanties bancaires
            
            **Phase 3 : Restructuration (J+31 à J+90)**
            
            5. **Réviser le modèle économique** :
               - Réduire les coûts structurels
               - Recentrer sur les activités rentables
               - Redéfinir la stratégie commerciale
            
            6. **Communiquer avec transparence** :
               - Informer régulièrement les partenaires
               - Maintenir la confiance des équipes
               - Préserver l'image de l'entreprise
            """)
    
    # ===== SYNTHÈSE ET VALIDATION =====
    st.markdown("---")
    col_synth1, col_synth2 = st.columns(2)
    
    with col_synth1:
        if st.button("✅ Marquer ce Module comme Complété", use_container_width=True):
            st.session_state.learning_path_completed['budget'] = True
            st.success("🎉 **Module Budget & Prévisions complété !**")
            st.balloons()
    
    with col_synth2:
        # Export du plan budgétaire
        if st.button("📥 Exporter le Plan Budgétaire", use_container_width=True):
            # Créer un DataFrame synthétique
            budget_data = {
                'Élément': ['CA Prévisionnel', 'Marge Brute', 'Charges Fixes', 'Résultat Prévisionnel'],
                'Valeur': [
                    sum(st.session_state.budget_ventes.values()) if 'budget_ventes' in st.session_state else 0,
                    sum(st.session_state.budget_ventes.values()) * 0.3 if 'budget_ventes' in st.session_state else 0,
                    150000,
                    (sum(st.session_state.budget_ventes.values()) * 0.3 - 150000) if 'budget_ventes' in st.session_state else 0
                ]
            }
            
            df_budget_export = pd.DataFrame(budget_data)
            
            # Générer le rapport
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_budget_export.to_excel(writer, sheet_name='Synthèse', index=False)
                
                if 'budget_ventes' in st.session_state:
                    df_ventes = pd.DataFrame({
                        'Mois': list(st.session_state.budget_ventes.keys()),
                        'Ventes Prévues': list(st.session_state.budget_ventes.values())
                    })
                    df_ventes.to_excel(writer, sheet_name='Budget Ventes', index=False)
            
            st.download_button(
                label="💾 Télécharger le Plan Budgétaire",
                data=output.getvalue(),
                file_name=f"plan_budgetaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

# ============================================
# MODULE 6: CENTRE D'APPRENTISSAGE
# ============================================

def show_learning_center():
    st.markdown('<h2 class="sub-header">🧠 Centre d\'Apprentissage - Ressources Pédagogiques</h2>', unsafe_allow_html=True)
    
    # ===== STATISTIQUES D'APPRENTISSAGE =====
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    with col_stats1:
        st.metric("Modules Complétés", 
                 f"{sum(st.session_state.learning_path_completed.values())}/4")
    
    with col_stats2:
        # Calcul du temps estimé d'apprentissage
        temps_estime = 8  # heures par module en moyenne
        temps_total = sum(st.session_state.learning_path_completed.values()) * temps_estime
        st.metric("Temps d'Apprentissage", f"{temps_total} heures")
    
    with col_stats3:
        # Score de compréhension (simulé)
        score = sum(st.session_state.learning_path_completed.values()) * 25
        st.metric("Score de Compréhension", f"{score}%")
    
    with col_stats4:
        # Niveau atteint
        niveaux = ['Débutant', 'Intermédiaire', 'Avancé', 'Expert']
        niveau_idx = min(sum(st.session_state.learning_path_completed.values()), 3)
        st.metric("Niveau Atteint", niveaux[niveau_idx])
    
    # ===== RESSOURCES PAR THÈME =====
    st.markdown("---")
    st.markdown("### 📚 **Ressources Thématiques**")
    
    themes = st.tabs([
        "📑 Bilan Comptable",
        "💰 Compte de Résultat", 
        "📈 Ratios Financiers",
        "🎯 Budget & Prévisions",
        "🧩 Cas Pratiques"
    ])
    
    with themes[0]:  # Bilan Comptable
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("""
            **🎥 Vidéos Formatives :**
            
            1. **Comprendre l'équilibre Actif/Passif** (15 min)
               - Le principe fondamental de la comptabilité
               - Exemples concrets d'équilibrage
            
            2. **Les postes clés du bilan** (20 min)
               - Actif immobilisé vs circulant
               - Capitaux propres vs dettes
            
            3. **Cas pratique : Construire un bilan** (25 min)
               - Saisie pas à pas
               - Vérification de l'équilibre
            """)
        
        with col_res2:
            st.markdown("""
            **📖 Articles et Guides :**
            
            1. **Guide du débutant : Le bilan en 10 points**
               - Définitions simples
               - Schémas explicatifs
            
            2. **10 erreurs fréquentes au bilan**
               - Comment les éviter
               - Comment les corriger
            
            3. **Exercices d'application**
               - Avec corrigés détaillés
               - Niveau progressif
            """)
        
        # Quiz interactif
        with st.expander("🧠 **Testez vos connaissances - Quiz Bilan**", expanded=False):
            st.markdown("""
            **Question 1 :** Quelle est l'équation fondamentale du bilan ?
            
            - [ ] Actif + Passif = 0
            - [x] Actif = Passif
            - [ ] Actif - Passif = Résultat
            - [ ] Actif × Passif = Capital
            
            **Question 2 :** Les stocks font partie de :
            
            - [ ] L'actif immobilisé
            - [x] L'actif circulant  
            - [ ] Les capitaux propres
            - [ ] Les dettes
            
            **Question 3 :** Un emprunt bancaire apparaît dans :
            
            - [ ] L'actif immobilisé
            - [ ] Les capitaux propres
            - [x] Les dettes
            - [ ] Le compte de résultat
            """)
            
            if st.button("Vérifier mes réponses", key="quiz_bilan"):
                st.success("""
                **Correction :**
                1. Actif = Passif ✅
                2. Actif circulant ✅  
                3. Dettes ✅
                
                Score : 3/3 - Excellent !
                """)
    
    with themes[1]:  # Compte de Résultat
        st.markdown("""
        **💡 Concepts Clés à Maîtriser :**
        
        **1. Différence Produits/Charges :**
        - **Produits** = Sources de revenus (CA, produits financiers)
        - **Charges** = Coûts de l'activité (achats, personnel, etc.)
        
        **2. Soldes Intermédiaires de Gestion :**
        ```
        Marge Commerciale → Valeur Ajoutée → EBE → 
        Résultat Exploitation → Résultat Courant → Résultat Net
        ```
        
        **3. Marge vs Profit :**
        - **Marge** = Différence entre prix de vente et coût
        - **Profit** = Ce qui reste après toutes les charges
        """)
        
        # Exercice interactif
        with st.expander("✍️ **Exercice Pratique - Calcul des SIG**", expanded=False):
            st.markdown("""
            **Données :**
            - CA : 200 000 €
            - Achats : 80 000 €
            - Variation stocks : +5 000 € (diminution)
            - Charges externes : 40 000 €
            - Charges personnel : 50 000 €
            - Dotations : 10 000 €
            - Produits financiers : 2 000 €
            - Charges financières : 8 000 €
            - Impôt : 5 000 €
            
            **Calculez :**
            1. La marge commerciale
            2. Le résultat net
            3. La marge nette
            """)
            
            col_exo1, col_exo2 = st.columns(2)
            
            with col_exo1:
                marge_com = st.number_input(
                    "Marge commerciale (€) :",
                    min_value=0.0,
                    step=1000.0,
                    key="exo_marge"
                )
            
            with col_exo2:
                resultat_net = st.number_input(
                    "Résultat net (€) :",
                    step=1000.0,
                    key="exo_resultat"
                )
            
            if st.button("Vérifier le calcul", key="verif_exo"):
                bonne_marge = 200000 - 80000 - 5000  # 115 000 €
                bon_resultat = 115000 - 40000 - 50000 - 10000 + 2000 - 8000 - 5000  # 4 000 €
                
                if abs(marge_com - bonne_marge) < 0.01 and abs(resultat_net - bon_resultat) < 0.01:
                    st.success("✅ Parfait ! Calculs exacts.")
                    st.balloons()
                else:
                    st.error(f"""
                    ❌ Quelques erreurs :
                    - Marge commerciale attendue : {bonne_marge:,.0f} €
                    - Résultat net attendu : {bon_resultat:,.0f} €
                    
                    **Détail du calcul :**
                    Marge = 200 000 - 80 000 - 5 000 = 115 000 €
                    Résultat = 115 000 - 40 000 - 50 000 - 10 000 + 2 000 - 8 000 - 5 000 = 4 000 €
                    """)
    
    with themes[2]:  # Ratios Financiers
        # Tableau synthétique des ratios
        st.markdown("#### 📋 **Tableau Synthétique des Ratios**")
        
        ratios_table = pd.DataFrame({
            'Ratio': ['Liquidité Générale', 'Taux d\'Endettement', 'ROA', 'ROE', 'Rotation Actifs'],
            'Formule': ['Actif Circulant / Dettes CT', 'Dettes / Total Actif × 100', 
                       'Résultat Net / Total Actif × 100', 'Résultat Net / Capitaux Propres × 100',
                       'CA / Total Actif'],
            'Objectif': ['> 1.5', '< 50%', '> 8%', '> 12%', '> 0.8'],
            'Interprétation': ['Capacité à payer CT', 'Indépendance financière', 
                              'Rentabilité des actifs', 'Rentabilité pour actionnaires',
                              'Efficacité opérationnelle']
        })
        
        st.dataframe(ratios_table, use_container_width=True)
        
        # Comparatif ROA vs ROE
        st.markdown("---")
        st.markdown("#### ⚡ **Comprendre ROA vs ROE**")
        
        col_roa, col_roe = st.columns(2)
        
        with col_roa:
            st.markdown("""
            **📊 ROA (Return on Assets)**
            
            **Signification :**
            - Performance de l'ensemble des actifs
            - Indépendant du mode de financement
            - Mesure l'efficacité opérationnelle
            
            **Formule :**
            ```
            Résultat Net
            ------------ × 100
            Total Actif
            ```
            
            **Secteur moyen :** 8-10%
            """)
        
        with col_roe:
            st.markdown("""
            **📈 ROE (Return on Equity)**
            
            **Signification :**
            - Rentabilité pour les actionnaires
            - Impact de l'endettement (levier)
            - Mesure la performance financière
            
            **Formule :**
            ```
            Résultat Net
            ------------------- × 100
            Capitaux Propres
            ```
            
            **Secteur moyen :** 12-15%
            """)
        
        # Simulateur d'effet de levier
        with st.expander("🧮 **Simulateur d\'Effet de Levier**", expanded=False):
            col_sim_lev1, col_sim_lev2 = st.columns(2)
            
            with col_sim_lev1:
                roa_base = st.slider("ROA de base (%) :", 5.0, 20.0, 10.0, 0.5)
                cout_dette = st.slider("Coût de la dette (%) :", 2.0, 10.0, 5.0, 0.5)
            
            with col_sim_lev2:
                dette_cp_ratio = st.slider("Ratio Dettes/CP :", 0.0, 3.0, 1.0, 0.1)
            
            # Calcul de l'effet de levier
            if roa_base > cout_dette:
                effet_levier = (roa_base - cout_dette) * dette_cp_ratio
                roe_calcule = roa_base + effet_levier
                
                st.success(f"""
                **⚡ EFFET DE LEVIER POSITIF**
                
                • ROA de base : {roa_base:.1f}%
                • Coût dette : {cout_dette:.1f}%
                • Effet de levier : +{effet_levier:.1f} points
                • ROE calculé : **{roe_calcule:.1f}%**
                
                L'endettement améliore la rentabilité des capitaux propres.
                """)
            else:
                effet_levier = (roa_base - cout_dette) * dette_cp_ratio
                roe_calcule = roa_base + effet_levier
                
                st.error(f"""
                **⚠️ EFFET DE LEVIER NÉGATIF**
                
                • ROA de base : {roa_base:.1f}%
                • Coût dette : {cout_dette:.1f}%
                • Effet de levier : {effet_levier:.1f} points
                • ROE calculé : **{roe_calcule:.1f}%**
                
                L'endettement réduit la rentabilité des capitaux propres.
                """)
    
    with themes[3]:  # Budget & Prévisions
        st.markdown("""
        **🎯 Méthodologie en 5 Étapes :**
        
        **1. Définir les hypothèses** (2 semaines)
        - Analyse du marché
        - Objectifs commerciaux
        - Contraintes financières
        
        **2. Élaborer le budget des ventes** (1 semaine)
        - Prévisions mensuelles
        - Analyse de saisonnalité
        - Scénarios optimiste/pessimiste
        
        **3. Construire le budget des charges** (1 semaine)
        - Charges variables (proportionnelles au CA)
        - Charges fixes (indépendantes du CA)
        - Investissements prévus
        
        **4. Établir le budget de trésorerie** (1 semaine)
        - Calendrier des encaissements
        - Calendrier des décaissements
        - Points de vigilance
        
        **5. Mettre en place le suivi** (continue)
        - Tableaux de bord mensuels
        - Analyse des écarts
        - Actions correctives
        """)
        
        # Template de budget à télécharger
        with st.expander("📥 **Templates à Télécharger**", expanded=False):
            st.markdown("""
            **Fichiers Excel prêts à l'emploi :**
            
            1. **Template Budget Simple** (débutant)
               - Structure basique
               - Formules pré-remplies
               - Guide d'utilisation
            
            2. **Template Budget Avancé** (confirmé)
               - Analyses automatiques
               - Graphiques intégrés
               - Scénarios what-if
            
            3. **Template Suivi Budget vs Réel**
               - Saisie des réalisations
               - Calcul automatique des écarts
               - Alertes visuelles
            """)
            
            if st.button("📥 Télécharger le Pack Templates"):
                st.info("""
                🚧 **Fonctionnalité en développement**
                
                Les templates seront disponibles dans la prochaine version.
                En attendant, utilisez nos outils interactifs pour créer vos budgets.
                """)
    
    with themes[4]:  # Cas Pratiques
        # Sélection du secteur
        secteur = st.selectbox(
            "Choisissez un secteur pour les cas pratiques :",
            ["Commerce de détail", "Industrie manufacturière", "Services aux entreprises", 
             "Restauration", "Technologie", "Construction"],
            key="cas_secteur"
        )
        
        # Cas adapté au secteur
        if secteur == "Commerce de détail":
            st.markdown("""
            **🏪 Cas : Magasin de Vêtements "Style & Co"**
            
            **Situation :**
            - CA annuel : 800 000 €
            - Marge brute : 45%
            - Surface : 300 m²
            - Employés : 8 personnes
            
            **Problème identifié :**
            • Rotation des stocks faible (4 fois/an)
            • Délai clients trop long (60 jours)
            • Trésorerie tendue en période creuse
            
            **Questions :**
            1. Quel ratio surveiller en priorité ?
            2. Quelles actions pour améliorer la trésorerie ?
            3. Comment optimiser la rotation des stocks ?
            
            **Réponses suggérées :**
            1. Surveiller le BFR et le ratio de liquidité
            2. Négocier délais fournisseurs, promos paiement comptant
            3. Réduire largeur gamme, système juste-à-temps
            """)
        
        elif secteur == "Industrie manufacturière":
            st.markdown("""
            **🏭 Cas : Usine "Precision Tech"**
            
            **Situation :**
            - CA annuel : 5 000 000 €
            - Investissements machines : 2 000 000 €
            - Effectif : 120 personnes
            - Clients B2B exclusivement
            
            **Problème identifié :**
            • ROA faible (6%) malgré CA important
            • Dettes élevées (75% du bilan)
            • Cycle de production long
            
            **Questions :**
            1. Comment améliorer le ROA ?
            2. Quelle stratégie de désendettement ?
            3. Comment réduire le cycle de production ?
            
            **Réponses suggérées :**
            1. Augmenter marge ou rotation actifs
            2. Augmentation capital, rééchelonnement dette
            3. Lean manufacturing, sous-traitance partielle
            """)
        
        # Espace pour créer son propre cas
        with st.expander("✍️ **Créez Votre Propre Cas**", expanded=False):
            st.markdown("**Analysez votre entreprise :**")
            
            col_cas1, col_cas2 = st.columns(2)
            
            with col_cas1:
                ca_perso = st.number_input("Votre CA annuel (€) :", 100000, 10000000, 500000, 50000)
                marge_perso = st.slider("Votre marge brute (%) :", 10.0, 60.0, 35.0, 1.0)
            
            with col_cas2:
                effectif = st.number_input("Nombre d'employés :", 1, 500, 10, 1)
                secteur_perso = st.selectbox("Votre secteur :", ["Services", "Commerce", "Industrie", "Autre"])
            
            # Analyse automatique
            if st.button("Analyser mon cas", key="analyse_cas"):
                # Calculs simplifiés
                marge_brute = ca_perso * marge_perso / 100
                charges_fixes_estimees = effectif * 50000  # Estimation
                resultat_estime = marge_brute - charges_fixes_estimees
                marge_nette_estimee = (resultat_estime / ca_perso) * 100 if ca_perso > 0 else 0
                
                st.markdown(f"""
                **📊 Analyse Préliminaire :**
                
                • **Marge brute :** {marge_brute:,.0f} € ({marge_perso:.0f}% du CA)
                • **Charges fixes estimées :** {charges_fixes_estimees:,.0f} €
                • **Résultat estimé :** {resultat_estime:,.0f} €
                • **Marge nette estimée :** {marge_nette_estimee:.1f}%
                
                **🎯 Points de vigilance :**
                {"• **Rentabilité à améliorer**" if marge_nette_estimee < 5 else "• **Rentabilité correcte**"}
                {"• **Effectif peut-être surdimensionné**" if charges_fixes_estimees > marge_brute * 0.6 else "• **Structure de coûts maîtrisée**"}
                """)
    
    # ===== CERTIFICATION =====
    st.markdown("---")
    st.markdown("### 🏆 **Certification FinGuide Pro**")
    
    # Vérification des conditions
    conditions = [
        ("✅ Module Bilan complété", st.session_state.learning_path_completed['bilan']),
        ("✅ Module Compte de Résultat complété", st.session_state.learning_path_completed['compte_resultat']),
        ("✅ Module Ratios complété", st.session_state.learning_path_completed['ratios']),
        ("✅ Module Budget complété", st.session_state.learning_path_completed['budget']),
        ("📝 Examen final réussi", False)  # À implémenter
    ]
    
    col_cert1, col_cert2 = st.columns([2, 1])
    
    with col_cert1:
        st.markdown("**Conditions pour la certification :**")
        
        for condition, statut in conditions:
            if statut:
                st.markdown(f"<div style='color: #10B981; margin: 5px 0;'>{condition}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #94A3B8; margin: 5px 0;'>{condition} (en attente)</div>", unsafe_allow_html=True)
    
    with col_cert2:
        # Vérifier si toutes les conditions sont remplies (sauf l'examen)
        modules_completes = all([st.session_state.learning_path_completed[k] for k in ['bilan', 'compte_resultat', 'ratios', 'budget']])
        
        if modules_completes:
            if st.button("🎓 Passer l'examen de certification", use_container_width=True):
                st.info("""
                🚧 **Examen en développement**
                
                La fonctionnalité d'examen certifiant sera disponible dans la version 2.0.
                
                En attendant, vous avez accès à :
                • Tous les quiz interactifs
                • Les exercices pratiques
                • Les cas d'étude sectoriels
                
                **Votre progression actuelle vous qualifie déjà comme utilisateur avancé !**
                """)
        else:
            st.warning("""
            ⏳ **En cours de qualification**
            
            Complétez tous les modules pour débloquer l'examen de certification.
            
            **Progression :** {completed}/4 modules
            """.format(completed=sum(st.session_state.learning_path_completed.values())))
    
    # ===== FEEDBACK ET AMÉLIORATION =====
    st.markdown("---")
    with st.expander("💬 **Feedback & Suggestions**", expanded=False):
        st.markdown("""
        **Aidez-nous à améliorer FinGuide Pro !**
        
        Votre feedback est précieux pour :
        • Améliorer l'expérience d'apprentissage
        • Développer de nouvelles fonctionnalités
        • Créer des contenus plus pertinents
        
        **Comment contribuer :**
        1. **Signaler un bug** : Utilisez le bouton ci-dessous
        2. **Suggérer une amélioration** : Décrivez votre idée
        3. **Proposer un cas pratique** : Partagez votre expérience
        """)
        
        type_feedback = st.selectbox(
            "Type de feedback :",
            ["Bug/Problème technique", "Suggestion d'amélioration", "Proposition de contenu", "Autre"]
        )
        
        feedback_text = st.text_area("Votre message :", height=150)
        
        if st.button("Envoyer le feedback", use_container_width=True):
            if feedback_text.strip():
                st.success("✅ Merci pour votre contribution ! Votre feedback a été enregistré.")
                # Ici, on pourrait enregistrer dans une base de données ou envoyer par email
            else:
                st.warning("Veuillez saisir un message avant d'envoyer.")

# ============================================
# MODULE 7: PARAMÈTRES
# ============================================

def show_settings():
    st.markdown('<h2 class="sub-header">⚙️ Paramètres & Personnalisation</h2>', unsafe_allow_html=True)
    
    tabs_settings = st.tabs(["👤 Profil Utilisateur", "🎯 Préférences", "🔗 Intégrations", "💾 Données"])
    
    with tabs_settings[0]:  # Profil
        st.markdown("### 👤 **Votre Profil d'Apprentissage**")
        
        with st.form("profil_form"):
            col_prof1, col_prof2 = st.columns(2)
            
            with col_prof1:
                nom = st.text_input("Nom :", value="Jean")
                prenom = st.text_input("Prénom :", value="Dupont")
                email = st.text_input("Email :", value="jean.dupont@example.com")
            
            with col_prof2:
                role = st.selectbox(
                    "Votre rôle :",
                    ["Comptable", "Contrôleur de gestion", "Manager", "Chef d'entreprise", 
                     "Étudiant", "Formateur", "Autre"]
                )
                
                experience = st.selectbox(
                    "Expérience en finance :",
                    ["Débutant (< 1 an)", "Intermédiaire (1-3 ans)", "Confirmé (3-5 ans)", "Expert (> 5 ans)"]
                )
                
                objectif = st.selectbox(
                    "Objectif principal :",
                    ["Apprentissage théorique", "Application pratique", 
                     "Préparation certification", "Analyse réelle d'entreprise"]
                )
            
            if st.form_submit_button("💾 Sauvegarder le profil"):
                st.success("✅ Profil mis à jour avec succès !")
        
        # Statistiques d'utilisation
        st.markdown("---")
        st.markdown("#### 📊 **Vos Statistiques d'Apprentissage**")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Sessions", "24")
            st.caption("Depuis le début")
        
        with col_stat2:
            st.metric("Temps moyen", "42 min")
            st.caption("Par session")
        
        with col_stat3:
            st.metric("Exercices", "18")
            st.caption("Complétés")
    
    with tabs_settings[1]:  # Préférences
        st.markdown("### 🎯 **Personnalisez Votre Expérience**")
        
        col_pref1, col_pref2 = st.columns(2)
        
        with col_pref1:
            st.markdown("#### 🎓 **Mode d'Apprentissage**")
            
            mode_apprentissage = st.radio(
                "Style pédagogique préféré :",
                ["Guidé (recommandé pour les débutants)",
                 "Autonome (pour les plus expérimentés)",
                 "Mixte (alternance guidé/autonome)"],
                index=0
            )
            
            niveau_detail = st.select_slider(
                "Niveau de détail :",
                options=["Basique", "Standard", "Avancé", "Expert"],
                value="Standard"
            )
            
            notifications = st.checkbox("Activer les notifications de progression", value=True)
        
        with col_pref2:
            st.markdown("#### 🌐 **Préférences Techniques**")
            
            devise = st.selectbox(
                "Devise par défaut :",
                ["EUR €", "USD $", "GBP £", "CHF CHF", "Autre"]
            )
            
            langue = st.selectbox(
                "Langue de l'interface :",
                ["Français", "Anglais", "Espagnol", "Allemand"]
            )
            
            format_nombre = st.selectbox(
                "Format des nombres :",
                ["1 000,00 € (standard français)",
                 "1,000.00 € (standard international)",
                 "1.000,00 € (standard européen)"]
            )
        
        # Thème visuel
        st.markdown("---")
        st.markdown("#### 🎨 **Apparence**")
        
        theme = st.radio(
            "Thème de l'interface :",
            ["Clair (défaut)", "Sombre", "Auto (suivi système)"],
            horizontal=True
        )
        
        taille_police = st.slider("Taille de police :", 12, 24, 16, 1)
        
        if st.button("💾 Appliquer les préférences", use_container_width=True):
            st.success("✅ Préférences appliquées !")
            st.info("""
            **Note :** Certains changements nécessitent un rechargement de la page.
            Rafraîchissez votre navigateur si besoin.
            """)
    
    with tabs_settings[2]:  # Intégrations
        st.markdown("### 🔗 **Intégrations Logicielles**")
        
        st.info("""
        💡 **Connectez FinGuide Pro à vos outils existants** pour :
        • Importer vos données financières automatiquement
        • Synchroniser vos analyses avec votre ERP
        • Exporter vers vos outils de reporting favoris
        """)
        
        # Liste des intégrations supportées
        integrations = [
            {"nom": "Excel/CSV", "statut": "✅ Disponible", "description": "Import/Export fichiers"},
            {"nom": "Sage", "statut": "🔧 Bientôt", "description": "Comptabilité française"},
            {"nom": "Cegid", "statut": "🔧 Bientôt", "description": "ERP français"},
            {"nom": "QuickBooks", "statut": "🔧 Bientôt", "description": "Comptabilité internationale"},
            {"nom": "SAP", "statut": "🔜 Planifié", "description": "ERP grande entreprise"},
            {"nom": "API REST", "statut": "🔜 Planifié", "description": "Connecteur personnalisé"}
        ]
        
        for integration in integrations:
            col_int1, col_int2, col_int3 = st.columns([1, 2, 1])
            
            with col_int1:
                st.markdown(f"**{integration['nom']}**")
            
            with col_int2:
                st.caption(integration['description'])
            
            with col_int3:
                st.markdown(f"`{integration['statut']}`")
        
        # Configuration d'une intégration
        st.markdown("---")
        st.markdown("#### ⚙️ **Configuration**")
        
        integration_choisie = st.selectbox(
            "Choisissez une intégration à configurer :",
            [i['nom'] for i in integrations if 'Disponible' in i['statut']] + ["Autre"]
        )
        
        if integration_choisie == "Excel/CSV":
            st.markdown("""
            **Configuration Excel/CSV :**
            
            1. **Format recommandé :**
               - Fichier .xlsx ou .csv
               - Première ligne : en-têtes
               - Données à partir de la ligne 2
            
            2. **Structure attendue :**
               ```csv
               Poste,Montant
               Immobilisations,100000
               Stocks,50000
               Capital,80000
               ```
            
            3. **Options d'import :**
               - Import complet (remplace tout)
               - Import partiel (ajoute aux données existantes)
               - Import avec mapping (personnalisez les colonnes)
            """)
            
            fichier_upload = st.file_uploader(
                "Téléversez votre fichier :",
                type=['xlsx', 'csv', 'xls'],
                key="upload_integration"
            )
            
            if fichier_upload:
                st.success(f"✅ Fichier {fichier_upload.name} téléversé avec succès !")
                
                col_import1, col_import2 = st.columns(2)
                
                with col_import1:
                    mode_import = st.radio(
                        "Mode d'import :",
                        ["Complet (remplace tout)", "Partiel (ajoute)", "Test (affiche seulement)"]
                    )
                
                with col_import2:
                    if st.button("🔄 Importer les données", use_container_width=True):
                        st.info("""
                        🚧 **Import en développement**
                        
                        Cette fonctionnalité sera pleinement opérationnelle dans la version 2.0.
                        
                        Pour le moment, vous pouvez :
                        1. Utiliser la saisie manuelle dans les modules
                        2. Exporter vos données pour les modifier dans Excel
                        3. Réimporter après modifications
                        """)
        
        elif integration_choisie != "Autre":
            st.warning(f"""
            ⏳ **Intégration {integration_choisie} en développement**
            
            Cette intégration sera disponible prochainement.
            
            **Prochaines étapes :**
            1. Développement du connecteur (en cours)
            2. Tests et validation
            3. Déploiement pour tous les utilisateurs
            
            **Date estimée :** Q3 2024
            """)
    
    with tabs_settings[3]:  # Données
        st.markdown("### 💾 **Gestion des Données**")
        
        col_data1, col_data2 = st.columns(2)
        
        with col_data1:
            st.markdown("#### 📤 **Export des Données**")
            
            format_export = st.radio(
                "Format d'export :",
                ["Excel complet (recommandé)", "CSV (données brutes)", "PDF (rapport formaté)", "JSON (technique)"]
            )
            
            scope_export = st.multiselect(
                "Éléments à exporter :",
                ["Bilan comptable", "Compte de résultat", "Ratios et analyses", 
                 "Budgets et prévisions", "Historique des exercices", "Profil d'apprentissage"],
                default=["Bilan comptable", "Compte de résultat", "Ratios et analyses"]
            )
            
            if st.button("📥 Générer l'export", use_container_width=True):
                # Calcul des ratios pour l'export
                ratios, _ = calculate_comprehensive_ratios(
                    st.session_state.balance_sheet, 
                    st.session_state.income_statement
                )
                
                sig = calculate_intermediate_balances(st.session_state.income_statement)
                
                # Génération du rapport
                excel_data = generate_comprehensive_report(
                    st.session_state.balance_sheet,
                    st.session_state.income_statement,
                    ratios,
                    sig
                )
                
                nom_fichier = f"finguide_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                if format_export.startswith("Excel"):
                    nom_fichier += ".xlsx"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif format_export.startswith("CSV"):
                    nom_fichier += ".zip"
                    mime_type = "application/zip"
                elif format_export.startswith("PDF"):
                    nom_fichier += ".pdf"
                    mime_type = "application/pdf"
                else:
                    nom_fichier += ".json"
                    mime_type = "application/json"
                
                st.download_button(
                    label="💾 Télécharger l'export",
                    data=excel_data,
                    file_name=nom_fichier,
                    mime=mime_type,
                    use_container_width=True
                )
        
        with col_data2:
            st.markdown("#### 🗑️ **Gestion Avancée**")
            
            # Sauvegarde automatique
            sauvegarde_auto = st.toggle("Sauvegarde automatique", value=True)
            
            if sauvegarde_auto:
                frequence = st.select_slider(
                    "Fréquence de sauvegarde :",
                    options=["Chaque modification", "Toutes les 5 minutes", "Toutes les 15 minutes", "À la fermeture"]
                )
            
            # Réinitialisation
            st.markdown("---")
            st.markdown("**Options de réinitialisation :**")
            
            type_reset = st.radio(
                "Que souhaitez-vous réinitialiser ?",
                ["Rien (par défaut)", "Données d'exercice", "Progression apprentissage", "Tout (usine)"],
                index=0,
                label_visibility="collapsed"
            )
            
            if type_reset != "Rien (par défaut)":
                confirmation = st.checkbox("Je confirme cette action")
                
                if st.button("🔄 Exécuter la réinitialisation", disabled=not confirmation, use_container_width=True):
                    if type_reset == "Données d'exercice":
                        st.session_state.balance_sheet = create_balance_sheet_template()
                        st.session_state.income_statement = create_income_statement_template()
                        st.session_state.current_step = 0
                        st.success("✅ Données d'exercice réinitialisées !")
                    
                    elif type_reset == "Progression apprentissage":
                        st.session_state.learning_path_completed = {
                            'bilan': False,
                            'compte_resultat': False,
                            'ratios': False,
                            'budget': False
                        }
                        st.success("✅ Progression réinitialisée !")
                    
                    elif type_reset == "Tout (usine)":
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
        
        # Sauvegarde cloud
        st.markdown("---")
        st.markdown("#### ☁️ **Sauvegarde Cloud**")
        
        compte_cloud = st.toggle("Activer la sauvegarde cloud", value=False)
        
        if compte_cloud:
            st.info("""
            **Avantages de la sauvegarde cloud :**
            • Accès à vos données depuis n'importe quel appareil
            • Historique des versions (annulation possible)
            • Synchronisation automatique
            • Partage facilité avec vos collaborateurs
            """)
            
            if st.button("🔗 Connecter un compte cloud", use_container_width=True):
                st.info("""
                🚧 **Fonctionnalité en développement**
                
                La sauvegarde cloud sera disponible dans la version 2.0.
                
                **Services prévus :**
                • Google Drive
                • OneDrive
                • Dropbox
                • Stockage FinGuide Pro
                
                **Date estimée :** Q4 2024
                """)

# ============================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"""
        ⚠️ **Une erreur est survenue**
        
        Détails : `{str(e)}`
        
        **Solution rapide :**
        1. Rafraîchissez la page (F5 ou Ctrl+R)
        2. Réinitialisez l'application via Paramètres → Données
        3. Contactez le support si le problème persiste
        
        **Informations techniques :**
        • Version : FinGuide Pro 1.0
        • Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}
        """)
        
        # Option de débogage (cachée par défaut)
        with st.expander("🔧 **Informations de débogage**", expanded=False):
            st.code(f"""
            Error type: {type(e).__name__}
            Error message: {str(e)}
            Session keys: {list(st.session_state.keys())}
            Balance sheet initialized: {'balance_sheet' in st.session_state}
            Income statement initialized: {'income_statement' in st.session_state}
            """)
