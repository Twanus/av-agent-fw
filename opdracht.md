# Eindopdracht Python: Agent Framework

### Doel

Ontwikkel een flexibel systeem-agent framework in Python met GitHub-integratie. De agent moet in staat zijn beheertaken op te halen uit een GitHub-repository en deze autonoom uit te voeren.

### Belangrijke Opmerkingen

- Het project is gericht op systeembeheer automatisering
- Test in een gecontroleerde ontwikkelomgeving
- Volg security best practices
- Documenteer alle functionaliteit zorgvuldig
- Geen plagiaat; ethisch gebruik van ChatGPT
- Reflecties in Markdown

## Planning

### **Week 1: Analyse en Conceptvorming (deadline: 4 december)**

#### **Theoretische analyse**

##### **Doelen van systeem-agents**

1. **Automatisering**: Het verminderen van handmatige interventie bij routinetaken zoals back-ups, systeemupdates en monitoring, wat leidt tot verhoogde efficiëntie en minder menselijke fouten.

2. **Consistentie**: Het waarborgen van uniforme uitvoering van taken volgens vooraf gedefinieerde regels en procedures.

3. **Realtime Monitoring**: Het continu monitoren van systeemprestaties en het proactief reageren op incidenten om downtime te minimaliseren.

4. **Schaalbaarheid**: Het faciliteren van eenvoudige opschaling binnen complexe IT-omgevingen zonder verlies van performance.

5. **Beveiliging**: Het implementeren van beveiligingsmaatregelen zoals regelmatige updates en het monitoren van verdachte activiteiten.

##### **Agents vs Services vs Daemons**

| Kenmerk   | Agents                                                                                      | Services                                                                                          | Daemons                                                                      |
| --------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Definitie | Kleine programma’s die specifieke taken uitvoeren en vaak met andere systemen communiceren. | Processen die een systeemfunctie bieden en kunnen worden beheerd (starten, stoppen, controleren). | Achtergrondprocessen die continu draaien en systeemfunctionaliteiten bieden. |
| Voorbeeld | Wazuh agent                                                                                 | systemd service zoals ssh.service                                                                 | mysqld (MySQL-daemon)                                                        |
| Werking   | Worden vaak op afstand beheerd en richten zich op specifieke taken.                         | Kunnen handmatig of automatisch worden gestart en gestopt.                                        | Draaien continu zonder directe tussenkomst, bedoeld voor langdurige taken.   |
| Gebruik   | Monitoring, data-aggregatie, beveiliging.                                                   | Applicatie- of systeembeheer.                                                                     | Voortdurende bewaking en systeembeheer.                                      |
| Beheer    | Communicatie met centrale systemen, soms geïntegreerd met dashboards.                       | Lokaal of via command-line tools zoals systemctl.                                                 | Worden beheerd via lokale configuratiebestanden of managementtools.          |

##### **Relevantie binnen systeembeheer**

In hedendaagse IT-infrastructuren zijn systeem-agents essentieel voor:

- **DevOps**: Ondersteuning van CI/CD door automatisering van build, test en deploy processen.

- **Infrastructuur as Code (IaC)**: Beheer van infrastructuur met geautomatiseerde scripts en configuraties.

- **Beveiligingsbeheer**: Proactieve detectie en mitigatie van beveiligingsdreigingen.

##### **Security overwegingen**

Beveiliging is een cruciaal aspect van systeembeheer en moet in elke fase van het ontwikkelingsproces worden geïntegreerd. Het omvat niet alleen het beschermen van systemen tegen aanvallen, maar ook het waarborgen van de integriteit, vertrouwelijkheid en beschikbaarheid van gegevens.

Het is nuttig om te kijken naar hoe tools zoals Ansible werken en welke best practices daar gelden:

- **Communicatie over Beveiligde Kanalen**: Ansible maakt gebruik van beveiligde protocollen zoals SSH voor communicatie met remote hosts, waardoor de kans op afluisteren of man-in-the-middle-aanvallen wordt verminderd.

- **Geen Permanente Agents**: In tegenstelling tot sommige andere tools, installeert Ansible geen permanente agents op de beheerde nodes, wat het aanvalsoppervlak verkleint.

- **Minimale Rechten**: Het principe van ‘least privilege’ wordt toegepast door alleen de minimale vereiste toegang te geven voor het uitvoeren van taken. Dit vermindert het risico als een account wordt gecompromitteerd.

