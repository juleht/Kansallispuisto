## Tulokset ja päätelmät

*species_info.csv* aineisto sisältää 5504 eri eläin- ja kasvilajia, jotka jakautuvat 7 eri luokkaan: nisäkkäisiin, lintuihin, matelijoihin, sammakkoeläimiin, kaloihin, putkilokasveihin ja sammaliin. Suojeluntila jakautuu aineistossa 4 luokkaan: uhanalainen, toipumassa, vaarassa olevat lajit ja huolta aiheuttavat lajit. Valtaosa lajeista ei ole vaarassa ollenkaan. Alla kuva eläinten ja kasvien määristä eri suojelustatuksesta:

![suojelutila](/kuvat/lajien_suojelutila.png)

Lähempi tarkastelu eri eläin- ja kasvilajien suojeluntilasta paljastaa sen, että eri eliöstöstä suurempi osa on suojelussa kuin toisesta. Eri prosentit lajeista, joilla on jokin suojelustatus:
![taulukko](/kuvat/taulukko.png)


Tarkastellaan ovatko suojeltujen lajien erot muutamien eläinlajiryhmien välillä tilastollisesti merkitseviä X2-testillä. X2-testi nisäkkäiden ja lintujen välillä paljastaa, että ero ei ole tilastollisesti merkitsevä p-arvo 0,44. Nisäkäs- ja lintulajeista yhtä monella on suojelustatus. Matelijoiden ja nisäkkäiden välillä ero sen sijaan oli tilastollisesti merkitsevä p-arvo 0,02. Suuremmalla määrällä nisäkäs lajeja on suojelustatus, kuin matelijoilla. 

Toista aineistoa *observations.csv* hyödynnetään lammaslajien havaintojen tarkasteluun. Ensin *observations.csv* ja *species_info.csv* yhdistetään lajien yleisiänimiä hyödyntäen. Havaintoja lampaista on neljästä eri kansallispuistosta ja alla on histogrammi havainnoista.

![havainnot](/kuvat/havainnot_viikko.png)