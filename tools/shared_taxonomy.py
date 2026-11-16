import json, os, re, unicodedata, collections
# shared taxonomy and helpers of the CNSC value-chain radars (extracted from the Saxony builder make_sx.py)

CODE={'1.1':('EDA nástroje','EDA tools','design'),'1.2':('IP bloky','IP cores','design'),'1.3':('Návrh čipů','Chip design','design'),
'1.4':('Software a nástroje pro čipy','Software enablement and tools for chips','software'),
'2.1':('Zařízení pro výrobu waferů','Wafer-fab equipment','equipment'),'2.2':('Metrologie, inspekce, mikroskopie','Metrology, inspection, microscopy','metrology'),
'2.3':('Zařízení pro montáž a test','Assembly and test equipment','equipment'),
'2.4.1':('Vakuová technika','Vacuum technology','subsystems'),'2.4.2':('Rozvod plynů, chemie a kapalin','Gas, chemical and fluid delivery','subsystems'),
'2.4.3':('Optika, lasery, fotonické komponenty','Optics, lasers and photonics components','subsystems'),'2.4.4':('Automatizace, handling, pohony','Automation, handling and motion','subsystems'),
'2.4.5':('Přesné díly a materiály pro nástroje','Precision parts and tool materials','subsystems'),'2.4.6':('Teplotní management, filtrace, kontrola kontaminace','Thermal, filtration and contamination control','subsystems'),
'2.5':('Služby a procesy pro výrobu','Enabling services and processes','subsystems'),'F':('Čisté prostory a fab infrastruktura','Fab facilities and cleanrooms','subsystems'),
'3.1':('Wafery a substráty','Wafers and substrates','materials'),'3.2':('Procesní materiály','Process materials','materials'),
'4.2':('Výroba čipů – foundry a IDM','Mature and specialty manufacturing','fab'),'4.3':('Paměti','Memory','fab'),'4.4':('Výkonové a WBG součástky','Power and wide-bandgap','fab'),
'4.5':('Senzory, MEMS, optoelektronika','Sensors, MEMS, optoelectronics','fab'),'4.6':('Fotonika a kvantové technologie','Photonics and quantum','fab'),
'5.1':('Služby montáže a testu','Assembly and test services','fab'),'5.2':('Pokročilé pouzdření','Advanced packaging','fab'),'5.3':('Testovací a kvalifikační služby','Test and qualification services','fab'),
'6.1':('Aplikace: automotive','End market: automotive','downstream'),'6.2':('Aplikace: průmysl','End market: industrial','downstream'),'6.3':('Aplikace: energetika','End market: energy','downstream'),
'6.4':('Aplikace: komunikace a IoT','End market: communications and IoT','downstream'),'6.5':('Aplikace: zdravotnictví','End market: health','downstream'),'6.6':('Aplikace: výpočty a AI','End market: computing and AI','downstream'),
'7.1':('Výzkum a pilotní linky','Research and pilot lines','ecosystem'),'7.2':('Vzdělávání a dovednosti','Skills','ecosystem'),'7.3':('Politika, financování, klastry','Policy, funding and clusters','ecosystem'),
'D':('Distribuce součástek','Distribution','distribution')}
DE_CODE={'1.1':'EDA-Werkzeuge','1.2':'IP-Blöcke','1.3':'Chipdesign','1.4':'Software und Werkzeuge für Chips','2.1':'Waferfertigungsanlagen','2.2':'Messtechnik, Inspektion, Mikroskopie','2.3':'Montage- und Testanlagen','2.4.1':'Vakuumtechnik','2.4.2':'Gas-, Chemikalien- und Fluidversorgung','2.4.3':'Optik, Laser, photonische Komponenten','2.4.4':'Automatisierung, Handling, Antriebe','2.4.5':'Präzisionsteile und Werkstoffe für Anlagen','2.4.6':'Temperierung, Filtration, Kontaminationskontrolle','2.5':'Dienstleistungen und Prozesse für die Fertigung','F':'Reinräume und Fab-Infrastruktur','3.1':'Wafer und Substrate','3.2':'Prozessmaterialien','4.2':'Chipfertigung – Foundry und IDM','4.3':'Speicher','4.4':'Leistungs- und WBG-Bauelemente','4.5':'Sensoren, MEMS, Optoelektronik','4.6':'Photonik und Quantentechnologien','5.1':'Montage- und Testdienstleistungen','5.2':'Advanced Packaging','5.3':'Test- und Qualifizierungsdienste','6.1':'Anwendung: Automotive','6.2':'Anwendung: Industrie','6.3':'Anwendung: Energie','6.4':'Anwendung: Kommunikation und IoT','6.5':'Anwendung: Gesundheit','6.6':'Anwendung: Computing und KI','7.1':'Forschung und Pilotlinien','7.2':'Aus- und Weiterbildung','7.3':'Politik, Förderung, Cluster','D':'Distribution von Bauelementen'}
SEG_DE={'design':'Chipdesign & IP','software':'Software für Chips','equipment':'Anlagen','metrology':'Messtechnik','subsystems':'Subsysteme & Dienstleistungen','materials':'Materialien','fab':'Fertigung & Packaging','distribution':'Distribution','downstream':'Anwendungen & Systeme','ecosystem':'Forschung, Bildung, Cluster'}
def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:40]
LEGAL=r'\b(gmbh\s*&\s*co\.?\s*kg|ggmbh|gmbh|ag|se|e\.?\s?v\.|b\.?v\.?|n\.?v\.?|s\.?a\.?s\.?|s\.?a\.?|s\.?r\.?l\.?|s\.?r\.?o\.?|ltd\.?|limited|oy|ab|inc\.?|corp\.?|co\.?,?\s*ltd\.?|llc|kg)\b'
SHORT={'X-FAB':'X-FAB','European Semiconductor Manufacturi':'ESMC','Advanced Mask Technology Center':'AMTC','Fraunhofer-Institut für Photonisch':'Fraunhofer IPMS','Fraunhofer-Institut für Elektronis':'Fraunhofer ENAS','Fraunhofer-Institut für Keramische':'Fraunhofer IKTS','Fraunhofer-Institut für Elektronen':'Fraunhofer FEP','Fraunhofer-Institut für Integriert':'Fraunhofer IIS/IZM','Fraunhofer-Institut für Intelligen':'Fraunhofer IAIS','Fraunhofer-Institut für Produktion':'Fraunhofer IPT','Fraunhofer-Institut für Verfahrens':'Fraunhofer IVV','Fraunhofer-Institut für Werkstoff':'Fraunhofer IWS','Fraunhofer-Institut für Werkzeugma':'Fraunhofer IWU','Fraunhofer-Institut für Zuverlässi':'Fraunhofer IZM','Fraunhofer Institut für Integriert':'Fraunhofer IIS','Last Mile Semiconductor':'Last Mile Semi','Silicon Saxony':'Silicon Saxony','Robert Bosch Semiconductor':'Bosch Dresden','GlobalFoundries Dresden':'GlobalFoundries','Infineon Technologies Dresden':'Infineon Dresden','HEIMANN Sensor':'Heimann Sensor','3D-Micromac':'3D-Micromac','Ferroelectric Memory':'FMC','DAS Environmental':'DAS EE','Technische Universität Dresden':'TU Dresden','TU Dresden':'TU Dresden','Helmholtz-Zentrum Dresden':'HZDR','Leibniz-Institut für Festkörper':'IFW Dresden','Hochschule für Technik und Wirtsch':'HTW Dresden','Westsächsische Hochschule':'WHZ Zwickau','Brandenburg University':'BTU Cottbus','Freiberger Compound Materials':'Freiberger CM','Tokyo Electron':'TEL','Lam Research':'Lam Research','Applied Materials':'Applied Materials','SAW COMPONENTS':'SAW Components'}
def short(n):
    for k,v in SHORT.items():
        if n.startswith(k): return v
    s=re.sub(LEGAL,'',n,flags=re.I); s=re.sub(r'\s*[,(|–].*$','',s).strip(' ,.-&')
    s=(s or n)
    if len(s)>22:
        cut=s[:22]; s=cut[:cut.rfind(' ')] if ' ' in cut[8:] else cut
    s=re.sub(r'\s+(und|and|&|for|für|of|de|-)$','',s.strip(' ,.-&'))
    return s.strip(' ,.-&')
