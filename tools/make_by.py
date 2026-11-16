"""Bavaria Value Chain Radar – data builder. Reuses the Saxony taxonomy, naming and place helpers from make_sx.py.
Inputs: data/cnsc_research_organisations.json (merged organisations incl. economics), events_by.json (120 events), tr_by_all.json (DE/EN translations).
Output: data/radar_by.json
"""
import json, re, datetime, collections
pilot=json.load(open('data/radar_base.json'))
SRC=None
ns={}
exec(open('tools/shared_taxonomy.py',encoding='utf-8').read(),ns)
CODE,DE_CODE,SEG_DE=ns['CODE'],ns['DE_CODE'],ns['SEG_DE']
slug,short,url,place=ns['slug'],ns['short'],ns['url'],ns['place']
SHORT_BY={'Bayerisches Chip-Design-Center':'BCDC','Bavarian Chips Alliance':'Bavarian Chips Alliance','Bayerisches Staatsministerium':'StMWi Bayern','Technische Universität München':'TUM','Ludwig-Maximilians':'LMU München','Friedrich-Alexander':'FAU Erlangen','Ostbayerische Technische':'OTH Regensburg','Fraunhofer IIS (':'Fraunhofer IIS','Fraunhofer IISB':'Fraunhofer IISB','Fraunhofer EMFT':'Fraunhofer EMFT','Fraunhofer AISEC':'Fraunhofer AISEC','Munich Quantum Valley':'Munich Quantum Valley','Cluster Mechatronik':'Cluster Mechatronik','Sensorik-Bayern':'Sensorik-Bayern','Semiconductor Ideas to the Market':'ITTM','Apple European':'Apple ESDC','TSMC European':'TSMC EUDC','AMD / Xilinx':'AMD Munich','Bosch Semiconductor Design':'Bosch Design Center','Qualcomm CDMA':'Qualcomm Munich','NVIDIA GmbH':'NVIDIA Munich','Micron Semiconductor':'Micron Munich','EverProX':'Silicon Line','Siemens EDA':'Siemens EDA','Keysight':'Keysight','Cadence':'Cadence','Synopsys':'Synopsys','Altair':'Altair (Siemens)','TOPTICA':'TOPTICA','ams-OSRAM':'ams OSRAM','Texas Instruments':'TI Freising','SEMIKRON / Vincotech':'Vincotech','Semikron Danfoss':'Semikron Danfoss','onsemi':'onsemi','STMicroelectronics':'STMicroelectronics','Infineon':'Infineon','Vishay':'Vishay Selb','Rogers Germany':'Rogers curamik','ESK Ceramics':'3M / ESK Ceramics','Schott AG':'SCHOTT','Züblin':'Züblin / Strabag','Avnet Silica':'Avnet / EBV','Bürklin':'Bürklin','Piller Blowers':'Busch Vacuum','HAM-LET':'HAM-LET / UCT','PILLAR':'PILLAR','Pfeiffer Vacuum':'Pfeiffer Vacuum','Leybold':'Leybold','Tokyo Electron':'TEL','Oxford Instruments':'Oxford Instruments','PVA TePla':'PVA TePla','Bruker Nano':'Bruker Nano','Micro-Epsilon Optronic':'Micro-Epsilon Optronic','Micro-Epsilon Messtechnik':'Micro-Epsilon','ASMPT':'ASMPT','Mühlbauer':'Mühlbauer','Rohde & Schwarz':'Rohde & Schwarz','First Sensor':'First Sensor / TE','JENOPTIK':'Jenoptik','WITTENSTEIN':'WITTENSTEIN','Bosch Sensortec':'Bosch Sensortec','SiTime':'SiTime','Sick AG':'SICK','TDK-Micronas':'TDK-Micronas','TRUMPF Photonic':'TRUMPF Photonic','Balluff':'Balluff','Hamamatsu':'Hamamatsu','Excelitas':'Excelitas','Linde GmbH':'Linde','Merck Electronics':'Merck Electronics','Wöllner':'Wöllner','SiC Processing':'SiC Processing','H.C. Carbon':'H.C. Carbon','Kunze Folien':'Kunze Folien','Diotec':'Diotec','Elmos':'Elmos','iC-Haus':'iC-Haus','Microchip':'Microchip','Nexperia':'Nexperia','NXP':'NXP Munich','Renesas':'Renesas Munich','ROHM':'ROHM','Analog Devices':'Analog Devices','CeramTec':'CeramTec','Rauschert':'Rauschert','SGL Carbon':'SGL Carbon','Ebara':'Ebara','Exyte':'Exyte','S+B Reinraumtechnik':'S+B Reinraumtechnik','G+B Photonik':'G+B Photonik','Faulhaber':'Faulhaber','KUKA':'KUKA','MAXON':'maxon','Schunk':'SCHUNK','Kontron':'Kontron','TQ-Systems':'TQ-Systems','Zollner':'Zollner','Arrow':'Arrow','Mouser':'Mouser','Spezial-Electronic':'Spezial-Electronic','Wolfspeed':'Wolfspeed','Sinelec':'Sinelec','Chipglobe':'Chipglobe','IC-Design Noris':'IC-Design Noris','ASIC GmbH':'ASIC GmbH','Quintauris':'Quintauris','Codasip':'Codasip','Rambus':'Rambus','Arm Germany':'Arm','Broadcom':'Broadcom','Vector Informatik':'Vector','camLine':'camLine','GenISys':'GenISys','KLA-Tencor':'KLA','Lauterbach':'Lauterbach','PDF Solutions':'PDF Solutions','TASKING':'TASKING','nextnano':'nextnano','Applied Materials':'Applied Materials','InnoLas':'InnoLas','Lam Research':'Lam Research','SUSS':'SUSS MicroTec','SCREEN':'SCREEN SPE','attocube':'attocube','confovis':'confovis','Park Systems':'Park Systems','senswork':'senswork','Advantest':'Advantest','ERS electronic':'ERS electronic','finetech':'finetech','FormFactor':'FormFactor','Teradyne':'Teradyne','VX Instruments':'VX Instruments','VAT Deutschland':'VAT','Bürkert':'Bürkert','GEMÜ':'GEMÜ','Siltronic':'Siltronic','Wacker':'Wacker Chemie','Melexis':'Melexis','Sensirion':'Sensirion','InfraTec':'InfraTec','LAPP Insulators':'LAPP Insulators','Kontron Europe':'Kontron'}
def short_by(n):
    for k,v in SHORT_BY.items():
        if n.startswith(k): return v
    return short(n)
