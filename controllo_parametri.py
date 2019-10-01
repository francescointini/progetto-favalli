#main
#interfaccia dei diversi componenti
#integrare ghdl
#ingresso 2 file vhd

#import
from pathlib import Path
import sys

#controllo parametri  3 parametri: 2 file e un numero
def controllo(file1,file2,intero):
    if (len(sys.argv)!= 5):
        print("Errore, numero parametri errati")
        exit("Errore 00")

    myfile=Path(file1)
    if not(myfile.is_file()):
        print("File1 nel primo parametro non esistente.")
        exit("Errore 01")
    
    myfile2=Path(file2)
    if not(myfile2.is_file()):
        print("File2 nel secondo parametro non esistente.")
        exit("Errore 02")

    if(intero == ""):
        print("Errore, terzo parametro mancante")
        exit("Errore 03")
    
    value = int(intero)
    if not(intero > 0):
        print("Errore valore non consentito.")
        exit("Errore 04")

#richiamo file .py e verifico che funzionino
vector_path="vector.py"
def file_vector():
    if not(vector_path.is_file()):
        print("Errore"+vector_path+" esistente")
        exit("Errore vettore")
    #else:
        #esecuzione vettore
        #./vector_path

#esecuzione init.py
init_path="init.py"
def fileinit():
    if not(init_path.is_file()):
        print("Errore, file "+init_path+" non trovato")
        exit("Errore init")
    #else: ./init_path


       
        
        



    