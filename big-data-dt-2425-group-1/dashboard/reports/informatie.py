import streamlit as st

# Pagina-titel
st.title("📘 Informatiepagina")
st.markdown(
    "Op deze pagina worden belangrijke begrippen en onderdelen van het dashboard toegelicht, "
    "zodat je snel kunt terugvinden wat iets betekent of waarvoor het dient."
)

st.divider()

# Materiaalsoorten
st.subheader("🔧 Materiaalsoorten")
st.markdown("De leidingen kunnen bestaan uit verschillende materialen. Hieronder vind je een overzicht van de afkortingen en toelichting per materiaal:")

materiaal_uitleg = {
    "GG": "Grijs Gietijzer – Robuust maar kwetsbaar voor breuk bij ouderdom.",
    "PVC": "Polyvinylchloride – Licht en goedkoop, maar gevoelig voor temperatuurveranderingen.",
    "GN": "Geplastificeerd Gietijzer – Verbeterde versie van GG met beschermende coating.",
    "BA": "Beton Asbest – Vroeger veel gebruikt, inmiddels verouderd en kwetsbaar.",
    "PE": "Polyethyleen – Flexibel en duurzaam, populair voor nieuwe installaties.",
    "K": "Koper – Corrosiebestendig, maar kostbaar en gevoelig voor diefstal.",
    "ST": "Staal – Zeer sterk, maar gevoelig voor roest zonder coating.",
    "AC": "Asbestcement – Vergelijkbaar met BA, maar minder gebruikt vanwege gezondheidsrisico’s."
}

for afkorting, uitleg in materiaal_uitleg.items():
    st.write(f"**{afkorting}** – {uitleg}")

st.markdown("*Let op: leidingen kunnen ook uit combinaties van materialen bestaan.*")

st.divider()

# Top 3 Redenen
st.subheader("📊 Top 3 redenen in het dashboard")
st.markdown("Het model toont per leiding de drie belangrijkste factoren die hebben geleid tot een verhoogde lekkagekans:")

redenen = {
    "dia": "Diameter van de leiding",
    "len": "Lengte van de leiding",
    "cor_protect": "Aanwezigheid van een beschermende coating",
    "mat": "Materiaalsoort van de leiding",
    "age": "Leeftijd van de leiding"
}

for code, uitleg in redenen.items():
    st.write(f"**{code}** – {uitleg}")

st.divider()

# Paginaoverzicht
st.subheader("📁 Pagina's in het dashboard")
st.markdown("Het dashboard bestaat uit vier pagina’s, elk met een eigen doel:")

st.markdown("""
1. **Home** – Uitleg over hoe het model werkt en hoe je het kunt interpreteren.  
2. **Voorspelling** – Geeft de voorspellingen van het model in een tabel weer, inclusief visualisaties op basis van die data.  
3. **Analyse** – Toont visualisaties op basis van ruwe data afkomstig van Waternet (niet bewerkt door het model).  
4. **Bijlagen** – Deze pagina met extra uitleg en definities.
""")

st.divider()

# Copyright en makers
st.subheader("👨‍💻 Makers & Copyright")
st.markdown("Dit project is gerealiseerd door vier studenten:")

studenten = ["Wesley Langelaan", "Jeroen Huiskes", "Graig Havelock", "Tatjana Volkova"]
for student in studenten:
    st.write(student)

st.markdown(
    "De data voor dit project is verstrekt door [Waternet](https://www.waternet.nl). "
    "Er is een geheimhoudingsverklaring (NDA) ondertekend waarin staat dat de data vertrouwelijk wordt behandeld "
    "en niet buiten dit project wordt gedeeld."
)