rows=json.load(open('data/cnsc_research_organisations.json')); events=json.load(open('data/cnsc_research_events.json'))
TR=json.load(open('data/translations_de_en.json')); TP,TE=TR['profiles'],TR['events']
TODAY=datetime.date(2026,11,16)
BI=json.load(open('data/bca_membership_ipcei.json')); BCA=BI['bca']; IPC=BI['ipcei']; BSRC=BI['_sources']
IPU={'ME/CT':BSRC['ipcei_mect']['url'],'ME':BSRC['ipcei_me']['url']}
# ---- economics value normalisation (light; numbers stay as given)
REP={'de':[('Veřejně obchodovaná','Börsennotierte'),('veřejně obchodovaná','börsennotierte'),('dceriná spol.','Tochtergesellschaft'),('Dceřiná spol.','Tochtergesellschaft'),('dceřiná spol.','Tochtergesellschaft'),('Dceřiná společnost','Tochtergesellschaft'),('dceřiná společnost','Tochtergesellschaft'),('Nezávislá soukromá','Unabhängige private'),('soukromá společnost','Privatunternehmen'),('soukromá','privat'),('Veřejnoprávní výzkumný ústav','Öffentlich-rechtliches Forschungsinstitut'),('Veřejná univerzita','Staatliche Universität'),('Svobodný stát Bavorsko','Freistaat Bayern'),('neveřejná AG','nicht börsennotierte AG'),('rodinné / zakladatelské vlastnictví','Familien-/Gründerbesitz'),('rodinné','Familienbesitz'),('Součást','Teil von'),('součást','Teil von'),('Divize','Sparte'),('divize','Sparte'),('skupina','Gruppe'),('skupiny','Gruppe'),('Privátní/institucionální investoři','Private/institutionelle Investoren'),('kotovaná','börsennotiert'),('Mittelstand','Mittelstand'),('globálně','weltweit'),('celosvětově','weltweit'),('lokálně','lokal'),('odhad','Schätzung'),('rozpočet','Budget'),('mil. ','Mio. '),('mld. ','Mrd. '),('tis. ','Tsd. '),('cca ','ca. '),('Mnichov','München'),('Řezno','Regensburg'),('Norimberk','Nürnberg'),('Bavorsko','Bayern'),('v DE','in DE'),('zaměstnanců','Beschäftigte'),('zaměstnanci','Beschäftigte'),('Firemní web','Firmenwebsite'),('Firemní zdroje','Unternehmensangaben'),('Rejstřík','Handelsregister'),('výroční zpráva','Geschäftsbericht'),('Výroční zpráva','Geschäftsbericht')],
'en':[('Veřejně obchodovaná','Listed'),('veřejně obchodovaná','listed'),('dceriná spol.','subsidiary'),('Dceřiná spol.','Subsidiary'),('dceřiná spol.','subsidiary'),('Dceřiná společnost','Subsidiary'),('dceřiná společnost','subsidiary'),('Nezávislá soukromá','Independent private'),('soukromá společnost','private company'),('soukromá','private'),('Veřejnoprávní výzkumný ústav','Public research institute'),('Veřejná univerzita','Public university'),('Svobodný stát Bavorsko','Free State of Bavaria'),('neveřejná AG','unlisted AG'),('rodinné / zakladatelské vlastnictví','family/founder owned'),('rodinné','family-owned'),('Součást','Part of'),('součást','part of'),('Divize','Division'),('divize','division'),('skupina','group'),('skupiny','group'),('Privátní/institucionální investoři','Private/institutional investors'),('kotovaná','listed'),('Mittelstand','Mittelstand'),('globálně','global'),('celosvětově','global'),('lokálně','local'),('odhad','estimate'),('rozpočet','budget'),('mil. ','million '),('mld. ','billion '),('tis. ','k '),('cca ','approx. '),('Mnichov','Munich'),('Řezno','Regensburg'),('Norimberk','Nuremberg'),('Bavorsko','Bavaria'),('v DE','in DE'),('zaměstnanců','employees'),('zaměstnanci','employees'),('Firemní web','company website'),('Firemní zdroje','company sources'),('Rejstřík','register'),('výroční zpráva','annual report'),('Výroční zpráva','Annual report')]}
def tr_val(s,lang):
    if not s: return ''
    for a,b in REP[lang]: s=s.replace(a,b)
    return s
