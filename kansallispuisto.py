import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

# Projektissa analysoidaan kahta eri aineistoa,
# joista ensimmäinen species_info.csv
# kuvaa erilaisia eläin- ja kasvilajeja kansallispuistossa
# aineistossa on lajien tieteelliset nimet, yleisetnimet ja
# lajien suojeluntila

# Toinen aineisto observations.csv kuvaa erilaisten eläin-
# ja kasvilajien havaintojen määrää yhden viikon ajalta
# eri kansallispuistoissa. Aineistossa on lajien tieteellinen nimi,
# kansallispuistonnimi ja havaintojen lukumaara


lajit = pd.read_csv('aineistot/species_info.csv', sep = ',')
print(lajit.head())


lajien_lukumaara = lajit.common_names.nunique()
print(f"Erilaisten lajien lukumaara aineistossa on {lajien_lukumaara}")

luokittelu = lajit.category.unique()
print(f"Eläin ja kasvilajit on luokiteltu aineistossa ryhmiin: {luokittelu}")

suojelu = lajit.conservation_status.unique()
print(f"Eläin- ja kasvilajen suojeluntaso on luokiteltu aineistossa ryhmiin: {suojelu}")

lukumaara_suojelu = lajit.groupby('conservation_status').common_names.count()
print(f"Määrät eri suojeluluokassa olevista lajeista:\n{lukumaara_suojelu}")

# Valtaosa lajistossa on aineistossa suojelematta, joten täytetään tyhjät arvot suojeluntila kolumnissa
lajit.conservation_status.fillna('No Intervention', inplace = True)
lukumaara_suojelu_NaN = lajit.groupby('conservation_status').common_names.count()
print(f"Lajien määrät eri suojeluluokissa olevista lajeista:\n{lukumaara_suojelu_NaN}")

# Järjestetään suojelutila pienimmästä suurimpaan histogrammia varten
suojelu_maarat = lajit.groupby('conservation_status').common_names.count().reset_index().sort_values(by='common_names')


# luodaan histogrammi kuvaamaan lajien määrää suojelussa
plt.figure(figsize=(10,4))
ax = plt.subplot(1,1,1)
x = list(range(len(suojelu_maarat)))
print(x)
y = suojelu_maarat.common_names
xakseli = suojelu_maarat.conservation_status.to_numpy()

plt.bar(x,y)
ax.set_xticks(x)
ax.set_xticklabels(xakseli)
plt.xlabel('Lajien lukumaara')
plt.title('Lajien suojeluntila')
plt.show()

# Valtaosa eläimistä ei tarvitse suojelua, mutta tarkastellaan onko jokin eliöryhmä:
# nisäkkäät, selkärangattomat jne. todennäköisemmin suojelun tarpeessa kuin toinen
# analyysi tehdään chi2-testillä

# luodaan ensin uusi kolumni, joka kuvaa onko eläin jonkin asteisen suojelun tarpeessa vai ei
suojelu_tila = lambda x : True if x != 'No Intervention' else False
lajit['is_protected'] = lajit.conservation_status.apply(suojelu_tila)

luokittelu_suojelu = lajit.groupby(['category', 'is_protected']).scientific_name.count().reset_index()

luokittelu_suojelu_kaannetty = luokittelu_suojelu.pivot(
    index = 'category',
    columns = 'is_protected',
    values = 'scientific_name'
).reset_index()

luokittelu_suojelu_kaannetty = luokittelu_suojelu_kaannetty.rename(columns={
    False :'not_protected',
    True : 'protected',
    
})

print(f"määrät eliöittäin onko suojelussa vai ei:\n{luokittelu_suojelu_kaannetty}")

p = lambda row : (row.protected/(row.not_protected + row.protected)) * 100

luokittelu_suojelu_kaannetty['suojelu_aste'] = luokittelu_suojelu_kaannetty.apply(p,axis=1)

