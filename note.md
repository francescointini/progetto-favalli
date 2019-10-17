# Problema

E' evidente la necessità di definire un sistema per tracciare gli stati di errore di un componente elettronico digitale, capacita apparentemente non insita nel VHDL da noi studiato. Per questioni di semplicità e sviluppo per ora verrà definita solamente una notazione basilare per definire gli errori più semplici

------

## L'analisi di qui sotto può definirsi DEPRECATED

### Flag stato di errore

E' l'elemento della riga che definisce l'inizio delle istruzioni di errore per il parser, per contiguità con la notazione del VHDL uso:

```VHDL
ERROR OF ARCHITECTURE_NAME is
    (...
     ... descrizione stato di errore ..
     ...)
END ERROR
```
### Comandi per la definizione dello stato di errore

Lavorando principalmente con valori **bool** per l'appunto 1 e 0, conviene definire gli errori a partire dalle operazioni definite per i booleani ...

------

## Inizio nuove note