def rel_of(s):
    s=(s or '').lower()
    if s.startswith('verified') and 'estimated' in s: return 'mixed'
    if s.startswith('verified'): return 'verified'
    if s.startswith('estimated'): return 'estimated'
    return ''
# ---- members
members=[]; ids=set(); byid={}
def sortkey(c): return tuple(int(x) if x.isdigit() else {'D':90,'F':91,'X':99}.get(x,95) for x in re.findall(r'\d+|[DFX]',c)) or (999,)
rows.sort(key=lambda r:(sortkey(r['code']),r['name'].lower()))
def card(code,name,p,s,label):
    t=f"{code} {name}."
    if p:
        t+=" "+p.strip()
        if not t.endswith(('.', '!', '?')): t+='.'
        if s: t+=f" {label}: {s.strip()}"
    return t
for r in rows:
    code=r['code']; cs_n,en_n,sec=CODE[code]; i=r['id']; ids.add(i)
    t=TP.get(i,{})
    de_p,de_s=(t.get('de',{}).get('p',''),t.get('de',{}).get('s','')) if t else ('','')
    en_p,en_s=(t.get('en',{}).get('p',''),t.get('en',{}).get('s','')) if t else ('','')
    city,cc=place(r['city'],'')
    eco=None
    if r.get('legal') or r.get('rev') or r.get('emp_by'):
        eco={'legal':{'cs':r['legal'],'de':tr_val(r['legal'],'de'),'en':tr_val(r['legal'],'en')},'emp_by':{'cs':r['emp_by'],'de':tr_val(r['emp_by'],'de'),'en':tr_val(r['emp_by'],'en')},'emp_g':{'cs':r['emp_g'],'de':tr_val(r['emp_g'],'de'),'en':tr_val(r['emp_g'],'en')},'rev':{'cs':r['rev'],'de':tr_val(r['rev'],'de'),'en':tr_val(r['rev'],'en')},'rel':rel_of(r['rel']),'relraw':r['rel'],'note':r['enote']}
    conf={'high':'high','to verify':'to verify','medium':'to verify','uncertain':'uncertain'}.get((r['conf'] or '').lower(),'to verify' if not r['profile'] else 'high')
    m={"id":i,"n":r['name'],"short":short_by(r['name']),"city":city,"cc":cc,"url":url(r['web']),"s":sec,"acadChip":False,"partnerIn":[],
       "cs":card(code,cs_n,r['profile'],r['products'],'Produkty a služby'),"en":card(code,en_n,en_p or r['profile'],en_s or r['products'],'Products and services'),"de":card(code,DE_CODE.get(code,en_n),de_p or r['profile'],de_s or r['products'],'Produkte und Dienstleistungen'),
       "conf":conf,"logo":"","li":"","yt":"","ipcei":[],"note":r.get('note',''),"verified":bool(r['profile']),"liScope":"","liFilter":"","offer":{},"ver":1 if conf=='high' else 0,"code":code,"raw":r['raw'],"eco":eco}
    b=BCA.get(i)
    m['bca']=b['c'] if b else ''
    m['bcaAs']=b['as'] if b else ''
    m['bcaT']=b['t'] if b else ''
    m['ssm']=bool(b)   # dashed on the map = not in the BCA competence map
    m['ipcei']=[{"p":x['p'],"y":x['y'],"s":(x['ent']+' – '+x['s']),"u":IPU[x['p']],"by":x['by'],"ent":x['ent'],"sites":x['s']} for x in IPC.get(i,[])]
    members.append(m); byid[i]=m
