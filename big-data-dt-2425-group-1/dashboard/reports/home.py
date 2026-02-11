import streamlit as st

# Bovenbalk met logo en titel
col1, col2 = st.columns([5, 5])
with col2:
    st.image("reports/Images/Logo_Waternet-blauw.png")
with col1:
    st.markdown("## 💧 Dashboard Waternet – Team 1")

st.markdown("---")  # Lijn onder header

# Over het model
st.markdown("### 👨🏼‍💻 Over het model")
st.markdown("""
Dit model is ontwikkeld in Python met behulp van het **XGBoost**-algoritme, een krachtige en efficiënte methode voor het maken van voorspellingen op basis van grote hoeveelheden data. 
Het model is specifiek getraind om te voorspellen of een waterleiding in de nabije toekomst lekkage zal vertonen.

Voor elke leiding wordt een risicoscore berekend, uitgedrukt als een percentage. Hoe hoger dit percentage, hoe groter de kans dat er een lekkage optreedt. 
Wanneer een leiding een kans van **60% of hoger** heeft om te lekken, wordt dit beschouwd als een **verhoogd risico**. Deze leidingen worden automatisch gemarkeerd 
en weergegeven in de tabel met voorspellingen, zodat ze extra aandacht kunnen krijgen bij inspectie of onderhoudsplanning.

Het model maakt gebruik van verschillende kenmerken van de leidingen, zoals materiaal, leeftijd, locatie en historische storingen, 
om zo een nauwkeurige inschatting te maken van het risico.
""")

st.divider()

# Hoe het model te interpreteren
st.markdown("### 🕵🏼‍♀️ Hoe het model te interpreteren")
st.markdown("""
De tabel met voorspellingen laat per leiding zien wat de kans is op een lekkage en welke factoren daarbij een rol spelen. 
Hieronder leggen we de betekenis van elke kolom uit, zodat je de uitkomsten eenvoudig kunt begrijpen:
""")

st.markdown("**📌 Kolommen in de tabel:**")
st.write("- **pipeid** – Uniek identificatienummer van een leiding.")
st.write("- **mat** – Het materiaal waarvan de leiding is gemaakt (bijv. PE, PVC, GG).")
st.write("- **age** – De leeftijd van de leiding, vanaf het jaar van aanleg tot nu (naar boven afgerond).")
st.write("- **probability** – De kans (in %) dat de leiding gaat lekken, berekend door het model.")
st.write("- **top_3_redenen** – De drie belangrijkste factoren die deze kans bepalen (bijv. diameter, lengte, leeftijd).")

st.markdown("**🚦 Risicocategorieën:**")
st.write("- **Hoog** – Kans ≥ 60% ⚠️")
st.write("- **Gemiddeld** – Kans tussen 10% en 59.99%")
st.write("- **Laag** – Kans < 10%")

st.markdown("""
Deze indeling helpt om snel te zien welke leidingen prioriteit moeten krijgen bij controle of vervanging.
""")