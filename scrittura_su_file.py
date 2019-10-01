#prende due stringhe
#prova a scrivere su file
#numero,stringa

#import
from pathlib import Path
import sys


def scrittura(str1,str2):
    if(str1.is_empty()):
        print("Errore parametro 1 assente")
        exit("Errore 01")

    if(str2.is_empty()):
        print("Errore,parametro 2 assente")
        exit("Errore 02")

    if ("result.csv".is_file()):
        f1=open("result.csv","a")
        f1.write(str1+","+str2)
        f1.close()
    else:
        f1=open("result.csv","w+")
        f1.write(str1+","+str2)
        f1.close()