# ---- news from events
def ntype(t):
    t=t or ''
    if 'Finanční výsledky' in t or 'Výsledky Q' in t or 'Kapitálový' in t or 'Finanční kalendář' in t: return 'finance'
    if 'M&A' in t or 'Akvizice' in t or 'Investice' in t or 'Expanze' in t or 'Restrukturalizace' in t: return 'invest'
    if 'Partnerství' in t: return 'partner'
    if 'Ocenění' in t or 'Grant' in t: return 'award'
    if 'Vedení' in t: return 'people'
    if 'Projekty' in t or 'Infrastruktura' in t or 'Projekt' in t: return 'project'
    if 'Produkt' in t or 'Technologie' in t or 'Software' in t or 'průlom' in t.lower() or 'Integrace' in t or 'Portfolio' in t: return 'launch'
    if 'Video' in t: return 'media'
    return 'event'
def skind(st):
    return {'Company newsroom / press release':'press','Trade fair / conference':'fair','YouTube / video':'youtube','LinkedIn':'linkedin','Institute / university website':'web'}.get(st,'web')
TOP={'e007','e010','e031','e055','e061','e066','e014','e032','e017'}
N=[]; skipped=[]
for v in events:
    if v['type'].startswith('Bez nové'): skipped.append(v['eid']); continue
    mid=v['mid']
    if mid not in byid: print('event member missing',v['name']); continue
    t=TE[v['eid']]
    N.append({"d":v['date'],"a":False,"m":[mid],"ty":ntype(v['type']),"src":skind(v['stype']),"top":v['eid'] in TOP,"cs":v['text'],"en":t['en'],"de":t['de'],"u":v['url1'],"sn":v['sname'],"tyraw":v['type']})
