# Trattiamo la cogestione come un problema di assegnamento:
# le aule sono worker, i collettivi task. Il costo di un'assegnazione
# è lo scontento: la differenza pesata tra richieste del collettivo
# e risorse dell'aula.

# Algoritmo ungherese: restituisce le coordinate delle celle scelte in O(n^3)
# Written by CAT_BAXTER, 2012-05-03, 
# https://pastebin.com/tn6v0HDr
INF = 100000000000000000

def hungarian(matrix):
    h, w,  = len(matrix), len(matrix[0]) 
    u, v, ind = [0]*h, [0]*w, [-1]*w
    for i in range(h):
        links, mins, visited = [-1]*w, [INF]*w, [False]*w
        markedI, markedJ, j = i, -1, 0
        while True:
            j = -1
            for j1 in range(h):
                if not visited[j1]:
                    cur = matrix[markedI][j1] - u[markedI] - v[j1]
                    if cur < mins[j1]:
                        mins[j1] = cur
                        links[j1] = markedJ
                    if j == -1 or mins[j1] < mins[j]: j = j1
            delta = mins[j]
            for j1 in range(w):
                if visited[j1]:
                    u[ind[j1]] += delta;  v[j1] -= delta
                else:
                    mins[j1] -= delta
            u[i] += delta
            visited[j] = True
            markedJ, markedI = j, ind[j] 
            if markedI == -1:
                break
        while True:
            if links[j] != -1:
                ind[j] = ind[links[j]]
                j = links[j]
            else:
                break
        ind[j] = i
    return [(ind[j], j) for j in range(w)]

# OGGETTI
class Flag(object):
    def __init__(self, peso, valore):
        self.peso = peso
        self.valore = valore

    def __repr__(self):
        return str(self.valore)

class Assegnanda(object): # da usare come classe astratta
    def __init__(self, name, flags):  # flags :: [Flag]
        self.name = name
        self.flags = flags

    def __repr__(self):
        return self.name

    def prior(self):
        if not self.flags:
            return 0
        else:
            result = 0
            for flag in self.flags:
                result = result | flag.valore
            return result
            
class Aula(Assegnanda):
    def risorse(self):
        return self.prior()

class Coll(Assegnanda):
    def __init__(self, name, flags, turni):
        self.name = name
        self.flags = flags # flags :: [Flag]
        self.turni = turni # turni :: [[Bool]], lista di giorni, giorni = lista di turni 

    def richieste(self):
        return self.prior()

class Soluzione(object):
    def __init__(self, associativo):
        self.assegnazioni = associativo  # associativo :: [(Aula, Collettivo)]
        self.aule = list(zip(*associativo))[0]
        self.collettivi = list(zip(*associativo))[1]

    def __str__(self):
        result = []
        scontento_totale = 0
        numCollettivi = 0
        for (aula, collettivo) in self.assegnazioni:
            cellScontent = scontento(collettivo, aula)
            scontento_totale += cellScontent
            numCollettivi += 1
            result.append('%s, %s -> %d \n' % (aula.name, collettivo.name, cellScontent))
        result.append('Scontento totale: %d \n' % scontento_totale)
        if scontento_totale == 0:
            result.append('Soluzione perfetta \n')
        else:
            result.append('Scontento medio: %.2f \n' % (scontento_totale / numCollettivi,))
        return ''.join(result)

        def __repr__(self): 
            for aula, coll in self:
                yield (aula.name, coll.name)
    
    def extend(self, aggiunta):
        self.assegnazioni.extend(aggiunta)

# FUNZIONI
def scontento(coll, aula):
    """ Calcola il costo di una data assegnazione """
    assert isinstance(coll, Coll), (coll, type(coll))
    assert isinstance(aula, Aula), (aula, type(aula))
    result = 0
    soddisfazione = coll.richieste() & aula.risorse()
    for flag in coll.flags:
        if not soddisfazione & flag.valore:
            result += flag.peso
    return result

def tabella(aule, coll):
    """ Genera la matrice argomento dell'ungherese """
    assert isinstance(aule[0], Aula), (aule, type(aule[0]))
    assert isinstance(coll[0], Coll), (coll, type(coll[0]))
    rows = []
    for aula in aule:
        currentRow = []
        for collettivo in coll:
            currentRow.append(scontento(collettivo, aula))
        rows.append(currentRow)
    return rows

def soluzione(aule, collettivi):
    matrice = tabella(aule, collettivi)
    indexes = hungarian(matrice)
    result = []
    for row, column in indexes:
        result.append((aule[row], collettivi[column]))
    return Soluzione(result)
