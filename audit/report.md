# Topology Zoo data-quality audit

*Copyright © 2026 Eric Parsonage*

Source: `/home/eric/InternetTopologyZoo/graphml`  

Graphs parsed: **276**  

Total nodes: **10,952**  

Total edges: **13,976**  


## Location coverage

- **85** graphs have every node located (lat + lon).
- **175** graphs have a mix of located and unlocated nodes.
- **16** graphs have zero located nodes.
- Total nodes missing at least one of lat/lon: **2,137**
  (19.5% of all nodes).
- Nodes whose lat/lon value was *provided but invalid* (empty string, 'None', 'NaN', out-of-range, non-numeric): **0**.

## Node classification (per glang's topology-zoo shape rules)

- **9,751** real internal nodes (become CORE routers).
- **975** Rj45 nodes (links to other networks; `Internal == 0`).
- **226** switch nodes (shared-medium fabrics; `hyperedge == 1`).
- **1,055** edges connect to a network beyond the graph (at least one Rj45 endpoint).

## Real-node lat/lon coverage

- **66** of **276** graphs have at least one real internal node missing lat/lon (the Rj45/switch holes are excluded).
- Total real internal nodes lacking lat/lon: **936** (9.6% of real nodes).

## Geonames eligibility (upper bound for 100% population coverage)

Geonames offers two lookup paths.  A real internal node is *reachable* if at least one applies:

- **Reverse** (lat/lon → nearest populated place).  No country scope needed; coordinates disambiguate globally.
- **Forward** (place name → matching geonames record).  Needs a country scope, either the node's own `Country` attribute or a graph-level single-country context (`GeoExtent == "Country"` with a non-empty `GeoLocation`).

A graph is *geonames-eligible* when **every** real internal node is reachable by at least one path.  This is the upper bound on graphs that could plausibly have population data added to every internal node via the geonames API.

- **255** of **276** graphs are geonames-eligible (92.4%).
- Across the whole archive, **354** real internal nodes are unreachable by either path (3.63% of real nodes).

## Geonames coverage (measured against cities500)

Live cities500 lookups were run for every real internal node.  A node is *resolved* when geonames returned a record (reverse from lat/lon, or forward from name+country).  Resolved nodes carry a population figure on the `Real-node Populations` sheet.

- **8,847** of **9,751** real internal nodes resolved (90.7%).
- **211** of **276** graphs have 100% of their real internal nodes resolved (76.4%).
- Aggregate population across resolved nodes: **5,055,589,570**.

## Partial-resolution to-do list