N.sort(key=lambda n:n['d'],reverse=True)
# ---- Termine (upcoming, taken from the event texts)
def M(prefix):
    for m in members:
        if m['n'].startswith(prefix): return m['id']
    raise SystemExit('no member '+prefix)
EV=[
 {"d":"2026-11-17","end":"2026-11-18","when":{"cs":"17.–18. 11. 2026","en":"17–18 Nov 2026","de":"17.–18. 11. 2026"},"m":[M('IC-Design Noris')],"cs":"DVCon Europe 2026, Mnichov – konference o návrhu a verifikaci","en":"DVCon Europe 2026, Munich – design and verification conference","de":"DVCon Europe 2026, München – Konferenz zu Entwurf und Verifikation"},
 {"d":"2026-11-18","end":"2026-11-19","when":{"cs":"18.–19. 11. 2026","en":"18–19 Nov 2026","de":"18.–19. 11. 2026"},"m":[M('Micro-Epsilon Messtechnik')],"cs":"Präzisionsmesse 2026 – Micro-Epsilon vystavuje","en":"Präzisionsmesse 2026 – Micro-Epsilon exhibits","de":"Präzisionsmesse 2026 – Micro-Epsilon stellt aus"},
 {"d":"2026-11-24","end":"2026-11-24","when":{"cs":"24. 11. 2026","en":"24 Nov 2026","de":"24. 11. 2026"},"m":[M('TSMC European')],"cs":"TSMC OIP Europe 2026, Mnichov – fórum designového ekosystému","en":"TSMC OIP Europe 2026, Munich – design ecosystem forum","de":"TSMC OIP Europe 2026, München – Forum des Designökosystems"},
 {"d":"2026-11-24","end":"2026-11-24","when":{"cs":"24. 11. 2026","en":"24 Nov 2026","de":"24. 11. 2026"},"m":[M('Microchip')],"cs":"Microchip: výsledky za Q4 FY26","en":"Microchip: Q4 FY26 results","de":"Microchip: Ergebnisse Q4 FY26"},
 {"d":"2026-11-24","end":"2026-11-26","when":{"cs":"24.–26. 11. 2026","en":"24–26 Nov 2026","de":"24.–26. 11. 2026"},"m":[M('Micro-Epsilon Messtechnik'),M('Sensirion'),M('Sensorik-Bayern')],"cs":"SPS 2026, Norimberk – veletrh automatizace","en":"SPS 2026, Nuremberg – automation trade fair","de":"SPS 2026, Nürnberg – Automatisierungsmesse"},
 {"d":"2026-11-25","end":"2026-11-25","when":{"cs":"25. 11. 2026","en":"25 Nov 2026","de":"25. 11. 2026"},"m":[M('Sensorik-Bayern')],"cs":"Strategiedialog Automotive Regensburg 2026, TechBase Regensburg","en":"Strategiedialog Automotive Regensburg 2026, TechBase Regensburg","de":"Strategiedialog Automotive Regensburg 2026, TechBase Regensburg"},
 {"d":"2026-11-25","end":"2026-11-25","when":{"cs":"25. 11. 2026","en":"25 Nov 2026","de":"25. 11. 2026"},"m":[M('Fraunhofer IISB')],"cs":"Fokusgruppe Energiespeicher, Erlangen (Fraunhofer IISB)","en":"Fokusgruppe Energiespeicher, Erlangen (Fraunhofer IISB)","de":"Fokusgruppe Energiespeicher, Erlangen (Fraunhofer IISB)"},
]
# ---- segments, types, source kinds, meta
SEG=[dict(x) for x in pilot['segments']]+[{"id":"downstream","code":"09","cs":"Aplikace a systémy","en":"Applications & systems","c":{"l":"#64748B","d":"#94A3B8"}},{"id":"ecosystem","code":"10","cs":"Výzkum, vzdělávání, klastry","en":"Research, skills & clusters","c":{"l":"#0891B2","d":"#22D3EE"}}]
for x in SEG: x['de']=SEG_DE[x['id']]
TYPES=[dict(t) for t in pilot['types']]+[{"id":"media","cs":"Podcast / video","en":"Podcast / video","de":"Podcast / Video"},{"id":"finance","cs":"Finanční výsledky","en":"Financial results","de":"Finanzergebnisse"}]
SRCK=[dict(x) for x in pilot['sourcesKinds']]+[{"id":"youtube","cs":"YouTube kanál firmy","en":"Company YouTube channel","de":"YouTube-Kanal des Unternehmens"},{"id":"fair","cs":"Veletrh / konference","en":"Trade fair / conference","de":"Messe / Konferenz"}]
for x in SRCK:
    if x['id']=='press': x.update({"cs":"Tisková zpráva / newsroom firmy","en":"Company newsroom / press release","de":"Pressemitteilung / Newsroom des Unternehmens"})
    if x['id']=='web': x.update({"cs":"Web firmy nebo instituce","en":"Company or institute website","de":"Website des Unternehmens oder Instituts"})
