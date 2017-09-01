import hu
import os
import csv
import sys

LIM = hu.Flag(4, 1 << 2)
TVX = hu.Flag(2, 1 << 1)
BIG = hu.Flag(1, 1 << 0)

FILE_COLLETTIVI = 'classes2.csv'
FILE_AULE = 'aule.csv'
SUBDIR_RISULTATI = 'risultati/'

I_C_INIZIO_TURNI = 2
I_C_FINE_TURNI = 7
I_C_INIZIO_FLAG = 8
I_C_FINE_FLAG = 10 

TURNI_PER_GIORNATA = 2
GIORNATE = 3

# Parsing del csv
def parsaAule(file_aule):
    """ Dato il csv genera lista di aule """
    aule = []
    with open(file_aule, 'r') as aulefile:
        parsedAule = csv.reader(aulefile, delimiter=';')
        for row in parsedAule:
            flags = []
            name = "A" + str(row[0])
            for (certainFlag, assignableFlag) in zip(row[5:],[LIM,TVX,BIG]):
                assert certainFlag == '1' or certainFlag == '0', "Invalid flag aula %s" % str(certainFlag)
                if certainFlag == '1':
                    flags.append(assignableFlag)
            aule.append(hu.Aula(name, flags))
    return aule
            
def parsaCollettivi(file_collettivi):
    """ Dato il csv genera lista di collettivi """
    collettivi = []
    with open(file_collettivi, 'r') as aulefile:
        parsedCollettivi = csv.reader(aulefile, delimiter=';') 
        for row in parsedCollettivi:
            flags = []
            turni = []
            name = "C" + str(row[0])
            for (certainFlag, assignableFlag) in zip(row[I_C_INIZIO_FLAG:I_C_FINE_FLAG + 1],[LIM,TVX,BIG]):
                assert certainFlag == '1' or certainFlag == '0', "Invalid flag coll %s" % str(certainFlag)
                if certainFlag == '1':
                    flags.append(assignableFlag)

            for turno in row[I_C_INIZIO_TURNI : I_C_FINE_TURNI + 1]:
                assert len(row[I_C_INIZIO_TURNI : I_C_FINE_TURNI + 1]) % TURNI_PER_GIORNATA == 0, 'Numero di turni errato'
                assert int(turno) >= -1
                if turno != '-1':
                    turni.append(True)
                else:
                    turni.append(False)
            
            turni = [turni[n:n + TURNI_PER_GIORNATA] for n in range(0, len(turni), TURNI_PER_GIORNATA)]  # raggruppa a due a due i turni in giornate 
            assert len(turni) == GIORNATE, 'Numero giornate errato'
            collettivi.append(hu.Coll(name, flags, turni))

    return collettivi

# Da usare se ci sono più aule che collettivi
def trimAule(aule, n):
    """ Ritorna le prime n aule, ordinate per risorse decrescenti """
    assert isinstance(aule[0], hu.Aula), (type(aule[0])) 
    return sorted(aule, key = (lambda x: x.risorse()), reverse=True)[:n]

def main():
    collettivi = parsaCollettivi(FILE_COLLETTIVI)
    aule = parsaAule(FILE_AULE)

    for giornata in range(GIORNATE): # una iterazione per giornata
        print('')
        print('------ GIORNATA %d ------' % giornata)

        pathGiornataCorrente = SUBDIR_RISULTATI + 'g%d' % giornata
        os.makedirs(pathGiornataCorrente, exist_ok=True)

        collettiviT0 = []
        collettiviT1 = []
        for collettivo in collettivi:
            if collettivo.turni[giornata][0]:
                collettiviT0.append(collettivo)
            elif collettivo.turni[giornata][1]:
                collettiviT1.append(collettivo)
            
        if len(aule) < len(collettiviT0):
            print('Aule non sufficienti nel turno 0, giornata %d' %  giornata, file=sys.stderr)
            sys.exit(1)

        if len(aule) < len(collettiviT1):
            print('Aule non sufficienti nel turno 1, giornata %d' %  giornata, file=sys.stderr)
            sys.exit(1)

        auleT0 = trimAule(aule, len(collettiviT0))  # Questa e` un'assunzione forte, ma non rischiosa con i nostri dati
        print('')
        print('*** TURNO 0 ***' )
        soluzioneT0 = hu.soluzione(auleT0, collettiviT0)
        print(soluzioneT0)

        auleAssegnateT0 = soluzioneT0.aule
        auleT1 = [a for a in aule if a not in auleAssegnateT0]
        auleT1 = trimAule(auleT1, len(collettiviT1))
        print('')
        print('*** TURNO 1 ***' )
        soluzioneT1 = hu.soluzione(auleT1, collettiviT1)
        soluzioneT1.extend(assegnazione for assegnazione in soluzioneT0.assegnazioni if assegnazione[1].turni[giornata][1]) # Per non spostare i collettivi da un turno all'altro
        print(soluzioneT1)
        
        soluzioni = [soluzioneT0, soluzioneT1]
        for i in range(2):
            with open(pathGiornataCorrente + ('/t%d.csv' % i), 'w') as output:
                for (aula, collettivo) in soluzioni[i].assegnazioni:
                    line = aula.name + ',' + collettivo.name + '\n'
                    output.write(line)

if __name__ == '__main__':
   main()
