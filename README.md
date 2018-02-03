# Ungherese

Durante i tre giorni di cogestione al VV gli studenti presentano più di 100 conferenze.

Per garantire la distribuzione ideale di aule, lavagne interattive (LIM) e proiettori tra i relatori utilizziamo questo programma, che implementa l'algoritmo di assegnazione di Kuhn-Munkres (detto anche _algoritmo ungherese_) e aggiunge strumenti utili all'organizzazione dell'evento.

In questo modo abbiamo alleggerito notevolmente il carico sugli organizzatori, che ora possono affidarsi a un sistema automatico e avere la garanzia di implementare la migliore distribuzione delle risorse limitate.


## Uso

È necessario preparare due file: `aule.csv` e `collettivi.csv` che descrivono le risorse e le richieste. I risultati sono salvati in `./risultati`.

* aule `ID;Lotto;Piano;Aula;Classe;LIM;PROJ;Big`
* collettivi `ID;Name;T1;T2;T3;T4;T5;T6;LIM;PRO;BIG;Lotto`

Aule e collettivi sono identificati da un codice numerico univoco. LIM, PRO e BIG indicano se una data risorsa è disponibile (nel caso delle aule) o richiesta (per i collettivi).

Ciascun collettivo assegna 1 ai vari turni in cui verrà tenuto. I turni sono numerati a partire dal primo turno del primo giorno (T1) fino all'ultimo del terzo giorno (due turni al giorno).

Infine il codice si segue con `$ python runner.py`