cnt=collections.Counter(m['s'] for m in members); codes=collections.Counter(m['code'] for m in members)
n_bca=sum(1 for m in members if m['bca']); n_bcap=sum(1 for m in members if m['bca']=='partner'); n_ipc=sum(1 for m in members if m['ipcei']); n_eco=sum(1 for m in members if m['eco']); n_prof=sum(1 for m in members if m['verified']); doms=len(set(re.sub(r'^https?://(www\.)?','',n['u']).split('/')[0] for n in N if n['u']))
meta=dict(pilot['meta'])
meta.update({"edition":"W46/2026","updated":"2026-11-16",
 "title":{"cs":"Radar polovodičového hodnotového řetězce – Bavorsko (náhled)","en":"Semiconductor Value Chain Radar – Bavaria (preview)","de":"Radar der Halbleiter-Wertschöpfungskette – Bayern (Vorschau)"},
 "lede":{"cs":"Co firmy a instituce bavorského polovodičového ekosystému zveřejňují, od návrhu čipů přes zařízení, subsystémy a materiály po výrobu, výzkum a distribuci – doplněno o základní ekonomické údaje. Seznam organizací a jejich zařazení do taxonomie CNSC vychází z rešerše CNSC ve veřejných zdrojích a je pracovní.",
  "en":"What companies and institutes in the Bavarian semiconductor ecosystem publish, from chip design through equipment, subsystems and materials to fabrication, research and distribution – with basic economic data. The organisation list and its classification into the CNSC taxonomy come from CNSC research in public sources and are provisional.",
  "de":"Was Unternehmen und Institute des bayerischen Halbleiter-Ökosystems veröffentlichen, vom Chipdesign über Anlagen, Subsysteme und Materialien bis zu Fertigung, Forschung und Distribution – ergänzt um wirtschaftliche Eckdaten. Die Liste der Organisationen und ihre Zuordnung zur CNSC-Taxonomie stammen aus CNSC-Recherchen in öffentlichen Quellen und sind vorläufig."},
 "banner":{"cs":f"Pracovní náhled, edice W46/2026 (16. 11. 2026). {len(members)} organizací z rešerše CNSC ({n_prof} s firemním profilem, {n_eco} s ekonomickými údaji, {n_bca} v Kompetenzatlasu Bavarian Chips Alliance – z toho {n_bcap} partnerů, {n_ipc} s účastí v IPCEI ME/ME-CT), {len(N)} záznamů aktivit za říjen–listopad 2026 ze {doms} veřejných zdrojů (firemní newsroomy, veletrhy electronica a SEMICON Europa 2026). Neveřejná pracovní verze, zařazení čeká na ověření s bavorskými partnery.",
  "en":f"Working preview, edition W46/2026 (16 Nov 2026). {len(members)} organisations from CNSC research ({n_prof} with a company profile, {n_eco} with economic data, {n_bca} in the Bavarian Chips Alliance competence map – {n_bcap} of them partners, {n_ipc} with IPCEI ME/ME-CT participation), {len(N)} activity items for October–November 2026 from {doms} public sources (company newsrooms, the electronica and SEMICON Europa 2026 trade fairs). Non-public working version; classification awaits review with Bavarian partners.",
  "de":f"Arbeitsvorschau, Ausgabe W46/2026 (16. 11. 2026). {len(members)} Organisationen aus CNSC-Recherche ({n_prof} mit Unternehmensprofil, {n_eco} mit Wirtschaftsdaten, {n_bca} im Kompetenzatlas der Bavarian Chips Alliance – davon {n_bcap} Partner, {n_ipc} mit IPCEI-ME/ME-KT-Beteiligung), {len(N)} Aktivitätseinträge für Oktober–November 2026 aus {doms} öffentlichen Quellen (Unternehmens-Newsrooms, Messen electronica und SEMICON Europa 2026). Nicht öffentliche Arbeitsversion; die Zuordnung wartet auf die Prüfung mit bayerischen Partnern."}})
