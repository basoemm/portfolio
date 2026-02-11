import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import numpy as np
import os

# Verbinden met database
db_user = os.getenv("user")
db_password = os.getenv("password")
db_host = os.getenv("host")

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/waternet')

# Alle leidingen:
df_pipes = pd.read_csv('Data/pipes_utilb_std.csv')

df_pipes['inst_date'] = df_pipes['inst_date'].replace(0, np.nan)
df_pipes['rehab_date'] = df_pipes['rehab_date'].replace(0, np.nan)
df_pipes['rem_date'] = df_pipes['rem_date'].replace(0, np.nan)

df_pipes['inst_date'] = pd.to_datetime(df_pipes['inst_date'], format='%Y')
df_pipes['rehab_date'] = pd.to_datetime(df_pipes['rehab_date'], format='%Y')
df_pipes['rem_date'] = pd.to_datetime(df_pipes['rem_date'], format='%Y')
df_pipes = df_pipes.drop(['dataset'], axis=1)
df_pipes.to_sql(name='pipes_original', con=engine, if_exists='fail', index=False)

# Alle actieve
df_active_pipes = df_pipes.loc[lambda df: df['active'] == True]


df2 = pd.read_csv('data/breaks_utilb_pipeid_match.csv')
df2['brid'] = df2['brid'].str.replace(',', '', regex=True)
df2['brid'] = pd.to_numeric(df2['brid'])
df2 = df2.drop(['dataset'], axis= 1)
df2.to_sql(name='breaks_pipes_match_original', con=engine, if_exists='fail', index=False)

df_with_id = pd.merge(df2, df_pipes, on='pipeid', how='inner')


df3 = pd.read_csv('data/breaks_utilb_csv3.csv')
df3['date'] = pd.to_datetime(df3['date'], format='%m/%d/%y')
df3['brid'] = df3['brid'].str.replace(',', '', regex=True)
df3['brid'] = pd.to_numeric(df3['brid'])
df3.to_sql(name='breaks_original', con=engine, if_exists='fail', index=False)


# Inner join de storing df met pipes DF
df_with_breaks = pd.merge(df_with_id, df3, on='brid', how='inner')

# converteer datum van storing naar datum type:
df_with_breaks['date'] = pd.to_datetime(df_with_breaks['date'], format='%m/%d/%y')

# Kolommen verwijderen die niet belangrijk lijken:
df_with_breaks = df_with_breaks.drop(['brid', 'col_0', 'dataset_x', 'dataset_y', 'loc1_x', 'owner', 'Nummer afhandeling (Afhandeling)' ,'loc1_y'], axis=1)

# Leidinginen met onbekende installatiedatum verwijderen
df_with_breaks = df_with_breaks[df_with_breaks['inst_date'] != 0]


# Aannames, leeg is geen: 
df_with_breaks['cor_protect'] = df_with_breaks['cor_protect'].fillna('Geen')
df_with_breaks['lining'] = df_with_breaks['lining'].fillna('Geen')

df_with_breaks['manufacturer'] = df_with_breaks['manufacturer'].fillna('onbekend')

# Drop velden met missende waardes:
df_with_breaks = df_with_breaks.dropna()

# Duplicates verwijderen:
df_with_breaks = df_with_breaks.drop_duplicates()

# Converteer naar datum:
df_with_breaks['inst_date'] = pd.to_datetime(df_with_breaks['inst_date'], format='%Y')
df_with_breaks['rehab_date'] = pd.to_datetime(df_with_breaks['inst_date'], format='%Y')
df_with_breaks['rem_date'] = pd.to_datetime(df_with_breaks['inst_date'], format='%Y')

# To SQL:
#df_with_breaks.to_sql(name='breaks_cleaned2', con=engine, if_exists='fail', index=False)
query = """SELECT year(inst_date) as Installatiedatum, count(*) as Aantal FROM waternet.breaks_original a
inner join waternet.breaks_pipes_match_original b on a.brid = b.brid
inner join waternet.pipes_original c on b.pipeid = c.pipeid
where inst_date is not null
group by Installatiedatum
order by Installatiedatum"""

df4 = pd.read_sql(query, con=engine)
df4 = df4.set_index('Installatiedatum')

# data = {'Coating': ['Onbekend','Bitumen','Cement','Epimid','Geen','Polyetheen','Practisch geen','Teer-epoxy','Zink + bitumen'],
#         'Meldingen per 1000': [1899,1280,65,0,2368,233,3328,0,2411]}


# df4 = pd.DataFrame(data)
# df4 = df4.set_index('Coating')
# df4 = df4.sort_values(by="Meldingen per 1000", ascending=False)

# Vergroot de figuur en verbeter de stijl
plt.figure(figsize=(120, 60))
df4.plot(kind='line')

# Labels en titel
plt.title("Aantal storingen per installatiejaar", fontsize=16, fontweight='bold')
plt.xlabel("Jaar", fontsize=14)
plt.ylabel("Aantal", fontsize=14)

# Draai labels voor betere leesbaarheid
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Voeg grid toe
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.figtext(0.5, -0.1, "Totaal aantal meldingen: 439879, unieke melding IDs: 252052", ha="center", fontsize=12, bbox=dict(facecolor="lightgray", alpha=0.5))
# Toon de plot
plt.legend(title="Legenda", fontsize=12)
plt.tight_layout()
plt.show()


labels = ['Onderhoud', 'Niet plaatsgevonden']
sizes = [1288, 164141]
colors = ['#ff9999','#66b3ff'] 
explode = (0.1, 0)  

# Create the pie chart
plt.figure(figsize=(8, 8))  # Adjust figure size if needed
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, startangle=140)

plt.title('Verdeling van levensduurverlengend onderhoud')
plt.show()