**51** graphs resolved most of their real internal nodes but missed at least one.  Each subsection below lists the unresolved labels alongside the lookup method that failed (`forward-miss` -- a name+country lookup that didn't match cities500; `unreachable` -- no lat/lon and no usable name+country).  Listed in completion-percentage order so the easiest graphs to finish appear first.

### Oteglobe -- 82/83 resolved (98.8%)

- `16` `OPTEGLOBE TBN` (unreachable)

### Bellsouth -- 50/51 resolved (98.0%)

- `22` `?` (forward-miss)

### Tinet -- 48/49 resolved (98.0%)

- `1` `?` (unreachable)

### DialtelecomCz -- 178/183 resolved (97.3%)

- `7` `Warsaw` (forward-miss)
- `36` `Bratislava` (forward-miss)
- `39` `Rajka` (forward-miss)
- `78` `Frankfurt` (forward-miss)
- `158` `None` (forward-miss)

### Ion -- 103/106 resolved (97.2%)

- `30` `None` (unreachable)
- `31` `None` (unreachable)
- `85` `Empire Telephone Co` (unreachable)

### Interoute -- 96/99 resolved (97.0%)

- `17` `Dubai` (unreachable)
- `41` `Edirne` (unreachable)
- `82` `Washington DC` (unreachable)

### Bren -- 29/30 resolved (96.7%)

- `9` `NMU` (forward-miss)

### Biznet -- 28/29 resolved (96.6%)

- `19` `Bakauhuni` (forward-miss)

### Janetbackbone -- 28/29 resolved (96.6%)

- `9` `Dublin` (forward-miss)

### Renater2006 -- 26/27 resolved (96.3%)

- `9` `CERN` (forward-miss)

### Renater2008 -- 26/27 resolved (96.3%)

- `9` `CERN` (forward-miss)

### Ulaknet -- 76/79 resolved (96.2%)

- `10` `Gazimagusa` (forward-miss)
- `17` `K. Maras` (forward-miss)
- `65` `S. Urfa` (forward-miss)

### GtsHungary -- 25/26 resolved (96.2%)

- `0` `None` (forward-miss)

### Amres -- 21/22 resolved (95.5%)

- `1` `Kosovska Mitrovica` (forward-miss)

### BtNorthAmerica -- 33/35 resolved (94.3%)

- `3` `?` (unreachable)
- `26` `?` (unreachable)

### Nextgen -- 16/17 resolved (94.1%)

- `2` `None` (forward-miss)

### GtsPoland -- 26/28 resolved (92.9%)

- `25` `Gdyia` (forward-miss)
- `30` `Gorzow Wilkp` (forward-miss)

### Litnet -- 39/42 resolved (92.9%)

- `5` `Siale` (forward-miss)
- `36` `N.Akmene` (forward-miss)
- `40` `Skoudas` (forward-miss)

### Rhnet -- 13/14 resolved (92.9%)

- `7` `Bifrost` (forward-miss)

### Geant2011 -- 37/40 resolved (92.5%)

- `10` `UA` (unreachable)
- `11` `MD` (unreachable)
- `19` `BY` (unreachable)

### Geant2012 -- 37/40 resolved (92.5%)

- `10` `UA` (unreachable)
- `11` `MD` (unreachable)
- `19` `BY` (unreachable)

### GtsSlovakia -- 28/31 resolved (90.3%)

- `1` `None` (forward-miss)
- `21` `None` (forward-miss)
- `22` `None` (forward-miss)

### GtsCzechRepublic -- 26/29 resolved (89.7%)

- `8` `Zmjno` (forward-miss)
- `10` `None` (forward-miss)
- `11` `Hardec Kralove` (forward-miss)

### Deltacom -- 101/113 resolved (89.4%)

- `84` `None` (forward-miss)
- `85` `None` (forward-miss)
- `86` `None` (forward-miss)
- `97` `None` (forward-miss)
- `98` `None` (forward-miss)
- `99` `None` (forward-miss)
- `100` `None` (forward-miss)
- `101` `None` (forward-miss)
- `102` `None` (forward-miss)
- `103` `None` (forward-miss)
- `111` `None` (forward-miss)
- `112` `None` (forward-miss)

### Evolink -- 32/36 resolved (88.9%)

- `13` `Frankfurt` (forward-miss)
- `27` `Bucharest` (forward-miss)
- `29` `Amsterdam` (forward-miss)
- `36` `Skopie` (forward-miss)

### KentmanJan2011 -- 30/34 resolved (88.2%)

- `16` `UCA-Epsom` (unreachable)
- `19` `UCA - Chatham` (unreachable)
- `27` `SOAS - Wye` (unreachable)
- `31` `Universities at Medway` (unreachable)

### Cesnet2 -- 20/23 resolved (87.0%)

- `1` `Plzen` (forward-miss)
- `5` `Praha` (forward-miss)
- `22` `Breclav,Lednice` (forward-miss)

### Restena -- 13/15 resolved (86.7%)

- `6` `ADSL (via EPT)` (forward-miss)
- `11` `ADSL (via Tango)` (forward-miss)

### Belnet2010 -- 19/22 resolved (86.4%)

- `0` `Liege1` (forward-miss)
- `6` `Bruzav` (forward-miss)
- `10` `Brudie` (forward-miss)

### Grena -- 13/16 resolved (81.2%)

- `7` `Corecess DX6524` (forward-miss)
- `9` `Corecess DX6524` (forward-miss)
- `12` `Corecess DX6524` (forward-miss)

### LambdaNet -- 33/41 resolved (80.5%)

- `9` `Prague` (forward-miss)
- `10` `Stockholm` (forward-miss)
- `17` `Brno` (forward-miss)
- `18` `Vienna` (forward-miss)
- `19` `Bratislava` (forward-miss)
- `23` `London` (forward-miss)
- `28` `Zurich` (forward-miss)
- `33` `Copenhagen` (forward-miss)

### BtLatinAmerica -- 36/48 resolved (75.0%)

- `4` `?` (unreachable)
- `10` `?` (unreachable)
- `18` `?` (unreachable)
- `19` `?` (unreachable)
- `20` `?` (unreachable)
- `25` `?` (unreachable)
- `26` `?` (unreachable)
- `27` `?` (unreachable)
- `28` `?` (unreachable)
- `33` `?` (unreachable)
- `39` `?` (unreachable)
- `40` `?` (unreachable)

### UniC -- 15/22 resolved (68.2%)

- `9` `None` (forward-miss)
- `12` `None` (forward-miss)
- `13` `None` (forward-miss)
- `15` `None` (forward-miss)
- `17` `None` (forward-miss)
- `23` `None` (forward-miss)
- `24` `None` (forward-miss)

### Sinet -- 47/74 resolved (63.5%)

- `3` `Kyushu IT` (forward-miss)
- `8` `IMS, U Tokyo` (forward-miss)
- `9` `ISSP, U Tokyo` (forward-miss)
- `12` `Kamioka Obs, ICRR, U Tokyo` (forward-miss)
- `15` `NIFS` (forward-miss)
- `17` `JAIST` (forward-miss)
- `19` `ICR, Kyoto U` (forward-miss)
- `21` `NINS-Okazaki` (forward-miss)
- `29` `NII` (forward-miss)
- `30` `NII-CHiba` (forward-miss)
- `31` `GSIST, U Tokyo` (forward-miss)
- `32` `U Electro-Communications` (forward-miss)
- `33` `RIKEN` (forward-miss)
- `36` `JAXA-ISAS` (forward-miss)
- `37` `Yokohama National U` (forward-miss)
- `39` `Tokyo IT` (forward-miss)
- `42` `KEK` (forward-miss)
- `43` `JAEA` (forward-miss)
- `47` `ISM` (forward-miss)
- `55` `JAMSTEC` (forward-miss)
- `56` `JASRI` (forward-miss)
- `60` `NAOJ` (forward-miss)
- `62` `JAXA-IAT` (forward-miss)
- `63` `Tokyo U Ag and Tech` (forward-miss)
- `65` `Kurnamoto U` (forward-miss)
- `68` `Kitami IT` (forward-miss)
- `72` `U of the Ryukyus` (forward-miss)

### Globenet -- 40/63 resolved (63.5%)

- `4` `1` (unreachable)
- `9` `12` (unreachable)
- `12` `9` (unreachable)
- `13` `14` (unreachable)
- `15` `15` (unreachable)
- `17` `19` (unreachable)
- `18` `3` (unreachable)
- `20` `4` (unreachable)
- `23` `21` (unreachable)
- `25` `20` (unreachable)
- `28` `10` (unreachable)
- `29` `16` (unreachable)
- `30` `8` (unreachable)
- `34` `11` (unreachable)
- `37` `18` (unreachable)
- `38` `6` (unreachable)
- `41` `17` (unreachable)
- `42` `6` (unreachable)
- `44` `7` (unreachable)
- `45` `22` (unreachable)
- `48` `2` (unreachable)
- `51` `23` (unreachable)
- `63` `13` (unreachable)

### Easynet -- 12/19 resolved (63.2%)

- `0` `1` (unreachable)
- `1` `1` (unreachable)
- `2` `1` (unreachable)
- `3` `1` (unreachable)
- `6` `1` (unreachable)
- `7` `1` (unreachable)
- `17` `1` (unreachable)

### Myren -- 20/35 resolved (57.1%)

- `0` `UiTM` (forward-miss)
- `6` `IUM` (forward-miss)
- `7` `UPSI` (forward-miss)
- `8` `Nottingham Malaysia` (forward-miss)
- `10` `UTHM` (forward-miss)
- `12` `UMT` (forward-miss)
- `14` `UDM` (forward-miss)
- `16` `UPNIM` (forward-miss)
- `17` `UTeM` (forward-miss)
- `18` `NOC` (forward-miss)
- `23` `MIMOS` (forward-miss)
- `25` `TMRnD` (forward-miss)
- `26` `MoHE` (forward-miss)
- `28` `UniMAP` (forward-miss)
- `30` `Border Router` (forward-miss)

### Columbus -- 31/60 resolved (51.7%)

- `0` `None` (unreachable)
- `1` `None` (unreachable)
- `7` `None` (unreachable)
- `14` `None` (unreachable)
- `15` `None` (unreachable)
- `17` `None` (unreachable)
- `22` `None` (unreachable)
- `24` `None` (unreachable)
- `26` `None` (unreachable)
- `31` `None` (unreachable)
- `32` `None` (unreachable)
- `34` `None` (unreachable)
- `37` `None` (unreachable)
- `38` `None` (unreachable)
- `39` `None` (unreachable)
- `41` `None` (unreachable)
- `44` `None` (unreachable)
- `45` `None` (unreachable)
- `47` `St Kitts & Nevis` (unreachable)
- `49` `None` (unreachable)
- `50` `None` (unreachable)
- `56` `None` (unreachable)
- `58` `None` (unreachable)
- `59` `None` (unreachable)
- `60` `None` (unreachable)
- `62` `None` (unreachable)
- `63` `None` (unreachable)
- `67` `None` (unreachable)
- `69` `None` (unreachable)

### JanetExternal -- 1/2 resolved (50.0%)

- `5` `JANET` (forward-miss)

### Reuna -- 15/31 resolved (48.4%)

- `0` `UCT` (forward-miss)
- `2` `UACH` (forward-miss)
- `3` `UFRO` (forward-miss)
- `4` `UCN` (forward-miss)
- `5` `UNAP Sede Santiago` (forward-miss)
- `6` `UNAP` (forward-miss)
- `11` `RC-12` (forward-miss)
- `12` `RC-Nacional` (forward-miss)
- `27` `UDEC` (forward-miss)
- `28` `UBB` (forward-miss)
- `29` `UDA` (forward-miss)
- `32` `UCHILE` (forward-miss)
- `33` `UTEM` (forward-miss)
- `34` `UMCE` (forward-miss)
- `35` `USACH` (forward-miss)
- `36` `REUNA` (forward-miss)

### Gambia -- 12/25 resolved (48.0%)

- `0` `Gamnet` (unreachable)
- `1` `Qnet AS` (unreachable)
- `4` `MDI` (unreachable)
- `5` `GTMI` (unreachable)
- `6` `Quantum Net` (unreachable)
- `7` `MRC` (unreachable)
- `8` `Univ Gambia` (unreachable)
- `9` `GTMI` (unreachable)
- `10` `Mansk Gambia` (unreachable)
- `11` `Gamtel House` (unreachable)
- `12` `Action Ltd` (unreachable)
- `13` `UNDP` (unreachable)
- `17` `Gantd Center` (unreachable)

### Belnet -- 10/22 resolved (45.5%)

- `1` `Gent1` (forward-miss)
- `2` `Gent2` (forward-miss)
- `3` `Antwerpen1` (forward-miss)
- `4` `Antwerpen 2` (forward-miss)
- `5` `Korthijk` (forward-miss)
- `11` `Liege2` (forward-miss)
- `12` `Liege 1` (forward-miss)
- `13` `Brusell Camp.` (forward-miss)
- `14` `Bruzav` (forward-miss)
- `15` `Brudie` (forward-miss)
- `18` `Leuven1` (forward-miss)
- `19` `Leuven2` (forward-miss)

### Marwan -- 6/14 resolved (42.9%)

- `5` `University 2` (forward-miss)
- `6` `None` (forward-miss)
- `8` `Institution 1` (forward-miss)
- `9` `University 3` (forward-miss)
- `10` `University 1` (forward-miss)
- `13` `None` (forward-miss)
- `14` `University 4` (forward-miss)
- `15` `None` (forward-miss)

### Zamren -- 14/33 resolved (42.4%)

- `0` `N/Western Province` (forward-miss)
- `4` `NRDC` (forward-miss)
- `5` `UNZA Research` (forward-miss)
- `8` `NIPA` (forward-miss)
- `9` `ZICAS` (forward-miss)
- `10` `Gateway Router` (forward-miss)
- `11` `Gateway Router` (forward-miss)
- `12` `Gateway Router` (forward-miss)
- `16` `ZESCO TS` (forward-miss)
- `17` `ZAMTEL TS` (forward-miss)
- `19` `NISR` (forward-miss)
- `20` `Mt Makulu` (forward-miss)
- `22` `KTC` (forward-miss)
- `23` `COSETCO` (forward-miss)
- `24` `KABWE TRADES` (forward-miss)
- `25` `NKRUMAH` (forward-miss)
- `26` `Gateway Router` (forward-miss)
- `34` `Gateway Router` (forward-miss)
- `35` `Gateway Router` (forward-miss)

### Fatman -- 5/14 resolved (35.7%)

- `0` `Carnegie College` (unreachable)
- `1` `Adam Smith College` (unreachable)
- `3` `UoD Fife Campus` (unreachable)
- `7` `Dundee College` (unreachable)
- `8` `Angus College` (unreachable)
- `13` `University of Abertay Dundee` (unreachable)
- `14` `University of Dundee` (unreachable)
- `15` `University of St Andrews` (unreachable)
- `16` `Elmwood College` (unreachable)

### Esnet -- 18/54 resolved (33.3%)

- `4` `ANL` (forward-miss)
- `7` `FNAL` (forward-miss)
- `8` `DOE-A` (forward-miss)
- `9` `Allied Signal` (forward-miss)
- `16` `None` (forward-miss)
- `17` `None` (forward-miss)
- `18` `NETL` (forward-miss)
- `19` `DOE` (forward-miss)
- `20` `None` (forward-miss)
- `21` `None` (forward-miss)
- `22` `PPPL` (forward-miss)
- `23` `BNL` (forward-miss)
- `24` `PSFC` (forward-miss)
- `25` `None` (forward-miss)
- `27` `NREL` (forward-miss)
- `29` `SNLA` (forward-miss)
- `31` `GA` (forward-miss)
- `36` `ARM` (forward-miss)
- `37` `NOAA` (forward-miss)
- `38` `None` (forward-miss)
- `39` `None` (forward-miss)
- `40` `None` (forward-miss)
- `41` `None` (forward-miss)
- `42` `None` (forward-miss)
- `43` `None` (forward-miss)
- `44` `BECHTEL-NV` (forward-miss)
- `46` `DOE GTN` (forward-miss)
- `47` `NNSA` (forward-miss)
- `48` `OSTI` (forward-miss)
- `49` `ORAU` (forward-miss)
- `54` `JLAB` (forward-miss)
- `55` `SRS` (forward-miss)
- `56` `PNNL` (forward-miss)
- `59` `INL` (forward-miss)
- `64` `LANL` (forward-miss)
- `65` `LIGO` (forward-miss)

### TLex -- 1/4 resolved (25.0%)

- `2` `Cat 6500 AS23814` (unreachable)
- `10` `BigIron 15000 AS23814` (unreachable)
- `11` `NetIron N140G AS23814` (unreachable)

### Cynet -- 4/24 resolved (16.7%)

- `0` `Cyprus Univ. of Tech.` (forward-miss)
- `2` `United Nations` (forward-miss)
- `4` `Users` (forward-miss)
- `5` `Grid` (forward-miss)
- `6` `Grid-SW` (forward-miss)
- `7` `None` (forward-miss)
- `9` `Inst. of Neurology` (forward-miss)
- `10` `Pedagogical Inst.` (forward-miss)
- `11` `Nursing School` (forward-miss)
- `12` `Phillips College` (forward-miss)
- `13` `European Uni.` (forward-miss)
- `14` `Open Uni. of Cyprus` (forward-miss)
- `15` `Univ. of Nicosia` (forward-miss)
- `16` `Agriculture Inst.` (forward-miss)
- `17` `Cyprus Inst.` (forward-miss)
- `18` `English School` (forward-miss)
- `19` `Uni. of Frederick` (forward-miss)
- `21` `European Inst. of Cyprus` (forward-miss)
- `23` `EUMED CONNECT` (forward-miss)
- `28` `Evagoras` (forward-miss)

### Padi -- 1/14 resolved (7.1%)

- `0` `AQSA` (unreachable)
- `1` `IUG` (unreachable)
- `2` `HU` (unreachable)
- `3` `PPU` (unreachable)
- `4` `AZHR` (unreachable)
- `5` `ARIJ` (unreachable)
- `6` `ICB` (unreachable)
- `8` `Annajah National Univeristy` (unreachable)
- `9` `AAUJ` (unreachable)
- `10` `BZU` (unreachable)
- `12` `QOU` (unreachable)
- `13` `AQU` (unreachable)
- `14` `BU` (unreachable)

### Pern -- 8/123 resolved (6.5%)

- `0` `None` (forward-miss)
- `1` `None` (forward-miss)
- `2` `None` (forward-miss)
- `3` `None` (forward-miss)
- `4` `None` (forward-miss)
- `5` `None` (forward-miss)
- `6` `None` (forward-miss)
- `7` `None` (forward-miss)
- `8` `None` (forward-miss)
- `9` `None` (forward-miss)
- `11` `None` (forward-miss)
- `12` `None` (forward-miss)
- `14` `None` (forward-miss)
- `15` `None` (forward-miss)
- `16` `None` (forward-miss)
- `17` `None` (forward-miss)
- `18` `None` (forward-miss)
- `19` `None` (forward-miss)
- `20` `None` (forward-miss)
- `21` `None` (forward-miss)
- `22` `None` (forward-miss)
- `23` `None` (forward-miss)
- `24` `None` (forward-miss)
- `25` `None` (forward-miss)
- `26` `None` (forward-miss)
- `27` `None` (forward-miss)
- `28` `None` (forward-miss)
- `29` `None` (forward-miss)
- `30` `None` (forward-miss)
- `31` `None` (forward-miss)
- `32` `None` (forward-miss)
- `33` `None` (forward-miss)
- `34` `None` (forward-miss)
- `35` `None` (forward-miss)
- `36` `None` (forward-miss)
- `37` `None` (forward-miss)
- `38` `None` (forward-miss)
- `39` `None` (forward-miss)
- `40` `None` (forward-miss)
- `41` `None` (forward-miss)
- `42` `None` (forward-miss)
- `44` `None` (forward-miss)
- `45` `None` (forward-miss)
- `47` `None` (forward-miss)
- `48` `None` (forward-miss)
- `49` `None` (forward-miss)
- `51` `None` (forward-miss)
- `52` `None` (forward-miss)
- `53` `None` (forward-miss)
- `54` `None` (forward-miss)
- `55` `None` (forward-miss)
- `56` `None` (forward-miss)
- `57` `None` (forward-miss)
- `58` `None` (forward-miss)
- `61` `None` (forward-miss)
- `62` `None` (forward-miss)
- `63` `None` (forward-miss)
- `64` `None` (forward-miss)
- `65` `None` (forward-miss)
- `67` `None` (forward-miss)
- `68` `None` (forward-miss)
- `69` `None` (forward-miss)
- `70` `None` (forward-miss)
- `71` `None` (forward-miss)
- `73` `None` (forward-miss)
- `74` `None` (forward-miss)
- `75` `None` (forward-miss)
- `76` `None` (forward-miss)
- `77` `None` (forward-miss)
- `78` `None` (forward-miss)
- `79` `None` (forward-miss)
- `80` `None` (forward-miss)
- `81` `None` (forward-miss)
- `82` `None` (forward-miss)
- `83` `None` (forward-miss)
- `84` `None` (forward-miss)
- `85` `None` (forward-miss)
- `86` `None` (forward-miss)
- `87` `None` (forward-miss)
- `88` `None` (forward-miss)
- `89` `None` (forward-miss)
- `90` `None` (forward-miss)
- `91` `None` (forward-miss)
- `92` `None` (forward-miss)
- `93` `None` (forward-miss)
- `94` `None` (forward-miss)
- `95` `None` (forward-miss)
- `96` `None` (forward-miss)
- `97` `None` (forward-miss)
- `98` `None` (forward-miss)
- `99` `None` (forward-miss)
- `100` `None` (forward-miss)
- `101` `None` (forward-miss)
- `103` `None` (forward-miss)
- `104` `None` (forward-miss)
- `105` `None` (forward-miss)
- `106` `None` (forward-miss)
- `107` `None` (forward-miss)
- `108` `None` (forward-miss)
- `109` `None` (forward-miss)
- `110` `None` (forward-miss)
- `111` `None` (forward-miss)
- `112` `None` (forward-miss)
- `113` `None` (forward-miss)
- `114` `None` (forward-miss)
- `115` `None` (forward-miss)
- `116` `None` (forward-miss)
- `117` `None` (forward-miss)
- `118` `None` (forward-miss)
- `120` `None` (forward-miss)
- `121` `None` (forward-miss)
- `122` `None` (forward-miss)
- `123` `None` (forward-miss)
- `124` `None` (forward-miss)
- `125` `None` (forward-miss)

### AsnetAm -- 1/63 resolved (1.6%)

- `0` `?` (unreachable)
- `1` `Drug Agency` (unreachable)
- `2` `Inst. Radio Meas.` (unreachable)
- `3` `Isnt. Chemical Physics` (unreachable)
- `4` `Inst. Biochem` (unreachable)
- `5` `Inst. Geophysics` (unreachable)
- `6` `Inst. of Health` (unreachable)
- `7` `Inst. Informatics` (unreachable)
- `8` `TV station` (unreachable)
- `9` `Inst. Phylosophy` (unreachable)
- `10` `?` (unreachable)
- `11` `Organic chem` (unreachable)
- `12` `Library` (unreachable)
- `14` `ICT` (unreachable)
- `15` `Geological` (unreachable)
- `16` `Inst. Math.` (unreachable)
- `17` `Inst. Mechanics` (unreachable)
- `18` `ASHMS` (unreachable)
- `19` `Inst. Physiology` (unreachable)
- `20` `Yeveran Physics Inst.` (unreachable)
- `21` `ArmESFo` (unreachable)
- `22` `National Academy` (unreachable)
- `23` `NSSPA` (unreachable)
- `24` `Min. of Education` (unreachable)
- `25` `National Stats. science` (unreachable)
- `26` `EEMC MNP` (unreachable)
- `27` `?` (unreachable)
- `28` `Museum` (unreachable)
- `29` `ISTC` (unreachable)
- `30` `Geophys. Obser.` (unreachable)
- `31` `?` (unreachable)
- `32` `Encycloped.` (unreachable)
- `33` `Literature` (unreachable)
- `34` `Economy` (unreachable)
- `35` `Linguistic Inst` (unreachable)
- `37` `American Uni.` (unreachable)
- `38` `Oriental` (unreachable)
- `39` `Hist` (unreachable)
- `41` `Hydroecol` (unreachable)
- `42` `Engineer academy` (unreachable)
- `43` `education` (unreachable)
- `44` `SCS` (unreachable)
- `45` `Organic Chem` (unreachable)
- `46` `Astrophysical Obs.` (unreachable)
- `47` `Inst. Microbiology` (unreachable)
- `48` `Molecular Structure` (unreachable)
- `49` `General Chem` (unreachable)
- `50` `research` (unreachable)
- `51` `engineering center` (unreachable)
- `52` `?` (unreachable)
- `53` `Inst. Radiophysics` (unreachable)
- `54` `ARENA` (unreachable)
- `55` `Institute of Applied Physics` (unreachable)
- `56` `Inst. of Molecular Biology` (unreachable)
- `57` `Agricultural Academy` (unreachable)
- `58` `Ecological Center` (unreachable)
- `59` `Intitute of Botany` (unreachable)
- `60` `Institute of Zoology` (unreachable)
- `61` `Gallery` (unreachable)
- `62` `Yerevan University` (unreachable)
- `63` `State Engineering University` (unreachable)
- `64` `Yerevan Medical University` (unreachable)

## Graph structure

- Multigraphs (at least one pair of parallel edges): **96**.
- Total parallel edges across the archive: **654**.
- Total self-loops: **2**.
- Graphs with >1 connected component: **23**.
- Isolated (edgeless) nodes overall: **115**.
- Edges whose source or target was not declared as a node: **0**.

## Labels

- Nodes without any `label` attribute: **20**.
- Nodes whose label is whitespace only: **0**.
- Nodes whose label contains control characters: **0**.
- Graphs containing duplicate labels: **120**.
- Total duplicate-label occurrences: **269** (counted as 1 per label that has ≥2 carriers within its graph).

## Issue tally by category

- `node-missing-both`: 2137
- `real-node-missing-latlon`: 936
- `edge-parallel`: 498
- `node-label-duplicate`: 266
- `node-isolated`: 115
- `graph-disconnected`: 23
- `node-label-missing`: 20
- `edge-self-loop`: 2

## Issue tally by severity

- `info`: 2658
- `warn`: 1339

## Largest graphs

| Graph | Nodes | Edges | Multi? | Missing latlon |
|---|---:|---:|:---:|---:|
| Kdl | 754 | 899 | yes | 28 |
| Cogentco | 197 | 245 | yes | 11 |
| DialtelecomCz | 193 | 151 | no | 15 |
| UsCarrier | 158 | 189 | no | 6 |
| Colt | 153 | 191 | yes | 4 |
| GtsCe | 149 | 193 | no | 8 |
| TataNld | 145 | 194 | yes | 2 |
| Pern | 127 | 129 | no | 119 |
| Ion | 125 | 150 | yes | 22 |
| Deltacom | 113 | 183 | yes | 12 |

## Worst location coverage (absolute count)

| Graph | Nodes | Missing | % |
|---|---:|---:|---:|
| Pern | 127 | 119 | 93.7% |
| Opteglobe | 93 | 93 | 100.0% |
| IntNetworkmap | 89 | 89 | 100.0% |
| AsnetAm | 65 | 64 | 98.5% |
| Garr | 56 | 56 | 100.0% |
| Cudi | 51 | 51 | 100.0% |
| Esnet | 68 | 51 | 75.0% |
| Internode | 66 | 46 | 69.7% |
| Columbus | 70 | 39 | 55.7% |
| Geant | 37 | 37 | 100.0% |

## Top multigraphs by parallel-edge count

| Graph | Edges | Parallel pairs |
|---|---:|---:|
| Ntt | 216 | 153 |
| Deltacom | 183 | 22 |
| Highwinds | 53 | 22 |
| Globenet | 113 | 18 |
| Sunet | 49 | 17 |
| Colt | 191 | 14 |
| Garr201112 | 89 | 14 |
| Garr201201 | 89 | 14 |
| Esnet | 92 | 13 |
| Garr201110 | 87 | 13 |

## How to use the workbook

The companion workbook `zoo-audit.xlsx` has:
1. **Summary** — one row per graph with the same columns as the totals at the bottom of this report. The last row is the cross-archive total.
2. **Missing Locations** — every single node with a missing or invalid lat/lon across the whole corpus.
3. **Issues** — every issue found, labelled by severity (error / warn / info) and category, with the node or edge id in the detail.
4. **Multigraphs** — the subset of graphs with parallel edges, plus their edge counts.
5. **one sheet per graph** — full attribute table for every node and every edge; rows with problems are highlighted.

## Notes on terminology

- "Missing lat/lon" counts a node if *either* of its Latitude or Longitude attributes is absent, empty, one of the sentinels `None`/`NaN`/`null`/`-`, or fails numeric coercion.
- "Multigraph" here means *observed* parallel edges, not the GraphML `parse.multiplegraph` flag (which is rarely set in the Zoo files).
- "Duplicate labels" counts **distinct labels** carried by 2+ nodes; for a count of *affected nodes* multiply by at least 2.