def url(u):
    u=(u or '').strip()
    return '' if not u else (u if u.startswith('http') else 'https://'+u)
def tags(t):
    ks=[re.sub(r'\s*\(en\)','',x).strip() for x in (t or '').split('|')]
    ks=[k for k in ks if k and k.lower() not in('semiconductor industry','micro- / nanoelektronics','micro- / nanoelectronics','materials','electronics','software','mechanical engineering','automation')]
    return ks[:6]
LI={'Silicon Saxony':'silicon-saxony','GlobalFoundries Dresden':'globalfoundries','Robert Bosch Semiconductor Manufac':'bosch-semiconductors-and-sensors','X-FAB Semiconductor':'x-fab','European Semiconductor Manufacturi':'esmc-dresden','HEIMANN Sensor':'heimannsensor','Siltronic AG':'siltronic-ag','Novaled':'novaled','3D-Micromac':'3d-micromac-ag','VON ARDENNE':'von-ardenne','Freiberg Instruments':'freiberg-instruments-gmbh','Fabmatics':'fabmatics-gmbh','SEMPA':'sempa-systems','DAS Environmental':'das-environmental-experts','Kontron AIS':'kontronaisgmbh','Ferroelectric Memory':'ferroelectric-memory-company','FaradaIC':'faradaic-sensors-gmbh','Last Mile Semiconductor':'lm-semi','Fraunhofer-Institut für Photonisch':'fraunhofer-ipms','Fraunhofer-Institut für Elektronis':'fraunhofer-enas','Fraunhofer-Institut für Keramische':'fraunhoferikts','NaMLab':'namlab-gmbh','Barkhausen Institut':'barkhausen-institut','Infineon Technologies Dresden':'infineon-technologies','3-5 Power Electronics':'3-5-power-electronics-gmbh','ALLOS Semiconductors':'allos-semiconductors','Freiberger Compound Materials':'freiberger-compound-materials-gmbh','Photronics MZD':'photronics-mzd-gmbh','ALLRESIST':'allresist-gmbh','HQ-Dielectrics':'hq-dielectrics-gmbh','DREEBIT':'dreebit-gmbh','Racyics':'racyics','SAW COMPONENTS':'saw-components-dresden-gmbh','Advanced Mask Technology Center':'advanced-mask-technology-center'}
YT={'Silicon Saxony':'UCeYgs8OL1iLuEAA8nTt83kA','Infineon Technologies Dresden':'UCoTflChMPX0VBFXvXYmcu9w','GlobalFoundries Dresden':'UCzTp5bq9Oylz1QPOw3DFT3g','HEIMANN Sensor':'UCnEuDKDci1G8giQ3pXcTz9w','X-FAB Semiconductor':'UCZVqNluNp8W0Ni9CQ0PTvyQ','Siltronic AG':'UCLaAar8l5kh3ten-Ag1NmSw','Photronics MZD':'UCrvDiBLvJdJvI_SXHCMK79g','Novaled':'UCJWoougdyBG0Fhyx6G6WgUQ','3D-Micromac':'UCI-HLfaix5_l9LYwSWzinJQ','VON ARDENNE':'UC_1vCMlqcrB0VnND6ZhnLsA','Freiberg Instruments':'UC4mz6Hb91CCTTHW278WQD3g','DREEBIT':'UCX1vv8U7YwiDXnDQvlUzQ2Q','HQ-Dielectrics':'UCQLZeFR96KUlVG4DVPdF0zA','Fabmatics':'UC_lEqVo7uY_DSz_Mo_JJz4A','DAS Environmental':'UC3brnNte3BrCgBUCjUy3Caw','Kontron AIS':'UCFPhhlovG57eiXnoEkHNgpA','SEMPA':'UCE0aQdSf-tcJM5jNDFxMq4A','Ferroelectric Memory':'UCwS8QbcXSicNi7UaMwIrBzg','Fraunhofer-Institut für Elektronis':'UCSx8JH3Z-MMPFXoIB2AG8Sw','Fraunhofer-Institut für Photonisch':'UCQIIfGII-_2Xo31XCaBTVEQ','Fraunhofer-Institut für Keramische':'UCuqD8nyRSBEIyH8G4svs6fg','NaMLab':'UCWwLt9Kz-wFJ4BkTfJMY_Fw'}

