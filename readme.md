# Progetto "Linguaggi di descrizione dell' hardware"
##### Gregorelli Mirko, Intini Francesco, Luchiari Simone


## Richiesta
Prototipare uno strumento previsto di G.U.I. che permetta di velocizzare la creazione di un VHDL **strutturale** con particolare enfasi sulla creazione delle mappature.

**Nota:** Non è richiesto un applicativo funzionante

### Approccio al problema
Data la richiesta di un applicativo previsto di GUI si è deciso di sviluppare una web app, data la relativa semplicità di programmazione rispetto allo sviluppo di un applicativo desktop.

Come principale linguaggio con cui sviluppare il progetto si è scelto il python, con precisione Python 3.7.5, mentre per gestire le richieste web si è deciso di utilizzare il framework **'Django'**. L'interfaccia web si basa sul classico stack tecnologico del web: HTML5, ES6 e CSS5. Come database per il backend è stato utilizzato SQLITE3.

## Setup ambiente locale per testare il progetto

- Installare python 3.7

*(se in ambiente Debian/Ubuntu)*

``` shell
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3
```

- Installare pypi (gestore dei pacchetti di python)

```shell
sudo apt install python3-pip -y
```

- Installare pipenv (modulo di python per la gestione degli ambienti di sviluppo)

```shell
pip3 install --user pipenv
```
- Accedere alla cartella del progetto e lanciare i seguenti comandi

```shell
pipenv shell
pipenv install django
```
**Ora è possibile lanciare il progetto con il seguente comando**

```shell
python manage.py runserver
```
**la web app è raggiungibile all'indirizzo 'https://localhost:8000'**

## Relazione sull'applicativo

### NOTA:
Non saranno riportate le informazioni inerenti al puro sviluppo della web-app in quanto il numero di righe di codice da coprire diventerebbe esorbitante, il focus sarà unicamente sul flow che porta alla creazione del VHDL strutturale.

## Descrizione del flow
Per la creazione di un **VHDL strutturale** l'utente deve caricare deve selezionare i componenti da istanziare all'interno dello strutturale e , in seguito, mappare le porte degli stessi.

### Fase 1: Caricare i componenti:
Attraverso una vista: **'BASEURL/component/creation'** l'utente può caricare un componente VHDL.
Questa vista richiede all'utente di inserire un nome per il componente e il caricamento del file **VHDL** che lo contiene.
Il file **VHDL** una volta caricato viene elaborato al fine di estrapolarne le informazioni necessarie.
(file: vhdl/component_parsing.py)
Qui vengono definite du classi **Component** e **Port** che rappresentano gli oggetti fondamentali dell'elaborazione: il componente caricato dall'utente e le porte dello stesso.

```python

class Component:
    def __init__(self):
        self.entity_name = ''
        self.input_port = ''
        self.output_port = ''
        self.architecture_name = ''
    
    def __str__(self):
        return f"Componente: { self.entity_name }, { self.input_port }, \
        { self.output_port }, { self.architecture_name }"

class Port:
    def __init__(self):
        self.name = ''
        self.verse = ''
        self.type = ''
    
    def __str__(self):
        return f"{self.name} {self.verse} {self.type}"

```

*per le proprietà delle classi sono stati scelti nomi ideomatici al fine di non doverne mai spiegarne il contenuto.*

La funzione "parsing" di popolare la classe Component e poi salvarla in DB

```python
def parsing(obj):
    with open(obj.file.path, 'r') as file:
        component = Component()
        lines = file.read().lower().splitlines()

        component.entity_name = get_entity(lines)
        component.input_port, component.output_port = get_ports(lines)
        component.input_port = component.input_port.strip()
        component.output_port = component.output_port.strip()
        component.architecture_name = get_architecture(lines, component.entity_name)

        # print(component.input_port)

        obj.entity_name = component.entity_name
        obj.input_ports = component.input_port
        obj.output_ports = component.output_port
        obj.architecture_name = component.architecture_name
        obj.save()
```

Questa funzione richiama sequenzialmente una serie di funzioni:
- get_entity
- get_ports
- get_architecture
Tutte queste funzioni elaborano il contenuto testuale del file caricato dall'utente