- **Credential Management**: Ansible adviseert het gebruik van veilige methoden voor het beheren van credentials, zoals Ansible Vault voor het versleutelen van gevoelige gegevens.

- **Idempotentie**: Door ervoor te zorgen dat taken idempotent zijn, wordt voorkomen dat dezelfde wijzigingen meerdere keren worden toegepast, wat de systeemstabiliteit ten goede komt.

- **Logging en Auditing**: Het bijhouden van gedetailleerde logs van uitgevoerde acties helpt bij het auditen en het snel identificeren van potentiële beveiligingsincidenten.

In de context van ons agent framework moeten vergelijkbare security best practices worden gevolgd:

- **Versleutelde Communicatie**: Alle communicatie tussen de agent en de GitHub-repository is beveiligd.

- **Authenticatie en Autorisatie**: Sterke authenticatiemechanismen om ongeautoriseerde toegang te voorkomen, en beperkte acties op basis van gebruikersrechten.

- **Veilig Opslaan van Gevoelige Gegevens**: Veilige methoden voor het opslaan van tokens, API-sleutels en andere gevoelige informatie.

- **Regelmatige Updates**: De agent en alle gebruikte libraries up-to-date houden om bekende kwetsbaarheden te mitigeren.

- **Input Validatie**: Validatie van alle externe input om beveiligingsproblemen zoals injectie-aanvallen te voorkomen.

- **Code Signing**: Eventueel het gebruik van code signing voor modules om ervoor te zorgen dat alleen vertrouwde code wordt uitgevoerd.

#### **Technische analyse**

##### **Architectuur van het Agent Framework**

Het doel is een modulair en uitbreidbaar agent-framework te bouwen dat beheertaken automatiseert door modules op te halen en uit te voeren vanuit een GitHub-repository.

###### **1. Core Agent**

Functie:

- Communiceert met GitHub om modules en configuraties op te halen.
- Laadt en voert modules uit volgens geplande taken of triggers.
- Logging en monitoring voor auditing en foutopsporing.
- Voert beveiligingscontroles uit (code signing en inputvalidatie).

Technologieën:

- Python 3.x: Voor de ontwikkeling van de agent vanwege de brede ondersteuning en beschikbare libraries.
- GitHub API (PyGithub): Voor interactie met de GitHub-repository.
- Logging Module: Gebruik van Python’s ingebouwde logging module.

###### **2. Module Systeem**

Functie:

- Plug-ins die specifieke taken uitvoeren, zoals systeemmonitoring, back-ups, installatie van software, etc.

Kenmerken:

- Standaard Interface: Elke module implementeert een voorgedefinieerde interface met bijvoorbeeld een execute() methode.
- Isolatie: Modules draaien in een gecontroleerde omgeving om systeemveiligheid te waarborgen.
- Versiebeheer: Modules worden versiebeheer via GitHub, wat updates en rollbacks mogelijk maakt.

Technologieën:

- Dynamic Importing: Gebruik van Python’s importlib om modules dynamisch te laden.
- venv: Voor het isoleren van module-afhankelijkheden.

###### **3. GitHub Integratie**

Functie:

- De agent synchroniseert met een GitHub-repository om modules en configuraties op te halen.

Implementatie:

- Authenticatie: Via een Personal Access Token (PAT) met minimale vereiste scopes.
- Bestandsstructuur:
  ```folder
    - config/
    - data/
    - modules/
  ```
- Periodieke sync: Agent controleert op nieuwe updates op vooraf ingestelde intervallen.

###### **4. Beveiliging**

Maatregelen:

- Versleutelde Communicatie: Alle communicatie met GitHub is beveiligd.
- Code Signing van Modules: Implementatie van code signing om de integriteit en authenticiteit van modules te waarborgen.
- Least Privilege: De agent draait met minimale systeemrechten.
- Input Validatie: Alle externe input wordt gevalideerd om injectie-aanvallen te voorkomen.
- Sandboxing: Overwegen van het gebruik van containers of virtuele omgevingen voor module-executie.

Technologieën:

- Cryptography: Voor het implementeren van code signing en encryptie.
- OS: gebruik makend van user & admin privileges.

###### **5. Configuratie Management**

Functie: Beheer van instellingen en parameters voor zowel de agent als de modules.

Implementatie:

- Configuratiebestanden: In YAML- of JSON-formaat binnen de config/ map.
- Prioriteit: Lokale configuraties kunnen globale instellingen overschrijven.

Technologieën:

- PyYAML of json: Voor het parsen van configuratiebestanden.

###### **6. Scheduling en Task Management**

Functie: Beheer van wanneer en hoe vaak modules worden uitgevoerd.

Implementatie:

- Geplande Taken: Scheduler om modules op specifieke tijden of intervallen uit te voeren.
- Ad-hoc Uitvoering: Mogelijkheid om modules direct uit te voeren bij behoefte.

Technologieën:

- Scheduler: Voor eenvoudige planning van taken.

###### **7. Data Opslag**

Functie: Opslag van output, logs en tijdelijke bestanden.

Implementatie:

- Data Directory: Gebruik van de data/ map voor gestructureerde opslag.
- Rotating Logs: Implementatie van logrotatie om opslagruimte te beheren.

Technologieën:

- Logging: Voor het loggen van informatie.
- OS: Voor het beheer van bestandslocaties.

###### **8. Logging en Monitoring**

Functie: Bijhouden van activiteiten voor auditing en foutopsporing.

Implementatie:

- Gestandaardiseerd Logformaat: Voor consistentie en eenvoud in loganalyse.
- Logging Levels: Gebruik van verschillende niveaus (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Technologieën:

- Python’s logging module: Voor flexibele en configureerbare logging.

##### **Dependencies**

- Python 3.x: Hoofdprogrammeertaal.
- PyGithub: Voor GitHub API interactie.
- cryptography: Voor encryptie en code signing.
- PyYAML / json: Voor configuratiebeheer.
- Schedule: Voor taakplanning.
- venv: Voor omgeving-isolatie.
- Unit Testing Frameworks: Zoals unittest of pytest voor het schrijven van tests.

### **Project Planning**

#### 1. **Project Setup**:

- Github repo aanmaken
- ci/cd pipeline aanmaken
- venv samenstellen

#### 2. **Core Agent Ontwikkelen**:

- GitHub-authenticatie
- Module loader
- Scheduler
- Logging

#### 3. **Beveiligingsfuncties Implementeren**:

- Code signing
- Inputvalidatie
- Minimale rechten

#### 4. **Configuratiebeheer**:

- Definieer het formaat voor configuratiebestanden.
- Implementeer functionaliteit om configuraties te laden en te herladen.

#### 5. **Module Ontwikkeling**:

- Ontwikkel minimaal drie custom modules, bijvoorbeeld:
  - Systeemmonitor
  - Back-up
  - Log Analyzer
- Zorg dat elke module voldoet aan de standaard interface.

#### 6. **Testing**:

- Unittests
- Integratietests
- Beveiligingsfuncties

#### 7. **Documentatie**:

- Docstrings
- Handleidingen
- Beveiligingsmaatregelen

#### 8. **Deployment in Gecontroleerde Omgeving**:

- Testomgeving op vmware
- Host-only netwerk
- Bridged via pfSense

#### **Uitdagingen en Overwegingen**

- **Veiligheid**: API-tokens, input validatie
- **Betrouwbaarheid**: Fouttolerantie, exception handling, rollback
- **Uitbreidbaarheid**: Makkelijk nieuwe modules toevoegen.
- **Prestaties**: Minimaliseer de impact indien mogelijk.

#### **Toekomstige Uitbreidingen**

- **Web Dashboard**: Real-time monitoring en beheer.
- **Machine Learning Integratie**: Geavanceerde analyse van de logs.
- **Distributed Agents**: Centraal beheer van meerdere agents.

### Week 2-4: Ontwikkeling (tussentijdse deadlines: 11 en 18 december)

#### Basisfunctionaliteit

1. GitHub-Repository structuur:

   - config/
   - data/
   - modules/

2. Agent-framework vereisten:
   - GitHub API integratie
   - Module loader
   - Gecontroleerde scheduling

#### Custom Modules (kies 3)

- System Monitor module
- Backup module
- Log Analyzer module
- Update Manager module
- Resource Monitor
- Configuration Management Module

### Week 4: Afronding (deadline: 20 december)

- Testing
- Eindreflectie
- Documentatie

## Eindproducten

1. Code
2. GitHub repository (private)
3. Reflectieverslag + Demo video (max 3min)