g = pd.concat([luokittelu_suojelu_kaannetty.category, luokittelu_suojelu_kaannetty.suojelu_aste], axis =1)

print(f"Eri prosentit lajiesta, joilla on jokin suojelutaso:\n{g}")

# Testataan chi2-testillä onko nisäkkäiden ja lintujen suojeluasteessa tilastollisesti merkitsevää eroa.
lintu = luokittelu_suojelu_kaannetty.iloc[1:2, 1:3]
nisakas = luokittelu_suojelu_kaannetty.iloc[3:4, 1:3]
lintu_nisakas = pd.concat([lintu,nisakas]).to_numpy()

chi2, p_arvo, vapausaste, odotusarvot = chi2_contingency(lintu_nisakas)
if p_arvo < 0.05:
    print(f"{p_arvo} on pienempi kuin 0.05, mikä tarkoittaa että 95 % luottamusvälillä suojeluntasossa on tilastollisesti merkittävä ero. Nisäkkäitä suojellaan enemmän kuin lintuja.")
else:
    print(f"{p_arvo} on suurempi kuin 0.05, mikä tarkoittaa, että 95 % luottamusvälillä suojeluntasossa ei ole tilastollisesti merkittävää eroa. Nisäkkäitä ja lintuja suojellaan yhtä paljon.")

# Testataan chi2-testillä onko nisäkkäiden ja matelijoiden suojeluasteessa tilastollisesti merkitsevää eroa.

matelija = luokittelu_suojelu_kaannetty.iloc[5:6,1:3]
matelija_nisakas = pd.concat([matelija, nisakas]).to_numpy()

chi2, p_arvo, vapausaste, odotusarvot = chi2_contingency(matelija_nisakas)
if p_arvo < 0.05:
    print(f"{p_arvo} on pienempi kuin 0.05, mikä tarkoittaa että 95 % luottamusvälillä suojeluntasossa on tilastollisesti merkittävä ero. Nisäkkäitä suojellaan enemmän kuin matelijoita.")
else:
    print(f"{p_arvo} on suurempi kuin 0.05, mikä tarkoittaa, että 95 % luottamusvälillä suojeluntasossa ei ole tilastollisesti merkittävää eroa. Nisäkkäitä ja matelijoita suojellaan yhtä paljon.")



# Havainnot aineisto kuvaa erilaisten lajien havaintoja kansallispuistoissa viimeisen 7 päivän ajalta

havainnot = pd.read_csv('aineistot/observations.csv', sep=',')
print(havainnot.head(10))

# Tarkastellaan havaintoja lampaista kansallispuistoissa. Tätä varten yhdistetään ensimäinen aineisto Lajit
# Havainnot-aineiston kanssa, aloitetaan selvittämällä lammaslajit Lajit-aineistosta ja yhdistetään sitten aineistot keskenään.

l = lambda x : 'sheep' in x.lower()
lajit['is_sheep'] = lajit.common_names.apply(l)
lampaat = lajit[(lajit.is_sheep == True) & (lajit.category == 'Mammal')]
lammas_havainnot = havainnot.merge(lampaat)
print(f"Havainnot lampaista viimeisen viikon ajalta kansallispuistoissa\n{lammas_havainnot}")

lammas_havainnot_yhteensa = lammas_havainnot.groupby('park_name').observations.sum().reset_index()
print(f"Havainnot lampaista kansallispuistoissa laskettuna yhteen\n{lammas_havainnot_yhteensa}")

plt.figure(figsize=(16,4))
ax = plt.subplot(1,1,1)
x = range(len(lammas_havainnot_yhteensa))
xtick = lammas_havainnot_yhteensa.park_name.to_numpy()
print(xtick) 
y = lammas_havainnot_yhteensa.observations
ax.set_xticks(x)
ax.set_xticklabels(xtick)

plt.bar(x,y)
plt.ylabel('Havaintojen lukumaara')
plt.xlabel('Luonnonpuiston nimi')
plt.title('Lammashavainnot viikottain')
plt.show()