# IPCEI participation (public sources: Freistaat Sachsen press release 2023, BMWK, European Commission)
SX_MECT='https://www.medienservice.sachsen.de/medien/news/1069594'
EC_MECT='https://ec.europa.eu/commission/presscorner/detail/en/ip_23_3087'
EC_ME='https://ec.europa.eu/commission/presscorner/detail/en/IP_18_6862'
BMWK_ME='https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/M-O/staerkung-mikroelektronik-standort-deutschland-europa-erlaeuterungspapier.pdf'
IPCEI={
 'GlobalFoundries Dresden':[('ME/CT',2023,'Dresden',SX_MECT),('ME',2018,'Dresden',BMWK_ME)],
 'Infineon Technologies Dresden':[('ME/CT',2023,'Dresden',SX_MECT),('ME',2018,'Dresden',BMWK_ME)],
 'Robert Bosch Semiconductor':[('ME/CT',2023,'Dresden',SX_MECT),('ME',2018,'Dresden',BMWK_ME)],
 'Bosch Sensortec':[('ME/CT',2023,'Dresden',SX_MECT)],
 'Ferroelectric Memory':[('ME/CT',2023,'Dresden',SX_MECT)],
 'Freiberger Compound Materials':[('ME/CT',2023,'Freiberg',SX_MECT)],
 'NXP Semiconductors Germany':[('ME/CT',2023,'Dresden',SX_MECT)],
 'Racyics':[('ME',2018,'Dresden',EC_ME)],
 'Advanced Mask Technology Center':[('ME',2018,'Dresden (assoziiert)',EC_ME)],
 '3D-Micromac':[('ME',2018,'Chemnitz (assoziiert)',EC_ME)],
 'X-FAB Semiconductor':[('ME/CT',2023,'Erfurt, Itzehoe',EC_MECT),('ME',2018,'Erfurt, Itzehoe',EC_ME)],
 'Applied Materials':[('ME/CT',2023,'Feldkirchen (assoziiert)',EC_MECT)],
 'mi2-factory':[('ME/CT',2023,'Jena',EC_MECT)],
 'ZEISS':[('ME/CT',2023,'Oberkochen',EC_MECT),('ME',2018,'Oberkochen',EC_ME)],
 'Rohde & Schwarz GmbH':[('ME/CT',2023,'München',EC_MECT)],
}
# ---- place normalisation: "City (CC)" from research city / Silicon Saxony profile city ----
CZ_COUNTRY={'německo':'DE','rakousko':'AT','švýcarsko':'CH','francie':'FR','itálie':'IT','nizozemsko':'NL','belgie':'BE','lucembursko':'LU','dánsko':'DK','švédsko':'SE','finsko':'FI','norsko':'NO','irsko':'IE','velká británie':'GB','spojené království':'GB','usa':'US','izrael':'IL','japonsko':'JP','tchaj-wan':'TW','taiwan':'TW','jižní korea':'KR','korea':'KR','čína':'CN','singapur':'SG','polsko':'PL','česko':'CZ','slovinsko':'SI','chorvatsko':'HR','litva':'LT','lichtenštejnsko':'LI','španělsko':'ES','malajsie':'MY','germany':'DE','austria':'AT','switzerland':'CH','france':'FR','italy':'IT','netherlands':'NL','israel':'IL','japan':'JP','sweden':'SE','finland':'FI','denmark':'DK','ireland':'IE','luxembourg':'LU','slovenia':'SI','croatia':'HR','lithuania':'LT'}
CITY_CC={'vantaa':'FI','espoo':'FI','enschede':'NL','nijmegen':'NL','eindhoven':'NL','leuven':'BE','balzers':'LI','villach':'AT','salzburg':'AT','wallern':'AT','hart bei graz':'AT','bad bleiberg':'AT','st. florian am inn':'AT','feldkirch':'AT','cupertino':'US','fremont':'US','milpitas':'US','anaheim':'US','birmingham':'US','thief river falls':'US','mansfield':'US','hillsboro':'US','singapore':'SG','getxo vizcaya':'ES','villeurbanne':'FR','toulouse':'FR','poitiers':'FR','montbonnot':'FR','lund':'SE','catania':'IT','østervrå':'DK','kaohsiung':'TW','kariya':'JP','seoul':'KR','bucheon':'KR','yongin-si':'KR','ljubljana':'SI','šibenik':'HR','zürich':'CH','bern':'CH','thun':'CH','luxembourg':'LU','vilnius':'LT','yokneam illit':'IL','warsaw':'PL','warszawa':'PL','dublin':'IE','celbridge':'IE','rožnov pod radhoštěm':'CZ','kuala lumpur':'MY','montbonnot-saint-martin':'FR','st. florian':'AT'}
EXONYM={'drážďany':'Dresden','mnichov':'München','berlín':'Berlin','kolín':'Köln','lipsko':'Leipzig','cvikov':'Zwickau','norimberk':'Nürnberg','vídeň':'Wien','curych':'Zürich','lublaň':'Ljubljana','frankfurt nad mohanem':'Frankfurt am Main','halle (saale)':'Halle/Saale'}
def place(research_city,ss_city,fallback_cc='DE'):
    """Return (label, cc). Research city wins; Czech exonyms and country words are normalised; '(pobočka Drážďany)' and similar notes are dropped."""
    raw=(research_city or '').strip()
    if raw and re.search(r"http|www\.",raw): raw=''
    if not raw:
        raw=re.sub(r"[^A-Za-zÄÖÜäöüß .\-()]","",ss_city or '').strip()
        if re.search(r"http|www\.|\.(de|com|org|net|eu|at|ch)\b",raw) or raw.lower()=='sasko': raw=''
    cc=None; city=raw
    # country after comma or in parentheses
    m=re.search(r",\s*([^,()]+)$",city)
    if m and m.group(1).strip().lower() in CZ_COUNTRY: cc=CZ_COUNTRY[m.group(1).strip().lower()]; city=city[:m.start()].strip()
    for pm in re.finditer(r"\(([^)]*)\)",city):
        inner=pm.group(1).strip().lower()
        if inner in CZ_COUNTRY: cc=CZ_COUNTRY[inner]
        elif re.fullmatch(r"[a-z]{2}",inner) and inner.upper() in ('DE','AT','CH','FR','IT','NL','BE','LU','DK','SE','FI','NO','IE','GB','US','IL','JP','TW','KR','CN','SG','PL','CZ','SI','HR','LT','LI','ES','MY'): cc=inner.upper()
        elif inner=='ct': cc='IT'  # Italian province code (Catania)
    # drop explanatory parentheses, keep geographic ones (Saale, Oder, Taunus, Siegerland)
    city=re.sub(r"\s*\((?!saale|oder|taunus|siegerland|durynsko|sasko)[^)]*\)","",city,flags=re.I).strip()
    city=re.sub(r"\s*\((durynsko|sasko)\)","",city,flags=re.I).strip()
    if '/' in city:
        parts=[x.strip() for x in city.split('/') if x.strip()]
        pick=parts[0]
        if any(parts[0].lower()==k or parts[0].lower().startswith(k+' ') for k in CITY_CC):
            for x in parts[1:]:
                xl=EXONYM.get(x.lower(),x).lower()
                if not any(xl==k or xl.startswith(k+' ') for k in CITY_CC): pick=x; cc=cc or 'DE'; break
        city=pick
    city=city.split(',')[0].strip()
    city=re.sub(r"\s*\((saale|oder|taunus|siegerland)\)",lambda mm:'/'+mm.group(1).capitalize(),city,flags=re.I)
    low=city.lower()
    if low in EXONYM: city=EXONYM[low]
    if not cc:
        for k,v in CITY_CC.items():
            if low==k or low.startswith(k+' '): cc=v; break
    if not cc: cc=fallback_cc
    return ((f"{city} ({cc})" if city else cc), cc)
# DE/EN translations of the Czech research profiles (id -> {de:{p,s}, en:{p,s}}); Czech is the fallback
def card(code,name,o2,label):
    t=f"{code} {name}."
    if o2 and o2.get('profile'):
        t+=" "+o2['profile'].strip()
        if not t.endswith(('.', '!', '?')): t+='.'
        if o2.get('products'): t+=f" {label}: {o2['products'].strip()}"
    return t