### GET_ENTITY
```python
def get_entity(lines):
    """
    Funzione che ritorna il nome dell'entity del componente VHDL
    """
    for line in lines:
        if ('entity' in line) and ('is' in line):
            new_line = line.strip().split(' ')
            return new_line[1]
```

### GET_PORTS
Questa è una funzione che ritorna due vettori separati, uno per le porte di input e uno per le porte di output.
Ogni elemento dei due vettori è così composto:

**"{nome porta} {verso_porta} {tipo_porta}"**
```python
def get_ports(lines):
    port = False

    ins = []
    outs = []

    for line in lines:
        if 'port' in line and '(' in line:
            port = True
        if ');' in line and port:
            break
        if ':' in line and ('in' in line or 'out' in line):
            new_line = line.strip().split(' ')
            port = Port()
            # print(new_line)
            port.name = new_line[0]
            port.verse = new_line[2]
            port.type = new_line[3]

            if ';' in port.type:
                port.type = port.type.replace(';', '')

            if port.verse == 'in':
                ins.append(port)
            elif port.verse == 'out':
                outs.append(port)
    str_ins = ''
    str_outs = ''
    for element in ins:
        string = ''
        string += element.name
        string += ' '
        string += element.verse
        string += ' '
        string += element.type
        string += ' '
        string += '|SEP|'
        str_ins += string
    for element in outs:
        string = ''
        string += element.name
        string += ' '
        string += element.verse
        string += ' '
        string += element.type
        string += ' '
        string += '|SEP|'
        str_outs += string
    
    # print(str_ins, str_outs)
    return str_ins, str_outs
```

### GET_ARCHITECTURE
```python
def get_architecture(lines, component_name):
    """
    Funzione che ritorna il nome dell'architettura del componente VHDL
    """
    for line in lines:
        if 'architecture' in line and component_name in line:
            new_line = line.strip().split(' ')
            return new_line[1]
```

Terminata questa fase l'utente ha generato un componente che potrà usare nei vari progetti di VHDL strutturale che creerà in quanto ogni componente è salvato in db.

### Fase 2: creazione Strutturale
L'utente andando alla vista: **'BASEURL/structural/selection'** viene rimandato alla fase di creazione di un VHDL strutturale.
Qui l'utente è chiamato a dare un nome al progetto e a selezionare i componenti da istanziare nel VHDL.

** Struttura del form**

```python 
class StructuralSelectionForm(forms.ModelForm):
    component_list = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    conferma = forms.ChoiceField(
        required=False,
        choices=[(False, 'No'), (True, 'Si')],
    )

    class Meta:
        model = Structural
        fields = (
            'name',
            'component_list',
        )
```
**component_list** = rappresenta il campo del form dove vengono selezionati i componenti vhdl. Da notare come le scelte che propone agli utenti vengano generate da un queryset su un DB locale.

Tutti i dati generati dall'interazione dell'utente con questa vista vengono passati alla vista successiva con il metodo **POST** dopo esser stati validati dalla vista stessa.

### Fase 3: mappatura dei componenti

L'utente andando alla vista: **'BASEURL/structural/< pk >'**, dove pk rappresenta l' ID dello strutturale (primary key), l'utente viene portato su una vista dove potrà eseguire le mappature di tutti i componenti istanziati.

Qui per ogni porta istanziata vi è un "menu a tendina" che permette di scegliere su quale porta mappare.
Ovviamente nelle scelte del "menu a tendina" sono presenti tutte le porte dei componenti istanziati.

In questo passaggio si identificano una serie di criticità:
- se vi è una mappatura fra la porta del componente A e la porta del componente B, va generato il segnale S1 di 'raccordo' fra le due.
- un componente deve poter essere mappato con una porta del componente che lo contiene.

La prima problematica viene risolta in fase di elaborazione dei dati del form, mentre la seconda viene risolta facendo la injection di una nuova porta sul queryset di **StructuralMappingForm** (file: vhdl/forms.py). Questa nuova porta avrà come nome PORTA_ENTITA e come tipo quello della porta con cui viene mappata.

