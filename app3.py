# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import io

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="FinGuide Pro", layout="wide")

st.title("📊 FinGuide Pro – Audit Financier & Contrôle de Gestion")

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("📂 Import des états financiers")

uploaded_file = st.sidebar.file_uploader("📥 Charger un fichier Excel", type=["xlsx"])

@st.cache_data
def load_data(file):
    return pd.read_excel(file, sheet_name=None)

data = None
if uploaded_file:
    data = load_data(uploaded_file)
else:
    st.sidebar.warning("Aucun fichier chargé. Utilisation d'un exemple de démonstration.")
    # Jeu de données fictif (simplifié)
    data = {
        "Bilan": pd.DataFrame({
            "Poste": ["Actif Circulant", "Actif Immobilisé", "Passif Circulant", "Capitaux Propres", "Dettes LT"],
            "Montant (€)": [60000, 100000, 50000, 70000, 40000]
        }),
        "Résultat": pd.DataFrame({
            "Poste": ["Chiffre d'affaires", "Résultat Net", "Charges Fixes"],
            "Montant (€)": [120000, 15000, 70000]
        })
    }

bilan_df = data["Bilan"]
resultat_df = data["Résultat"]

# ---------------------- ETAPE 1 : VISUALISATION BILAN ----------------------
st.header("📘 Structure du Bilan")

fig_bilan = px.pie(bilan_df, names="Poste", values="Montant (€)", title="Structure Bilan (Actif/Passif)")
st.plotly_chart(fig_bilan, use_container_width=True)

# ---------------------- ETAPE 2 : CALCUL DES RATIOS ----------------------

st.header("📈 Analyse Financière - Ratios Clés")

def calculate_ratios(bilan, resultat):
    ac = bilan.loc[bilan['Poste'] == "Actif Circulant", "Montant (€)"].values[0]
    ai = bilan.loc[bilan['Poste'] == "Actif Immobilisé", "Montant (€)"].values[0]
    pc = bilan.loc[bilan['Poste'] == "Passif Circulant", "Montant (€)"].values[0]
    cp = bilan.loc[bilan['Poste'] == "Capitaux Propres", "Montant (€)"].values[0]
    dt = bilan.loc[bilan['Poste'] == "Dettes LT", "Montant (€)"].values[0]
    ca = resultat.loc[resultat['Poste'] == "Chiffre d'affaires", "Montant (€)"].values[0]
    rn = resultat.loc[resultat['Poste'] == "Résultat Net", "Montant (€)"].values[0]

    total_actif = ac + ai
    total_passif = cp + pc + dt

    ratios = {
        "Ratio de Liquidité": round(ac / pc, 2),
        "Taux d'endettement": round((pc + dt) / total_actif * 100, 2),
        "ROA": round((rn / total_actif) * 100, 2),
        "Marge nette": round((rn / ca) * 100, 2)
    }

    return ratios, total_actif, total_passif

ratios, actif_total, passif_total = calculate_ratios(bilan_df, resultat_df)
st.metric("Total Actif", f"{actif_total:,.2f} €")
st.metric("Total Passif", f"{passif_total:,.2f} €")
st.warning("⚠️ Déséquilibre !" if abs(actif_total - passif_total) > 1 else "✅ Équilibré")

st.subheader("🔍 Ratios calculés")
for key, value in ratios.items():
    st.write(f"• **{key}** : {value}")

# ---------------------- ETAPE 3 : RECOMMANDATIONS ----------------------
st.header("🛠️ Recommandations Automatiques")

def generate_recommendations(ratios):
    recs = []
    if ratios["Ratio de Liquidité"] < 1:
        recs.append("❌ Liquidité insuffisante : améliorer les encaissements ou négocier les paiements.")
    if ratios["Taux d'endettement"] > 70:
        recs.append("❌ Endettement critique : limiter les dépenses ou rechercher des fonds propres.")
    if ratios["ROA"] < 5:
        recs.append("⚠️ Rentabilité faible : revoir l'efficacité des actifs.")
    if ratios["Marge nette"] < 10:
        recs.append("⚠️ Faible marge : optimiser les coûts ou augmenter les prix.")
    return recs

for r in generate_recommendations(ratios):
    st.error(r)

# ---------------------- ETAPE 4 : SIMULATEUR WHAT-IF ----------------------
st.header("🎲 Simulateur Économique (What-If)")

ca_input = st.number_input("Prévision Chiffre d'affaires (€)", value=120000)
marge_input = st.slider("Taux de Marge Brute (%)", 0.0, 100.0, 40.0)
charges_fixes = resultat_df.loc[resultat_df['Poste'] == "Charges Fixes", "Montant (€)"].values[0]

def simulate_result(ca, marge, charges):
    marge_brute = ca * (marge / 100)
    resultat = marge_brute - charges
    return resultat

scenarios = {
    "Optimiste": (1.1, 1.1),
    "Réaliste": (1.0, 1.0),
    "Pessimiste": (0.8, 0.9)
}

results = {}
for scen, (ca_mult, marge_mult) in scenarios.items():
    res = simulate_result(ca_input * ca_mult, marge_input * marge_mult, charges_fixes)
    results[scen] = res

st.subheader("📊 Résultats par Scénario")
st.bar_chart(results)

# ---------------------- ETAPE 5 : EXPORT RAPPORT ----------------------
st.header("📤 Export Excel")

def create_excel():
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        bilan_df.to_excel(writer, index=False, sheet_name='Bilan')
        resultat_df.to_excel(writer, index=False, sheet_name='Résultat')
        pd.DataFrame(ratios.items(), columns=["Ratio", "Valeur"]).to_excel(writer, index=False, sheet_name='Ratios')
    return output.getvalue()

if st.button("📥 Télécharger le rapport Excel"):
    excel_file = create_excel()
    st.download_button("📤 Télécharger", data=excel_file, file_name="rapport_finguide.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------------- CONTRÔLE INTERNE (Place Holder) ----------------------
st.sidebar.title("🛡️ Contrôle Interne")
st.sidebar.write("🔒 Module à venir : audit des procédures, séparation des tâches, etc.")
