"""
FinGuide Pro - Application d'Audit Financier et Contrôle de Gestion
Auteur: Expert Audit
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import des modules internes
from modules.data_import import FinancialDataImporter
from modules.ratio_analysis import RatioAnalyzer
from modules.risk_detection import RiskDetector
from modules.recommendations import RecommendationEngine
from modules.whatif_simulator import WhatIfSimulator
from modules.visualization import FinancialVisualizer
from modules.reporting import ReportGenerator
from modules.internal_control import InternalControlModule
from modules.tutorials import TutorialManager

# Configuration de la page
st.set_page_config(
    page_title="FinGuide Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FinGuidePro:
    """Classe principale de l'application FinGuide Pro"""
    
    def __init__(self):
        self.init_session_state()
        self.setup_sidebar()
        
    def init_session_state(self):
        """Initialise les variables de session"""
        session_defaults = {
            'financial_data': None,
            'balance_sheet': None,
            'income_statement': None,
            'cash_flow': None,
            'ratios': None,
            'risks': None,
            'recommendations': None,
            'current_step': 1,
            'company_info': {},
            'whatif_scenarios': None
        }
        
        for key, value in session_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def setup_sidebar(self):
        """Configure la barre latérale"""
        with st.sidebar:
            st.image("https://via.placeholder.com/200x60/1E3A8A/FFFFFF?text=FinGuide+Pro", 
                    use_column_width=True)
            
            st.title("🔍 Navigation")
            
            # Navigation par étapes
            steps = {
                1: "🏢 1. Informations Société",
                2: "📥 2. Import des Données",
                3: "📊 3. Analyse des Ratios",
                4: "⚠️  4. Détection des Risques",
                5: "💡 5. Recommandations",
                6: "🔮 6. Simulateur What-If",
                7: "📈 7. Visualisations",
                8: "🏛️  8. Contrôle Interne",
                9: "📄 9. Rapport Final"
            }
            
            selected_step = st.selectbox(
                "Étapes d'audit",
                options=list(steps.keys()),
                format_func=lambda x: steps[x],
                index=st.session_state.get('current_step', 1) - 1
            )
            
            st.session_state.current_step = selected_step
            
            # Section d'aide rapide
            st.divider()
            with st.expander("❓ Aide Rapide"):
                st.info("""
                **Conseils d'utilisation:**
                1. Commencez par importer vos états financiers
                2. Analysez les ratios automatiquement calculés
                3. Consultez les risques détectés
                4. Explorez les recommandations
                5. Testez des scénarios avec le simulateur
                """)
            
            # Téléchargement de template
            st.divider()
            st.download_button(
                label="📋 Template Excel",
                data=self.get_excel_template(),
                file_name="template_finguide.xlsx",
                mime="application/vnd.ms-excel"
            )
            
            # Informations de version
            st.divider()
            st.caption("FinGuide Pro v1.0 • © 2024")
    
    def get_excel_template(self):
        """Génère un template Excel pour l'importation"""
        # Code simplifié - en production, utiliser openpyxl
        return b"Template content"
    
    def run(self):
        """Exécute l'application en fonction de l'étape sélectionnée"""
        step = st.session_state.current_step
        
        # Header principal
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.title("FinGuide Pro")
        with col2:
            st.subheader("Audit Financier & Contrôle de Gestion Intelligent")
        with col3:
            if st.session_state.financial_data:
                st.success("✅ Données chargées")
        
        # Exécution de l'étape sélectionnée
        if step == 1:
            self.step_company_info()
        elif step == 2:
            self.step_data_import()
        elif step == 3:
            self.step_ratio_analysis()
        elif step == 4:
            self.step_risk_detection()
        elif step == 5:
            self.step_recommendations()
        elif step == 6:
            self.step_whatif_simulator()
        elif step == 7:
            self.step_visualizations()
        elif step == 8:
            self.step_internal_control()
        elif step == 9:
            self.step_final_report()
    
    def step_company_info(self):
        """Étape 1: Informations sur la société"""
        st.header("🏢 Informations de la Société")
        
        with st.form("company_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.session_state.company_info['name'] = st.text_input(
                    "Nom de l'entreprise",
                    value=st.session_state.company_info.get('name', '')
                )
                st.session_state.company_info['sector'] = st.selectbox(
                    "Secteur d'activité",
                    options=['Industrie', 'Services', 'Commerce', 'Technologie', 'Autre']
                )
                st.session_state.company_info['size'] = st.selectbox(
                    "Taille de l'entreprise",
                    options=['TPE (<20 salariés)', 'PME (20-250)', 'ETI (250-5000)', 'Grande Entreprise (>5000)']
                )
            
            with col2:
                st.session_state.company_info['currency'] = st.selectbox(
                    "Devise",
                    options=['EUR', 'USD', 'GBP', 'CHF', 'Autre']
                )
                st.session_state.company_info['fiscal_year'] = st.number_input(
                    "Année fiscale",
                    min_value=2000,
                    max_value=2030,
                    value=datetime.now().year - 1
                )
                st.session_state.company_info['country'] = st.text_input(
                    "Pays",
                    value="France"
                )
            
            if st.form_submit_button("Enregistrer les informations"):
                st.success("Informations enregistrées avec succès!")
                st.rerun()
    
    def step_data_import(self):
        """Étape 2: Importation des données financières"""
        st.header("📥 Importation des États Financiers")
        
        # Initialisation de l'importateur
        importer = FinancialDataImporter()
        
        # Onglets pour différents modes d'importation
        tab1, tab2, tab3 = st.tabs(["📊 Import Manuel", "📁 Fichier Excel", "🔄 Synchronisation"])
        
        with tab1:
            st.subheader("Saisie Manuelle des Données")
            
            with st.expander("📋 Bilan", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**ACTIF**")
                    actif_circulant = st.number_input(
                        "Actif Circulant (k€)", 
                        min_value=0.0,
                        value=500.0,
                        help="Stocks + Créances + Trésorerie"
                    )
                    actif_immobilise = st.number_input(
                        "Actif Immobilisé (k€)",
                        min_value=0.0,
                        value=1000.0,
                        help="Immobilisations corporelles, incorporelles, financières"
                    )
                    total_actif = actif_circulant + actif_immobilise
                    st.metric("Total ACTIF", f"{total_actif:,.0f} k€")
                
                with col2:
                    st.markdown("**PASSIF**")
                    capitaux_propres = st.number_input(
                        "Capitaux Propres (k€)",
                        min_value=0.0,
                        value=800.0
                    )
                    dettes_financieres = st.number_input(
                        "Dettes Financières (k€)",
                        min_value=0.0,
                        value=400.0
                    )
                    dettes_exploitation = st.number_input(
                        "Dettes d'Exploitation (k€)",
                        min_value=0.0,
                        value=300.0
                    )
                    total_passif = capitaux_propres + dettes_financieres + dettes_exploitation
                    st.metric("Total PASSIF", f"{total_passif:,.0f} k€")
                
                # Vérification de l'équilibre
                if abs(total_actif - total_passif) > 0.1:
                    st.error(f"⚠️ Déséquilibre du bilan: {total_actif - total_passif:,.2f} k€")
                else:
                    st.success("✅ Bilan équilibré")
            
            with st.expander("📈 Compte de Résultat"):
                chiffre_affaires = st.number_input(
                    "Chiffre d'Affaires (k€)",
                    min_value=0.0,
                    value=2000.0
                )
                achats_consommes = st.number_input(
                    "Achats Consommés (k€)",
                    min_value=0.0,
                    value=1200.0
                )
                charges_personnel = st.number_input(
                    "Charges de Personnel (k€)",
                    min_value=0.0,
                    value=400.0
                )
                autres_charges = st.number_input(
                    "Autres Charges (k€)",
                    min_value=0.0,
                    value=200.0
                )
                
                resultat_exploitation = chiffre_affaires - achats_consommes - charges_personnel - autres_charges
                st.metric("Résultat d'Exploitation", f"{resultat_exploitation:,.0f} k€")
            
            if st.button("Valider les données saisies"):
                # Création d'un dictionnaire de données
                data = {
                    'balance_sheet': {
                        'actif_circulant': actif_circulant,
                        'actif_immobilise': actif_immobilise,
                        'total_actif': total_actif,
                        'capitaux_propres': capitaux_propres,
                        'dettes_financieres': dettes_financieres,
                        'dettes_exploitation': dettes_exploitation,
                        'total_passif': total_passif
                    },
                    'income_statement': {
                        'chiffre_affaires': chiffre_affaires,
                        'achats_consommes': achats_consommes,
                        'charges_personnel': charges_personnel,
                        'autres_charges': autres_charges,
                        'resultat_exploitation': resultat_exploitation
                    }
                }
                
                st.session_state.financial_data = data
                st.success("Données enregistrées avec succès!")
        
        with tab2:
            st.subheader("Import depuis un fichier Excel")
            
            uploaded_file = st.file_uploader(
                "Choisissez un fichier Excel",
                type=['xlsx', 'xls'],
                help="Format attendu: onglets 'Bilan', 'Compte de Resultat', 'Cash Flow'"
            )
            
            if uploaded_file:
                try:
                    data = importer.import_excel(uploaded_file)
                    st.session_state.financial_data = data
                    st.success("✅ Fichier importé avec succès!")
                    
                    # Aperçu des données
                    with st.expander("Aperçu des données importées"):
                        st.write("**Bilan:**")
                        st.dataframe(pd.DataFrame([data['balance_sheet']]))
                        
                        st.write("**Compte de résultat:**")
                        st.dataframe(pd.DataFrame([data['income_statement']]))
                
                except Exception as e:
                    st.error(f"Erreur lors de l'import: {str(e)}")
        
        with tab3:
            st.subheader("Synchronisation avec logiciels comptables")
            st.info("Fonctionnalité en développement")
    
    def step_ratio_analysis(self):
        """Étape 3: Analyse des ratios financiers"""
        st.header("📊 Analyse des Ratios Financiers")
        
        if not st.session_state.financial_data:
            st.warning("Veuillez d'abord importer des données financières.")
            return
        
        # Initialisation de l'analyseur
        analyzer = RatioAnalyzer(st.session_state.financial_data)
        ratios = analyzer.calculate_all_ratios()
        st.session_state.ratios = ratios
        
        # Affichage des ratios par catégorie
        tabs = st.tabs(["📈 Rentabilité", "💧 Liquidité", "🏛️  Solvabilité", "⚙️  Activité", "📋 Synthèse"])
        
        with tabs[0]:  # Rentabilité
            col1, col2, col3 = st.columns(3)
            
            with col1:
                roe = ratios.get('roe', 0) * 100
                color = "green" if roe > 10 else "orange" if roe > 5 else "red"
                st.metric(
                    "ROE (Return on Equity)",
                    f"{roe:.1f}%",
                    delta=f"{'Bon' if roe > 10 else 'Moyen' if roe > 5 else 'Faible'}",
                    delta_color=color
                )
                st.caption("Rentabilité des capitaux propres")
            
            with col2:
                roa = ratios.get('roa', 0) * 100
                color = "green" if roa > 5 else "orange" if roa > 3 else "red"
                st.metric(
                    "ROA (Return on Assets)",
                    f"{roa:.1f}%",
                    delta_color=color
                )
                st.caption("Rentabilité de l'actif total")
            
            with col3:
                ros = ratios.get('ros', 0) * 100
                color = "green" if ros > 10 else "orange" if ros > 5 else "red"
                st.metric(
                    "ROS (Return on Sales)",
                    f"{ros:.1f}%",
                    delta_color=color
                )
                st.caption("Marge nette sur ventes")
        
        with tabs[1]:  # Liquidité
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current = ratios.get('current_ratio', 0)
                color = "green" if 1.5 <= current <= 2.5 else "orange" if 1 <= current < 1.5 else "red"
                st.metric(
                    "Ratio de Liquidité Générale",
                    f"{current:.2f}",
                    delta="Idéal: 1.5-2.5",
                    delta_color=color
                )
                st.caption("Actif circulant / Dettes CT")
            
            with col2:
                quick = ratios.get('quick_ratio', 0)
                color = "green" if quick >= 1 else "orange" if quick >= 0.5 else "red"
                st.metric(
                    "Ratio de Liquidité Réduite",
                    f"{quick:.2f}",
                    delta="Minimum: 1",
                    delta_color=color
                )
                st.caption("(Actif circ. - Stocks) / Dettes CT")
            
            with col3:
                cash_ratio = ratios.get('cash_ratio', 0)
                st.metric(
                    "Ratio de Trésorerie",
                    f"{cash_ratio:.2f}"
                )
                st.caption("Trésorerie / Dettes CT")
        
        with tabs[2]:  # Solvabilité
            col1, col2 = st.columns(2)
            
            with col1:
                debt_ratio = ratios.get('debt_ratio', 0) * 100
                color = "green" if debt_ratio < 50 else "orange" if debt_ratio < 70 else "red"
                st.metric(
                    "Taux d'Endettement",
                    f"{debt_ratio:.1f}%",
                    delta_color=color
                )
                st.caption("Dettes / Capitaux propres")
            
            with col2:
                financial_leverage = ratios.get('financial_leverage', 0)
                st.metric(
                    "Effet de Levier Financier",
                    f"{financial_leverage:.2f}"
                )
                st.caption("Actif total / Capitaux propres")
        
        with tabs[3]:  # Activité
            col1, col2 = st.columns(2)
            
            with col1:
                asset_turnover = ratios.get('asset_turnover', 0)
                st.metric(
                    "Rotation de l'Actif",
                    f"{asset_turnover:.2f}"
                )
                st.caption("CA / Actif total")
            
            with col2:
                bfr_days = ratios.get('bfr_days', 0)
                color = "green" if bfr_days < 60 else "orange" if bfr_days < 90 else "red"
                st.metric(
                    "BFR (en jours)",
                    f"{bfr_days:.0f} j",
                    delta_color=color
                )
                st.caption("Besoin en Fonds de Roulement")
        
        with tabs[4]:  # Synthèse
            # Graphique radar des ratios
            vis = FinancialVisualizer()
            fig = vis.create_radar_chart(ratios)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau synthétique
            df_ratios = pd.DataFrame({
                'Ratio': list(ratios.keys()),
                'Valeur': list(ratios.values()),
                'Seuil Min': [0.1, 1.0, 0.5, 0, 0.05, 0, 0.3, 0.5],
                'Seuil Max': [0.2, 2.5, 1.5, 2.0, 0.15, 1.5, 0.7, 1.0]
            })
            st.dataframe(df_ratios, use_container_width=True)
    
    def step_risk_detection(self):
        """Étape 4: Détection des risques et déséquilibres"""
        st.header("⚠️ Détection des Risques Financiers")
        
        if not st.session_state.financial_data or not st.session_state.ratios:
            st.warning("Veuillez d'abord effectuer l'analyse des ratios.")
            return
        
        # Initialisation du détecteur de risques
        detector = RiskDetector(
            st.session_state.financial_data,
            st.session_state.ratios
        )
        
        risks = detector.detect_all_risks()
        st.session_state.risks = risks
        
        # Affichage des risques par catégorie
        risk_categories = {
            'critical': "🔴 Critiques",
            'warning': "🟠 Avertissements",
            'info': "🔵 Informations"
        }
        
        for category, title in risk_categories.items():
            if risks.get(category):
                with st.expander(f"{title} ({len(risks[category])})", 
                               expanded=category=='critical'):
                    for risk in risks[category]:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{risk['title']}**")
                            st.markdown(f"{risk['description']}")
                            
                            if risk.get('impact'):
                                st.progress(min(risk['impact']/100, 1.0))
                                st.caption(f"Impact: {risk['impact']}/100")
                        
                        with col2:
                            if st.button("💡", key=f"btn_{risk['id']}"):
                                st.session_state[f"show_detail_{risk['id']}"] = \
                                    not st.session_state.get(f"show_detail_{risk['id']}", False)
                        
                        if st.session_state.get(f"show_detail_{risk['id']}", False):
                            with st.container(border=True):
                                st.markdown("**Recommandation détaillée:**")
                                st.markdown(risk.get('recommendation', 'Non disponible'))
                                st.markdown(f"**Secteur concerné:** {risk.get('sector', 'Général')}")
        
        # KPI de risque global
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            critical_count = len(risks.get('critical', []))
            st.metric(
                "Risques Critiques",
                critical_count,
                delta="À traiter en priorité" if critical_count > 0 else None,
                delta_color="inverse"
            )
        
        with col2:
            warning_count = len(risks.get('warning', []))
            st.metric(
                "Risques Moyens",
                warning_count
            )
        
        with col3:
            risk_score = detector.calculate_risk_score()
            st.metric(
                "Score de Risque Global",
                f"{risk_score}/100",
                delta="Élevé" if risk_score > 70 else "Modéré" if risk_score > 40 else "Faible",
                delta_color="inverse" if risk_score > 70 else "normal"
            )
    
    def step_recommendations(self):
        """Étape 5: Recommandations correctives"""
        st.header("💡 Recommandations Correctives")
        
        if not st.session_state.risks:
            st.warning("Veuillez d'abord effectuer la détection des risques.")
            return
        
        # Initialisation du moteur de recommandations
        recommender = RecommendationEngine(
            st.session_state.financial_data,
            st.session_state.ratios,
            st.session_state.risks
        )
        
        recommendations = recommender.generate_recommendations()
        st.session_state.recommendations = recommendations
        
        # Affichage des recommandations par priorité
        priorities = {
            'high': "🔥 Haute Priorité",
            'medium': "⚡ Priorité Moyenne",
            'low': "📋 Priorité Basse"
        }
        
        for priority, title in priorities.items():
            if recommendations.get(priority):
                with st.expander(f"{title} ({len(recommendations[priority])})"):
                    for rec in recommendations[priority]:
                        with st.container(border=True):
                            cols = st.columns([3, 1])
                            with cols[0]:
                                st.markdown(f"### {rec['title']}")
                                st.markdown(f"**Objectif:** {rec['objective']}")
                                st.markdown(f"**Actions:**")
                                for action in rec['actions']:
                                    st.markdown(f"- {action}")
                                
                                if rec.get('expected_impact'):
                                    st.markdown(f"**Impact attendu:** {rec['expected_impact']}")
                            
                            with cols[1]:
                                # Édition de la recommandation
                                with st.popover("✏️ Personnaliser"):
                                    custom_action = st.text_area(
                                        "Ajouter une action personnalisée",
                                        key=f"custom_{rec['id']}"
                                    )
                                    if st.button("Ajouter", key=f"add_{rec['id']}"):
                                        if custom_action:
                                            rec['actions'].append(custom_action)
                                            st.success("Action ajoutée!")
                                
                                # Suivi de mise en œuvre
                                status = st.selectbox(
                                    "Statut",
                                    ["Non démarré", "En cours", "Terminé"],
                                    key=f"status_{rec['id']}"
                                )
                                st.progress(
                                    0 if status == "Non démarré" 
                                    else 50 if status == "En cours" 
                                    else 100
                                )
        
        # Plan d'action global
        st.divider()
        st.subheader("📋 Plan d'Action Global")
        
        if st.button("📥 Générer le Plan d'Action"):
            action_plan = recommender.generate_action_plan()
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Télécharger en Excel",
                    data=action_plan.to_excel(index=False),
                    file_name="plan_action.xlsx",
                    mime="application/vnd.ms-excel"
                )
            
            with col2:
                st.download_button(
                    label="Télécharger en PDF",
                    data=b"PDF content",  # À remplacer par la génération PDF réelle
                    file_name="plan_action.pdf",
                    mime="application/pdf"
                )
    
    def step_whatif_simulator(self):
        """Étape 6: Simulateur What-If"""
        st.header("🔮 Simulateur de Scénarios What-If")
        
        if not st.session_state.financial_data:
            st.warning("Veuillez d'abord importer des données financières.")
            return
        
        # Initialisation du simulateur
        simulator = WhatIfSimulator(st.session_state.financial_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Paramètres du Scénario")
            
            # Variables modifiables
            with st.form("scenario_form"):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    ca_change = st.slider(
                        "Variation du CA (%)",
                        min_value=-30,
                        max_value=30,
                        value=0,
                        step=5
                    )
                    margin_change = st.slider(
                        "Variation de la marge (%)",
                        min_value=-5,
                        max_value=5,
                        value=0,
                        step=1
                    )
                
                with col_b:
                    cost_reduction = st.slider(
                        "Réduction des coûts (%)",
                        min_value=0,
                        max_value=20,
                        value=0,
                        step=2
                    )
                    inventory_days = st.slider(
                        "Jours de stock (cible)",
                        min_value=30,
                        max_value=120,
                        value=60,
                        step=10
                    )
                
                with col_c:
                    payment_terms = st.slider(
                        "Délai clients (jours)",
                        min_value=30,
                        max_value=120,
                        value=60,
                        step=10
                    )
                    debt_ratio_target = st.slider(
                        "Ratio d'endettement cible (%)",
                        min_value=0,
                        max_value=100,
                        value=50,
                        step=5
                    )
                
                if st.form_submit_button("🚀 Lancer la Simulation"):
                    scenario_params = {
                        'ca_change': ca_change,
                        'margin_change': margin_change,
                        'cost_reduction': cost_reduction,
                        'inventory_days': inventory_days,
                        'payment_terms': payment_terms,
                        'debt_ratio_target': debt_ratio_target
                    }
                    
                    results = simulator.run_scenarios(scenario_params)
                    st.session_state.whatif_scenarios = results
        
        with col2:
            st.subheader("Scénarios Prédéfinis")
            
            if st.button("📉 Scénario Pessimiste", use_container_width=True):
                st.session_state.whatif_scenarios = simulator.run_pessimistic_scenario()
            
            if st.button("📊 Scénario Réaliste", use_container_width=True):
                st.session_state.whatif_scenarios = simulator.run_realistic_scenario()
            
            if st.button("📈 Scénario Optimiste", use_container_width=True):
                st.session_state.whatif_scenarios = simulator.run_optimistic_scenario()
        
        # Affichage des résultats
        if st.session_state.whatif_scenarios:
            st.divider()
            st.subheader("📊 Résultats des Simulations")
            
            # Graphique comparatif
            vis = FinancialVisualizer()
            fig = vis.create_scenario_comparison(st.session_state.whatif_scenarios)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau des impacts
            st.dataframe(
                pd.DataFrame(st.session_state.whatif_scenarios['comparison']),
                use_container_width=True
            )
    
    def step_visualizations(self):
        """Étape 7: Visualisations graphiques"""
        st.header("📈 Visualisations Financières")
        
        if not st.session_state.financial_data:
            st.warning("Veuillez d'abord importer des données financières.")
            return
        
        # Initialisation du visualiseur
        vis = FinancialVisualizer(st.session_state.financial_data)
        
        # Sélection du type de visualisation
        viz_type = st.selectbox(
            "Type de visualisation",
            [
                "Structure du Bilan",
                "Évolution des Ratios",
                "Analyse Sectorielle",
                "Cartographie des Risques",
                "Tableau de Bord Intégré"
            ]
        )
        
        if viz_type == "Structure du Bilan":
            col1, col2 = st.columns(2)
            
            with col1:
                fig = vis.create_balance_sheet_sunburst()
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = vis.create_balance_composition_chart()
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Évolution des Ratios":
            fig = vis.create_ratio_trend_chart(st.session_state.ratios)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Cartographie des Risques":
            if st.session_state.risks:
                fig = vis.create_risk_heatmap(st.session_state.risks)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Aucun risque détecté pour la visualisation")
        
        elif viz_type == "Tableau de Bord Intégré":
            # Création d'un dashboard avec plusieurs graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                fig = vis.create_kpi_gauges(st.session_state.ratios)
                st.plotly_chart(fig, use_container_width=True)
                
                fig = vis.create_cash_flow_waterfall()
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = vis.create_profitability_pyramid()
                st.plotly_chart(fig, use_container_width=True)
                
                if st.session_state.recommendations:
                    fig = vis.create_recommendation_timeline(st.session_state.recommendations)
                    st.plotly_chart(fig, use_container_width=True)
    
    def step_internal_control(self):
        """Étape 8: Module de contrôle interne"""
        st.header("🏛️ Contrôle Interne")
        
        # Initialisation du module
        ic_module = InternalControlModule()
        
        # Évaluation par domaine
        domains = ic_module.get_control_domains()
        
        for domain in domains:
            with st.expander(f"{domain['icon']} {domain['name']}", expanded=True):
                st.markdown(f"**Description:** {domain['description']}")
                
                # Évaluation des contrôles
                for control in domain['controls']:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{control['name']}**")
                        st.caption(control['description'])
                    
                    with col2:
                        status = st.selectbox(
                            "État",
                            ["Non applicable", "Défaillant", "Partiel", "Efficace"],
                            key=f"status_{control['id']}"
                        )
                    
                    with col3:
                        if st.button("📋", key=f"btn_{control['id']}"):
                            st.session_state[f"detail_{control['id']}"] = True
                        
                        if st.session_state.get(f"detail_{control['id']}"):
                            with st.popover("Recommandation"):
                                st.markdown(control['recommendation'])
                                if st.text_area("Commentaire", key=f"comment_{control['id']}"):
                                    if st.button("Enregistrer", key=f"save_{control['id']}"):
                                        st.success("Commentaire enregistré")
                
                # Score du domaine
                st.progress(domain.get('score', 0) / 100)
                st.caption(f"Score: {domain.get('score', 0)}/100")
        
        # Rapport de contrôle interne
        st.divider()
        if st.button("📊 Générer le Rapport de Contrôle Interne"):
            report = ic_module.generate_report()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score Global", f"{report['overall_score']}/100")
                st.metric("Points Forts", report['strengths_count'])
            with col2:
                st.metric("Domaines à Améliorer", report['weaknesses_count'])
                st.metric("% de Conformité", f"{report['compliance_rate']}%")
            
            # Téléchargement du rapport
            st.download_button(
                "📥 Télécharger le Rapport",
                data=report['content'],
                file_name="rapport_controle_interne.pdf"
            )
    
    def step_final_report(self):
        """Étape 9: Rapport final"""
        st.header("📄 Rapport d'Audit Final")
        
        if not all([st.session_state.financial_data, 
                   st.session_state.ratios, 
                   st.session_state.risks]):
            st.warning("Veuillez compléter toutes les étapes précédentes.")
            return
        
        # Initialisation du générateur de rapports
        report_gen = ReportGenerator(
            company_info=st.session_state.company_info,
            financial_data=st.session_state.financial_data,
            ratios=st.session_state.ratios,
            risks=st.session_state.risks,
            recommendations=st.session_state.recommendations
        )
        
        # Aperçu du rapport
        st.subheader("Aperçu du Rapport")
        
        tabs = st.tabs(["Résumé Exécutif", "Analyse Détaillée", "Annexes"])
        
        with tabs[0]:
            st.markdown(report_gen.generate_executive_summary())
        
        with tabs[1]:
            st.markdown(report_gen.generate_detailed_analysis())
        
        with tabs[2]:
            st.dataframe(pd.DataFrame([st.session_state.ratios]), use_container_width=True)
            if st.session_state.whatif_scenarios:
                st.write("Scénarios What-If:", st.session_state.whatif_scenarios)
        
        # Options d'export
        st.divider()
        st.subheader("📤 Export du Rapport")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Générer Rapport Excel", use_container_width=True):
                excel_report = report_gen.generate_excel_report()
                st.download_button(
                    label="⬇️ Télécharger Excel",
                    data=excel_report,
                    file_name="rapport_audit.xlsx",
                    mime="application/vnd.ms-excel"
                )
        
        with col2:
            if st.button("📄 Générer Rapport PDF", use_container_width=True):
                pdf_report = report_gen.generate_pdf_report()
                st.download_button(
                    label="⬇️ Télécharger PDF",
                    data=pdf_report,
                    file_name="rapport_audit.pdf",
                    mime="application/pdf"
                )
        
        with col3:
            if st.button("📋 Générer Présentation", use_container_width=True):
                st.info("Fonctionnalité en développement")

def main():
    """Fonction principale"""
    app = FinGuidePro()
    app.run()

if __name__ == "__main__":
    main()