src=[["CNSC-Recherche in öffentlichen Quellen / rešerše CNSC (Unternehmenswebsites, Presse, Register), 5 Chargen, 16. 11. 2026","https://www.semicz.cz"],
["Wirtschaftsdaten: Geschäftsberichte, 10-K/IR-Veröffentlichungen, Bundesanzeiger, Handelsregister (4 Chargen, 16. 11. 2026) / ekonomika: výroční zprávy, rejstříky","https://www.bundesanzeiger.de"],
["Unternehmens-Newsrooms und Pressemitteilungen (öffentlich) / firemní newsroomy – Direktlinks bei jeder Meldung","https://www.semicz.cz"],
["electronica 2026 und SEMICON Europa 2026, München, 10.–13. 11. 2026 (Aussteller- und Programmseiten) / veletrhy","https://electronica.de"],
[BSRC['bca']['name']+" / Kompetenzatlas BCA – klasifikace členství",BSRC['bca']['url']],
[BSRC['ipcei_mect']['name']+" / seznam německých účastníků IPCEI ME/CT",BSRC['ipcei_mect']['url']],
[BSRC['ipcei_karte']['name'],BSRC['ipcei_karte']['url']],
[BSRC['ipcei_ast']['name']+" / IPCEI AST: účastníci dosud nezveřejněni, proto v radaru nezobrazeni",BSRC['ipcei_ast']['url']],
["CNSC-Taxonomie der Wertschöpfungskette v1.2","https://www.semicz.cz"]]
d={"meta":meta,"segments":SEG,"rings":pilot['rings'],"types":TYPES,"sourcesKinds":SRCK,"members":members,"centres":[],"news":N,"events":EV,"sources":src}
json.dump(d,open('data/radar_by.json','w'),ensure_ascii=False)
print('members',len(members),sorted(cnt.items(),key=lambda x:-x[1]),'news',len(N),'skipped',skipped,'events',len(EV))
print('codes',sorted(codes.items(),key=lambda x:sortkey(x[0])))
print('types',collections.Counter(n['ty'] for n in N),'src',collections.Counter(n['src'] for n in N))
print('bca',n_bca,'partners',n_bcap,'ipcei',n_ipc,[m['id'] for m in members if m['ipcei']]);print('eco',n_eco,'profiles',n_prof,'cc',collections.Counter(m['cc'] for m in members))
