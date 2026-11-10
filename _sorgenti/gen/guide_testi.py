#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testi delle guide di calcolaprecetti.it: guida 1, 2, 3 e indice /guide/.

Rivedute dal titolare il 10.11.2026. Dopo ogni modifica: python3 _sorgenti/genera.py e python3 _sorgenti/controlla.py;
per gli esempi numerici, node _sorgenti/gen/calc.js.
Le parti comuni (intestazione, piè di pagina, modello della pagina) restano in build_guides.py.
"""
from build_guides import *  # noqa: F401,F403  parti comuni e funzioni per le pagine
from build_guides import G1, G2, G3  # noqa: F401  indirizzi delle tre guide

# =========================================================================== guida 1
G1_BODY = '\n'.join([
    '<section id="passi">',
    '<h2>I sei passi</h2>',
    '<p class="g-sub">Segui l\'ordine: ogni passo prepara il successivo. Spesso basta arrivare al quarto.</p>',
    '<ol class="g-steps">',
    step(1, 'Controlla le carte', '''
<p>Tre controlli, dieci minuti.</p>
<ul>
<li><strong>La fattura è scaduta?</strong> Se non avete concordato un termine, il pagamento scade 30 giorni dopo il ricevimento della fattura. Con la fattura elettronica vale la data di consegna registrata dal Sistema di interscambio (SDI). Tra imprese potete concordare fino a 60 giorni; un termine più lungo vale solo se è scritto nel contratto e non è gravemente iniquo per chi deve incassare.</li>
<li><strong>Hai le prove?</strong> Metti insieme ordine o contratto, documento di trasporto firmato o conferma del lavoro finito, fattura, tutte le email scambiate.</li>
<li><strong>Ci sono contestazioni?</strong> Se il cliente ha contestato la merce, il lavoro o le tempistiche, rispondi per iscritto prima di andare avanti.</li>
</ul>
''' + note('In parole semplici', 'La fattura dice che hai chiesto dei soldi. L\'ordine e la consegna dicono perché ti spettano: se il cliente contesta, sono loro a fare la differenza.'),
         when='Prima di scrivere al cliente', sid='passo-1'),
    step(2, 'Sollecita subito', '''
<p>Una email e una telefonata. Molti ritardi sono dimenticanze, o fatture finite sulla scrivania sbagliata.</p>
<p>Nell'email scrivi quattro cose: numero e data della fattura, importo, IBAN e il giorno entro cui aspetti il pagamento. Una data precisa funziona meglio di «al più presto» o «a stretto giro».</p>
<p>Segnati quella data. Se passa senza risposta, vai al passo 3.</p>
''', when='Dal giorno dopo la scadenza', sid='passo-2'),
    step(3, 'Calcola quanto ti spetta', '''
<p>Tra imprese, professionisti e pubblica amministrazione il ritardo ha un prezzo fissato dalla legge (D.Lgs. 231/2002), che puoi calcolare con lo <a href="/interessi-moratori/">strumento degli interessi moratori</a>. Al capitale si aggiungono:</p>
<ul>
<li><strong>Gli interessi di mora.</strong> Tasso della BCE più 8 punti: oggi <span class="js-mora-rate">10,40%</span> l'anno. Partono dal giorno dopo la scadenza, senza bisogno di lettere.</li>
<li><strong>€ 40 per ogni fattura</strong> pagata in ritardo, come rimborso fisso dei costi di recupero.</li>
<li><strong>I costi in più,</strong> se li dimostri: per esempio la parcella dell'avvocato per la diffida.</li>
</ul>
<div class="g-conto">
<p class="g-conto-t"><b>Esempio.</b> Fattura da € 8.000 scaduta il 31 marzo 2026, conto fatto al 6 ottobre 2026.</p>
<div class="g-rows">
''' + '\n'.join([
        row('Capitale', '€ 8.000,00'),
        row('Interessi dal 1° aprile al 30 giugno, 91 giorni al 10,15%', '€ 202,44'),
        row('Interessi dal 1° luglio al 6 ottobre, 98 giorni al 10,40%', '€ 223,39'),
        row('Risarcimento forfettario', '€ 40,00'),
        row('Totale', '€ 8.465,83', tot=True),
    ]) + '''
</div>
</div>
<p>Se il cliente è un privato queste regole non valgono: gli interessi sono quelli legali, oggi <span class="js-legal-rate">1,60%</span> l'anno (<a href="/tassi/">verifica il tasso aggiornato</a>), e i € 40 non spettano.</p>
<div class="panel g-tool" id="strumento" data-quick="mora">
<span class="g-note-l">Lo strumento</span>
<h4 class="g-tool-t">Quanto ti spetta oggi</h4>
<div class="pair">
<label class="field"><span class="label">Importo della fattura</span><span class="money"><span class="sign">€</span><input type="text" inputmode="decimal" id="qCap" value="8.000,00" placeholder="0,00"></span></label>
<label class="field"><span class="label">Scadenza del pagamento</span><input type="date" id="qScad" value="2026-03-31"></label>
</div>
<p class="hint">I dati dell'esempio sono già inseriti: sostituiscili con i tuoi. Restano sul tuo dispositivo.</p>
<div class="g-out" id="qOutMora" aria-live="polite"><p class="empty">Per vedere il calcolo attiva JavaScript nel browser.</p></div>
<div class="actions"><a class="btn btn-secondary" href="/interessi-moratori/">Vedi il calcolo semestre per semestre</a></div>
</div>
''', when='Prima della diffida', sid='passo-3'),
    step(4, 'Manda la diffida', '''
<p>La diffida è una lettera formale: chiedi il pagamento entro un termine preciso, di solito 7 o 10 giorni, e avvisi che dopo ti rivolgerai al giudice.</p>
<p>Dentro ci vanno le fatture non pagate, il totale calcolato al passo 3, il termine, l'IBAN e cosa farai se il termine scade. Mandala per PEC o con raccomandata con ricevuta di ritorno: imprese e professionisti iscritti a un albo devono avere una PEC, e la trovi gratis su inipec.gov.it inserendo codice fiscale o numero della partita IVA.</p>
<p>Serve a tre cose:</p>
<ul>
<li><strong>Ferma la prescrizione.</strong> Il tempo che hai per pretendere il pagamento riparte da zero.</li>
<li><strong>Resta agli atti.</strong> È la prova che hai chiesto il pagamento, e quando.</li>
<li><strong>Cambia il tono.</strong> Chi la riceve capisce che il passo dopo è il giudice.</li>
</ul>
<p>Puoi firmarla tu oppure <a href="/recupero-crediti/#affida" data-conta="recupero-da-guide">farla scrivere a un avvocato</a>, così da essere sicuro che ogni elemento sia riportato nella lettera e non ci siano dimenticanze.</p>
''', when='Dopo una settimana di silenzio', sid='passo-4'),
    step(5, 'Chiedi il decreto ingiuntivo', '''
<p>Non serve una causa di anni. Con le carte del passo 1 un avvocato chiede al giudice un decreto ingiuntivo: l'ordine di pagare entro 40 giorni, dato senza convocare il debitore. Questo è un procedimento molto più veloce della vera e propria causa a cui siamo abituati.</p>
<ul>
<li>Le fatture elettroniche passate dal Sistema di interscambio valgono come prova scritta.</li>
<li>Non devi tentare prima una mediazione o una negoziazione assistita. Con risparmio di soldi e tempo.</li>
<li>Se il debitore non paga e non si oppone, il decreto diventa definitivo e puoi procedere con la notifica del precetto e successivamente, se perdura l'inadempimento, con il pignoramento.</li>
</ul>
<p>Tempi e costi sono nella guida <a href="%s">Decreto ingiuntivo: tempi e costi</a>.</p>
''' % G2 + note('Ti propone di pagare a rate?', 'Accetta solo con una proposta formulata per iscritto. Un piano di rientro firmato, in cui il cliente riconosce il suo debito, ferma la prescrizione e sposta su di lui l\'onere di provare che il debito non c\'è. Se poi salta una rata, ti permette di chiedere un decreto subito esecutivo per l\'importo residuo.'),
         when='Se il termine della diffida scade', sid='passo-5'),
    step(6, 'Precetto e pignoramento', '''
<p>L'avvocato notifica il precetto: è l'ultimo avviso, con 10 giorni per pagare. Poi si pignora quello che il debitore ha: il conto corrente, i crediti verso i suoi clienti, i beni o gli immobili.</p>
<p>Per sapere cosa pignorare c'è la ricerca telematica dei beni: l'ufficiale giudiziario interroga le banche dati pubbliche e ti dice dove il debitore ha conti, rapporti di lavoro e veicoli. Questa richiesta la fa <a href="/recupero-crediti/#affida" data-conta="recupero-da-guide">un avvocato</a>.</p>
<p>Termini e mosse sono nella guida <a href="%s">Precetto notificato: cosa succede adesso</a>. Per il conto da scrivere nell'atto c'è il <a href="/">calcolo delle somme del precetto</a>.</p>
''' % G3, when='Con il decreto esecutivo in mano', sid='passo-6'),
    '</ol>',
    '</section>',
    '',
    '<section id="debitore">',
    '<h2>Prima di spendere, guarda chi hai davanti</h2>',
    '<p>Un decreto contro chi non ha nulla resta un foglio. Due controlli da fare presto.</p>',
    '<ul>',
    '<li><strong>Visura e bilanci.</strong> Dal Registro delle imprese vedi se la società è attiva, in liquidazione o in una procedura concorsuale, e scarichi gli ultimi bilanci.</li>',
    '<li><strong>Liquidazione giudiziale.</strong> È il vecchio fallimento. Se il cliente c\'è già dentro, le azioni dei singoli creditori si fermano: il credito si fa valere con la domanda di ammissione al passivo, da inviare al curatore.</li>',
    '</ul>',
    '<h3>Se alla fine non incassi</h3>',
    '<p>Qualcosa si recupera lo stesso. Il verbale di un pignoramento andato a vuoto ti permette di riprendere l\'IVA versata su quella fattura, con una nota di variazione, e di dedurre la perdita. Per i crediti fino a € 2.500 (€ 5.000 per le imprese più grandi) la perdita si deduce già dopo sei mesi dalla scadenza. Parlane con il tuo commercialista, ti saprà sicuramente dare le direttive corrette.</p>',
    '</section>',
    '',
    '<section id="errori">',
    '<h2>Gli errori che costano</h2>',
    '<ul class="g-err">',
    '<li><strong>Aspettare.</strong> Più passa il tempo, più il recupero si complica. E i diritti scadono: di regola dopo dieci anni, ma dopo cinque per interessi e canoni e dopo uno per trasporti e spedizioni.</li>',
    '<li><strong>Continuare a consegnare.</strong> Ogni nuova fornitura a chi non paga aumenta il credito da recuperare.</li>',
    '<li><strong>Accordarsi a voce.</strong> Rate e dilazioni vanno scritte e firmate. Meglio un\'email che una telefonata. Valgono come prova anche i messaggi su WhatsApp.</li>',
    '<li><strong>Dimenticare interessi e € 40.</strong> Spettano per legge. Se non li chiedi, li regali.</li>',
    '<li><strong>Diffidare tre volte.</strong> Dopo una diffida scaduta, la seconda pesa meno. Il passo giusto è il giudice, non ha senso posticipare l\'azione.</li>',
    '</ul>',
    '</section>',
])

GUIDA1 = {
    'path': G1,
    'crumb': 'Fattura non pagata',
    'title': 'Fattura non pagata: cosa fare, passo per passo',
    'desc': ('Il cliente non paga la fattura? I sei passi per farsi pagare: sollecito, interessi di mora e € 40, diffida, '
             'decreto ingiuntivo, pignoramento. Con un esempio.'),
    'og': 'I sei passi per farsi pagare, dal sollecito al pignoramento, e quanto ti spetta tra interessi di mora e € 40.',
    'h1': 'Fattura non pagata: cosa fare, <mark>passo per passo</mark>',
    'lead': 'Il cliente non paga. Qui trovi cosa fare, in che ordine e quanto ti spetta: sei passi, dal primo sollecito al pignoramento.',
    'per': 'Per imprese e professionisti',
    'brief': [
        '<mark>Gli interessi partono da soli.</mark> Tra imprese non serve nessuna lettera: dal giorno dopo la scadenza maturano interessi di mora, oggi al <span class="js-mora-rate">10,40%</span> l\'anno. <a href="/interessi-moratori/">Verifica il tasso aggiornato</a>.',
        '<mark>Ti spettano anche € 40 per fattura,</mark> come rimborso fisso dei costi di recupero.',
        '<mark>Se non paga, non serve una causa lunga.</mark> Con le fatture puoi chiedere un decreto ingiuntivo, cioè un ordine di pagamento del giudice.',
    ],
    'toc': [('passi', 'I sei passi'), ('strumento', 'Lo strumento: quanto ti spetta oggi'), ('debitore', 'Guarda chi hai davanti'),
            ('errori', 'Gli errori che costano'), ('parole', 'Parole difficili, tradotte'), ('domande', 'Domande frequenti'),
            ('mossa', 'La mossa da fare oggi')],
    'body': G1_BODY,
    'gloss': [
        ('Mora', 'Il ritardo nel pagamento. Da quel momento chi deve pagare deve anche gli interessi.'),
        ('Diffida', 'La richiesta scritta e formale di pagare entro un termine. Si chiama anche messa in mora.'),
        ('Prescrizione', 'Il tempo oltre il quale non puoi più pretendere il pagamento.'),
        ('Decreto ingiuntivo', 'L\'ordine di pagare dato dal giudice sulla base dei documenti, senza sentire prima il debitore.'),
        ('Titolo esecutivo', 'Il documento che dà diritto di pignorare: per esempio un decreto ingiuntivo diventato esecutivo.'),
        ('Precetto', 'L\'ultimo avviso al debitore: paga entro 10 giorni, altrimenti si procede.'),
        ('Pignoramento', 'Il blocco di somme o beni del debitore, per pagare il creditore con quelli.'),
    ],
    'faqs': [
        ('Dopo quanto tempo dalla scadenza posso agire?',
         'Dal giorno dopo. La legge non impone un periodo di attesa né un numero minimo di solleciti.'),
        ('La diffida è obbligatoria prima del decreto ingiuntivo?',
         'No. Conviene quasi sempre però: ferma la prescrizione e spesso basta per farsi pagare. Conviene anche al creditore.'),
        ('Chi paga l\'avvocato?',
         'Il compenso per il tuo avvocato è dovuto da te, mentre la condanna del giudice obbliga il debitore a rimborsartelo. Se il debitore non ha beni e non si recupera nulla, il costo finale rimane a tuo carico però: per questo conviene verificare prima la sua situazione patrimoniale e <a href="/valutazione-credito/" data-conta="valutazione-da-guide">ricevere una valutazione</a>.'),
        ('Il cliente contesta la fattura solo dopo il sollecito. Cosa cambia?',
         'Il decreto ingiuntivo si può chiedere lo stesso. Se però il cliente fa opposizione dovrai provare la consegna della merce o il lavoro svolto: per questo servono ordine, documento di trasporto ed email.'),
        ('Posso chiedere gli interessi di mora a un privato?',
         'Quelli del D.Lgs. 231/2002 no: valgono solo tra imprese, professionisti e pubblica amministrazione. A un privato puoi chiedere gli interessi legali, oppure quelli previsti dal contratto.'),
        ('Se non incasso, recupero almeno l\'IVA?',
         'Sì, a certe condizioni: quando il debitore entra in una procedura concorsuale, oppure dopo un pignoramento rimasto senza esito. Si fa con una nota di variazione. Per questi aspetti però contatta il tuo commercialista di fiducia, saprà darti i giusti consigli operativi.'),
    ],
    'mossa': '''<section class="g-move" id="mossa">
<h2>La mossa da fare <mark>oggi</mark></h2>
<p>Apri l'elenco delle fatture scadute. Per ognuna calcola interessi e € 40, poi manda il sollecito con una data precisa. Se è scaduta da più di un mese, passa alla diffida.</p>
<p>Oppure, <a href="/recupero-crediti/#affida" data-conta="recupero-da-guide">scrivimi</a>. Sono disponibile ad approfondire il tuo caso specifico.</p>
<div class="actions"><a class="btn btn-primary" href="/interessi-moratori/">Calcola gli interessi di mora</a><a class="btn btn-secondary" href="%s">Guida successiva: decreto ingiuntivo</a></div>
</section>''' % G2,
    'norme': ('D.Lgs. 9 ottobre 2002, n. 231, artt. 2, 4, 5 e 6. Codice civile, artt. 1988, 2943, 2944, 2945, 2946, 2948 e 2951. '
              'Codice di procedura civile, artt. 492-bis, 633, 634 e 642. D.L. 12 settembre 2014, n. 132, art. 3. '
              'D.Lgs. 12 gennaio 2019, n. 14, artt. 150 e 201. D.P.R. 26 ottobre 1972, n. 633, art. 26. '
              'D.P.R. 22 dicembre 1986, n. 917, art. 101, comma 5. Corte di giustizia UE, 20 ottobre 2022, causa C-585/20, sui € 40 per ogni fattura.'),
}

# =========================================================================== guida 2
G2_BODY = '\n'.join([
    '<section id="quando">',
    '<h2>Quando puoi chiederlo</h2>',
    '<p>Servono due cose.</p>',
    '<ul>',
    '<li><strong>Una somma precisa e già scaduta.</strong> Per esempio, fatture non pagate, canoni, parcelle.</li>',
    '<li><strong>Una prova scritta.</strong> Fatture elettroniche, contratto, ordine firmato, documento di trasporto, una lettera in cui il debitore riconosce il debito.</li>',
    '</ul>',
    '<p>Non devi tentare prima una mediazione o una negoziazione assistita: il ricorso si deposita subito. Se la prova scritta manca, la strada è la causa ordinaria.</p>',
    note('In parole semplici', 'Il giudice non decide dopo aver sentito tutti e due. Ti crede sulla base delle carte e lascia al debitore 40 giorni per dire la sua.'),
    '</section>',
    '',
    '<section id="tempi">',
    '<h2>I tempi, tappa per tappa</h2>',
    '<p class="g-sub">Per ogni tappa trovi il termine fissato dalla legge e quello che succede di solito.</p>',
    '<ol class="g-steps">',
    step(1, 'Deposito del ricorso', '<p>L\'avvocato scrive la richiesta al giudice, allega i documenti e la deposita per via telematica. Da qui parte il conto dei giorni.</p>'),
    step(2, 'Il giudice emette il decreto', law(
        ('Per legge', 'Entro 30 giorni dal deposito.'),
        ('In pratica', 'Pochi giorni negli uffici più rapidi, alcune settimane in quelli più carichi.'))),
    step(3, 'Notifica al debitore', law(
        ('Per legge', 'Entro 60 giorni dall\'emissione. Oltre, il decreto perde efficacia e si ricomincia.'),
        ('In pratica', 'In giornata per PEC. Da pochi giorni a qualche settimana con l\'ufficiale giudiziario.'))),
    step(4, 'I 40 giorni del debitore', law(
        ('Per legge', '40 giorni dalla notifica per pagare o fare opposizione. Sono 50 se il debitore sta in un altro Paese dell\'Unione europea.'),
        ('In pratica', 'Dal 1° al 31 agosto il termine si ferma: è la sospensione feriale.'))),
    step(5, 'Il decreto diventa esecutivo', law(
        ('Per legge', 'Se non c\'è opposizione del debitore, il giudice lo dichiara esecutivo su richiesta dell\'avvocato.'),
        ('In pratica', 'Da pochi giorni a qualche settimana.'))
         + '\n<p>Da questo momento hai il titolo esecutivo: il documento che dà diritto di pignorare.</p>'),
    step(6, 'Precetto e pignoramento', law(
        ('Per legge', 'Almeno 10 giorni dalla notifica del precetto, poi può iniziare il pignoramento.'))
         + '\n<p>Come funziona: <a href="%s">Precetto notificato: cosa succede adesso</a>.</p>' % G3),
    '</ol>',
    note('In totale', 'Se il debitore non si oppone, tra il deposito e il titolo esecutivo passano in genere da tre a sei mesi. Dipende soprattutto dall\'ufficio.'),
    '<h3>La scorciatoia: il decreto subito esecutivo</h3>',
    '<p>In alcuni casi il giudice autorizza l\'esecuzione subito, senza aspettare i 40 giorni:</p>',
    '<ul>',
    '<li>hai una cambiale, un assegno o un atto del notaio;</li>',
    '<li>hai un documento firmato dal debitore che riconosce il debito, per esempio un piano di rientro;</li>',
    '<li>dimostri che il ritardo ti causerebbe un danno grave.</li>',
    '</ul>',
    '<p>Con il decreto subito esecutivo notifichi insieme decreto e precetto, e puoi iscrivere ipoteca sugli immobili del debitore.</p>',
    '<h3>Se il debitore si oppone</h3>',
    '<p>Si apre una causa vera davanti allo stesso ufficio, e i tempi diventano quelli di una causa: anni, non mesi.</p>',
    '<p>Non tutto si ferma. Se l\'opposizione non poggia su prove scritte, già alla prima udienza il giudice può rendere esecutivo il decreto: da quel momento puoi pignorare comunque mentre la causa continua.</p>',
    '<p>In alcune materie, come somministrazione, subfornitura e contratto d\'opera, a quel punto diventa obbligatoria la mediazione. Avviarla tocca a te: se non lo fai, il decreto viene revocato.</p>',
    '</section>',
    '',
    '<section id="costi">',
    '<h2>I costi: cosa anticipi</h2>',
    '<p>Tre voci.</p>',
    '<ul>',
    '<li><strong>Contributo unificato.</strong> È la tassa per avviare il procedimento. Per il decreto ingiuntivo si paga la metà di quello di una causa. Tutti i casi sono nella <a href="https://www.altalex.com/guide/contributo-unificato" target="_blank" rel="noopener noreferrer">guida di Altalex sul contributo unificato</a>.</li>',
    '<li><strong>Anticipazione forfettaria: € 27.</strong> Non è dovuta davanti al giudice di pace per i crediti fino a € 1.033.</li>',
    '<li><strong>Compenso dell\'avvocato.</strong> Lo concordi con lui per iscritto prima di iniziare.</li>',
    '</ul>',
    '<div class="scroll"><table class="det costi" id="costiTable">',
    '<thead><tr><th>Valore del credito</th><th class="r">Contributo unificato</th><th class="r">Compenso medio</th></tr></thead>',
    '<tbody>',
    '<tr data-max="1100" data-cu="21.5" data-comp="473"><td>fino a € 1.100</td><td class="r">€ 21,50</td><td class="r">€ 473</td></tr>',
    '<tr data-max="5200" data-cu="49" data-comp="473"><td>fino a € 5.200</td><td class="r">€ 49,00</td><td class="r">€ 473</td></tr>',
    '<tr data-max="26000" data-cu="118.5" data-comp="567"><td>fino a € 26.000</td><td class="r">€ 118,50</td><td class="r">€ 567</td></tr>',
    '<tr data-max="52000" data-cu="259" data-comp="1370"><td>fino a € 52.000</td><td class="r">€ 259,00</td><td class="r">€ 1.370</td></tr>',
    '<tr data-max="260000" data-cu="379.5" data-comp="2242"><td>fino a € 260.000</td><td class="r">€ 379,50</td><td class="r">€ 2.242</td></tr>',
    '<tr data-max="520000" data-cu="607" data-comp="4394"><td>fino a € 520.000</td><td class="r">€ 607,00</td><td class="r">€ 4.394</td></tr>',
    '<tr data-cu="843"><td>oltre € 520.000</td><td class="r">€ 843,00</td><td class="r">da calcolare</td></tr>',
    '</tbody>',
    '</table></div>',
    '<p class="g-cap">Ogni riga vale fino all\'importo indicato. Il valore è il capitale più gli interessi già maturati. Il compenso medio è quello dei parametri ministeriali per i decreti ingiuntivi, negli importi in vigore dal 2022: il giudice lo usa per fissare la somma a carico del debitore, e può ridurlo o aumentarlo fino alla metà. Si aggiungono il rimborso forfettario del 15%, la cassa avvocati del 4% e l\'IVA.</p>',
    '<h3>Chi decide</h3>',
    '<p>Fino a € 10.000 il giudice di pace, oltre il tribunale. La soglia dovrebbe salire a € 30.000 dal 31 ottobre 2027: l\'aumento è già stato rinviato più volte. Di regola ci si rivolge al giudice del luogo in cui il debitore ha la sede o la residenza; se il debitore è un consumatore, sempre a quello della sua residenza.</p>',
    '<div class="panel g-tool" id="strumento" data-quick="costi" data-gdp="10000" data-forf="27" data-esente="1033">',
    '<span class="g-note-l">Lo strumento</span>',
    '<h3 class="g-tool-t">Quanto costa per il tuo credito</h3>',
    '<label class="field"><span class="label">Importo del credito</span><span class="g-solo"><span class="money"><span class="sign">€</span><input type="text" inputmode="decimal" id="qValore" value="8.000,00" placeholder="0,00"></span></span><span class="hint">Capitale più interessi già maturati. L\'importo dell\'esempio è già inserito: sostituiscilo con il tuo.</span></label>',
    '<div class="g-out" id="qOutCosti" aria-live="polite"><p class="empty">Per vedere il calcolo attiva JavaScript nel browser.</p></div>',
    '<p class="hint">Vale per i crediti da fatture. Alcune materie, come gli affitti, vanno sempre al tribunale.</p>',
    '</div>',
    '</section>',
    '',
    '<section id="recuperi">',
    '<h2>I costi: cosa recuperi</h2>',
    '<p>Nel decreto il giudice ordina al debitore di pagare anche le spese: i costi vivi che hai anticipato e un compenso per l\'avvocato, calcolato sui parametri.</p>',
    '<div class="g-conto">',
    '<p class="g-conto-t"><b>Esempio.</b> Credito di € 8.000 per fatture non pagate tra imprese: cosa deve pagare il debitore.</p>',
    '<div class="g-rows">',
    row('Capitale', '€ 8.000,00'),
    row('Risarcimento forfettario', '€ 40,00'),
    row('Contributo unificato e anticipazione', '€ 145,50'),
    row('Compenso dell\'avvocato, valore medio', '€ 567,00'),
    row('Rimborso forfettario 15%', '€ 85,05'),
    row('Cassa avvocati 4%', '€ 26,08'),
    row('Totale, più gli interessi', '€ 8.863,63', tot=True),
    '</div>',
    '<p class="g-conto-n">Al totale si aggiungono gli interessi di mora, che corrono fino al giorno del pagamento. L\'IVA sul compenso non è nel conto: l\'impresa la detrae, quindi non la chiede al debitore.</p>',
    '</div>',
    '<p>Due cose da sapere.</p>',
    '<ul>',
    '<li><strong>La differenza resta a te.</strong> Se il compenso concordato con l\'avvocato è più alto di quello fissato dal giudice, la differenza non la recuperi dal debitore.</li>',
    '<li><strong>L\'imposta di registro arriva dopo.</strong> La chiede l\'Agenzia delle Entrate quando il decreto è esecutivo. Per i crediti da fatture con IVA è fissa, € 200; sugli interessi di mora e negli altri casi è il 3%. Dal 2025 l\'Agenzia la chiede prima al debitore, e a te solo se da lui non incassa.</li>',
    '</ul>',
    '</section>',
    '',
    '<section id="errori">',
    '<h2>Gli errori che costano</h2>',
    '<ul class="g-err">',
    '<li><strong>Notificare tardi.</strong> Oltre i 60 giorni il decreto perde efficacia e si ricomincia da capo.</li>',
    '<li><strong>Partire con poche carte.</strong> Per il decreto può bastare la fattura. Se arriva l\'opposizione servono ordine, consegna e corrispondenza. Meglio partire «attrezzati» sin da subito.</li>',
    '<li><strong>Non guardare chi hai davanti.</strong> Prima di anticipare le spese, controlla visura e bilanci del debitore, oppure <a href="/valutazione-credito/" data-conta="valutazione-da-guide">chiedi al tuo avvocato</a>.</li>',
    '<li><strong>Sbagliare giudice.</strong> Valore e luogo decidono a chi rivolgersi: un errore regala al debitore un motivo di opposizione.</li>',
    '</ul>',
    '</section>',
])

GUIDA2 = {
    'path': G2,
    'crumb': 'Decreto ingiuntivo: tempi e costi',
    'title': 'Decreto ingiuntivo: tempi e costi, spiegati semplice',
    'desc': ('Quanto ci vuole e quanto costa un decreto ingiuntivo: i termini tappa per tappa, il contributo unificato, '
             'il compenso dell\'avvocato e chi paga alla fine.'),
    'og': 'Quanto ci vuole, quanto anticipi e chi paga alla fine: il decreto ingiuntivo con i numeri, tappa per tappa.',
    'h1': 'Decreto ingiuntivo: <mark>tempi e costi</mark>',
    'lead': 'Quanto ci vuole, quanto anticipi e chi paga alla fine. Con i numeri, tappa per tappa.',
    'per': 'Per imprese e professionisti',
    'brief': [
        '<mark>È un ordine di pagamento, non una causa.</mark> Il giudice decide sui documenti, senza convocare il debitore.',
        '<mark>Da tre a sei mesi, di solito,</mark> per avere in mano il titolo con cui pignorare, se il debitore non si oppone.',
        '<mark>Le spese le paga il debitore.</mark> Tu le anticipi: per un credito di € 8.000 sono € 145,50 di costi vivi, più il compenso dell\'avvocato.',
    ],
    'toc': [('quando', 'Quando puoi chiederlo'), ('tempi', 'I tempi, tappa per tappa'), ('costi', 'I costi: cosa anticipi'),
            ('strumento', 'Lo strumento: quanto costa'), ('recuperi', 'I costi: cosa recuperi'), ('errori', 'Gli errori che costano'),
            ('parole', 'Parole difficili, tradotte'), ('domande', 'Domande frequenti'), ('mossa', 'La mossa da fare oggi')],
    'body': G2_BODY,
    'gloss': [
        ('Ricorso', 'La richiesta scritta al giudice, preparata dall\'avvocato.'),
        ('Opposizione', 'La causa con cui il debitore contesta il decreto, entro 40 giorni dalla notifica.'),
        ('Esecutivo', 'Che può essere usato per pignorare. Un decreto lo diventa quando lo dichiara il giudice.'),
        ('Contributo unificato', 'La tassa che si paga allo Stato per avviare un procedimento.'),
        ('Parametri', 'Le tabelle del Ministero della giustizia con cui il giudice calcola il compenso dell\'avvocato.'),
        ('Ipoteca giudiziale', 'La garanzia iscritta sugli immobili del debitore in forza di un provvedimento del giudice.'),
    ],
    'faqs': [
        ('Serve per forza un avvocato?',
         'Sì. Fa eccezione il giudice di pace per i crediti fino a € 1.100, dove puoi presentare il ricorso da solo.'),
        ('Il debitore viene avvisato prima?',
         'No. Il giudice decide senza convocarlo: il debitore lo scopre quando riceve la notifica del decreto.'),
        ('Quanto dura un decreto ingiuntivo?',
         'Va notificato entro 60 giorni dall\'emissione. Una volta definitivo vale come una sentenza: il credito si prescrive in dieci anni.'),
        ('E se il debitore paga solo una parte?',
         'Il resto rimane dovuto. I pagamenti parziali coprono prima spese e interessi, poi il capitale.'),
        ('Posso chiederlo contro un debitore all\'estero?',
         'Sì. Se il debitore è in un altro Paese dell\'Unione europea esiste anche il decreto ingiuntivo europeo, pensato per i crediti oltre confine.'),
        ('Ho letto che l\'avvocato può intimare il pagamento senza passare dal giudice. È vero?',
         'Non ancora. È una proposta all\'esame del Parlamento e riguarda i crediti di importo minore. Finché non diventa legge, la strada è il decreto ingiuntivo. Ma se esce qualche novità farò un apposito articolo qui nel blog e ne sarai informato.'),
    ],
    'mossa': '''<section class="g-move" id="mossa">
<h2>La mossa da fare <mark>oggi</mark></h2>
<p>Crea una cartella per ogni cliente che non paga e mettici contratto o ordine, documenti di consegna, fatture, solleciti e diffida. È tutto quello che serve all'avvocato per depositare il ricorso. Poi <a href="/recupero-crediti/#affida" data-conta="recupero-da-guide">contattami</a> che delineiamo la strategia più adatta al tuo caso.</p>
<div class="actions"><a class="btn btn-primary" href="/recupero-crediti/#affida" data-conta="recupero-da-guide">Contattami</a><a class="btn btn-secondary" href="/interessi-moratori/">Calcola gli interessi di mora</a><a class="btn btn-secondary" href="%s">Guida successiva: precetto notificato</a></div>
</section>''' % G3,
    'norme': ('Codice di procedura civile, artt. 7, 10, 82, 633, 634, 641, 642, 644, 645, 647, 648 e 655. '
              'D.P.R. 30 maggio 2002, n. 115, artt. 13 e 30. Legge 21 novembre 1991, n. 374, art. 46. '
              'D.M. 10 marzo 2014, n. 55, tabella 8, come modificato dal D.M. 13 agosto 2022, n. 147. '
              'D.Lgs. 13 luglio 2017, n. 116, art. 32, comma 3, come modificato dal D.L. 12 giugno 2026, n. 100, convertito dalla legge 7 agosto 2026, n. 145. '
              'D.Lgs. 4 marzo 2010, n. 28, artt. 5 e 5-bis. D.L. 12 settembre 2014, n. 132, art. 3. Legge 7 ottobre 1969, n. 742. '
              'D.P.R. 26 aprile 1986, n. 131, art. 57, comma 1.1, e Tariffa, parte prima, art. 8. Codice civile, artt. 1194 e 2953. '
              'Regolamento (CE) n. 1896/2006. Disegno di legge n. 978 del Senato, XIX legislatura.'),
}

# =========================================================================== guida 3
G3_BODY = '\n'.join([
    '<section id="cose">',
    '<h2>Cos\'è, in parole semplici</h2>',
    '<p>Il precetto è l\'atto con cui il creditore dice al debitore: paga quanto stabilito dal titolo entro 10 giorni, altrimenti procedo con l\'esecuzione forzata.</p>',
    '<p>Non lo scrive il giudice: lo scrive l\'avvocato del creditore. Ma alle spalle deve esserci un titolo esecutivo, cioè un documento che dà diritto di pignorare: una sentenza, un decreto ingiuntivo esecutivo, una cambiale, un assegno, un atto del notaio.</p>',
    '</section>',
    '',
    '<section id="termini">',
    '<h2>I due termini: 10 e 90 giorni</h2>',
    '<figure class="g-bar">',
    '<div class="g-track" role="img" aria-label="Linea del tempo in scala: dieci giorni per pagare, poi fino al novantesimo giorno per iniziare il pignoramento"><span class="a"></span><span class="b"></span></div>',
    '<div class="g-ticks" aria-hidden="true"><span class="t0">0</span><span class="t10">10</span><span class="t90">90 giorni</span></div>',
    '<figcaption>',
    '<ul class="g-key">',
    '<li><i class="k0"></i><span><strong>Giorno 0: la notifica.</strong> I giorni si contano da quello successivo.</span></li>',
    '<li><i class="ka"></i><span><strong>Fino al giorno 10: il tempo per pagare.</strong> Prima di questa data il creditore non può pignorare.</span></li>',
    '<li><i class="kb"></i><span><strong>Dal giorno 11 al giorno 90: il tempo per pignorare.</strong> Il creditore può iniziare quando vuole.</span></li>',
    '<li><i class="k9"></i><span><strong>Giorno 90: il precetto scade,</strong> se il pignoramento non è iniziato.</span></li>',
    '</ul>',
    '</figcaption>',
    '</figure>',
    '<p>Tre cose spostano le date.</p>',
    '<ul>',
    '<li><strong>La ricerca dei beni.</strong> Se il creditore chiede la ricerca telematica dei beni, i 90 giorni si fermano finché non arriva l\'esito.</li>',
    '<li><strong>L\'opposizione.</strong> Se il debitore si oppone al precetto, i 90 giorni restano sospesi.</li>',
    '<li><strong>Agosto non ferma niente.</strong> Né i 10 né i 90 giorni si sospendono per la pausa estiva dei tribunali.</li>',
    '</ul>',
    '<div class="panel g-tool" id="strumento" data-quick="termini">',
    '<span class="g-note-l">Lo strumento</span>',
    '<h3 class="g-tool-t">Le tue date</h3>',
    '<label class="field"><span class="label">Precetto notificato il</span><span class="g-solo"><input type="date" id="qNotifica"></span><span class="hint">Per la PEC conta la ricevuta di consegna. Se lasci la data di oggi vedi un esempio.</span></label>',
    '<div class="g-out" id="qOutTermini" aria-live="polite"><p class="empty">Per vedere le date attiva JavaScript nel browser.</p></div>',
    '<p class="hint">Se una scadenza cade di sabato o in un giorno festivo, il calcolo la sposta al primo giorno lavorativo. Se devi pagare, non aspettare l\'ultimo giorno.</p>',
    '<div class="actions"><a class="btn btn-secondary" href="/termini-precetto/">Calcolo completo, con la ricerca dei beni</a></div>',
    '</div>',
    '</section>',
    '',
    '<section id="ricevuto">',
    '<h2>Se l\'hai ricevuto</h2>',
    '<p class="g-sub">Cinque mosse, in quest\'ordine. Quella da non fare è ignorarlo: il silenzio non ferma nulla.</p>',
    '<ol class="g-steps">',
    step(1, 'Controlla il conto', '<p>Il precetto elenca capitale, interessi, spese e compenso dell\'avvocato. Verifica che corrispondano al titolo e che siano stati tolti gli acconti già versati. Puoi rifare il conto con il <a href="/">calcolo delle somme del precetto</a>.</p>'),
    step(2, 'Se il debito è giusto, paga entro i 10 giorni', '<p>Fai un bonifico alle coordinate indicate nell\'atto, oppure chiedile all\'avvocato del creditore. Scrivi nella causale gli estremi del precetto e chiedi una quietanza. Dopo costa di più: al conto si aggiungono le spese del pignoramento.</p>'),
    step(3, 'Se non riesci a pagare tutto, chiama subito', '<p>Il creditore non è obbligato ad accettare rate, ma una proposta seria fatta prima del pignoramento conviene spesso a entrambi. Fai mettere l\'accordo per iscritto e continua a contare i giorni: una trattativa non ferma i termini.</p>'),
    step(4, 'Se il precetto è sbagliato, opponiti', '''<p><a href="/chi-sono/#hContatti" data-conta="contatto-da-guide">Serve un avvocato</a>, e ci sono due strade.</p>
<ul>
<li><strong>Contesti il diritto del creditore,</strong> perché hai già pagato o il credito è prescritto: è l'opposizione all'esecuzione.</li>
<li><strong>Contesti la forma dell'atto o della notifica:</strong> è l'opposizione agli atti esecutivi, da proporre entro 20 giorni dalla notifica.</li>
</ul>
''' + note('Attenzione', 'Se il titolo è una sentenza o un decreto ingiuntivo non opposto, di regola non puoi più discutere se il debito era dovuto: andava fatto allora, nella causa o con l\'opposizione al decreto. E per queste opposizioni i termini di regola non si fermano ad agosto.', 'att')),
    step(5, 'Se i debiti sono troppi', '<p>Il precetto stesso ti avvisa che puoi rivolgerti a un organismo di composizione della crisi per una procedura di sovraindebitamento: serve a sistemare tutti i debiti insieme, non solo questo. Questo passaggio lo puoi fare anche da solo, oppure seguito dal tuo avvocato.</p>'),
    '</ol>',
    '<h3>Cosa può essere pignorato</h3>',
    '<ul>',
    '<li><strong>Il conto corrente:</strong> la banca blocca le somme.</li>',
    '<li><strong>Lo stipendio:</strong> di regola un quinto.</li>',
    '<li><strong>La pensione:</strong> resta sempre libera una quota pari al doppio dell\'assegno sociale, con un minimo di € 1.000. Del resto si può pignorare un quinto.</li>',
    '<li><strong>Beni e immobili:</strong> anche la prima casa, se il creditore è un privato. Il divieto riguarda solo l\'agente della riscossione, e a certe condizioni.</li>',
    '</ul>',
    '</section>',
    '',
    '<section id="notificato">',
    '<h2>Se l\'hai notificato</h2>',
    '<p class="g-sub">Da qui al pignoramento, sei mosse.</p>',
    '<ol class="g-steps">',
    step(1, 'Segna due date: giorno 11 e giorno 90', '<p>Se lasci passare i 90 giorni devi rifare il precetto, e le spese del primo di regola restano a te.</p>'),
    step(2, 'Aspetta i 10 giorni', '<p>Prima non puoi pignorare. Solo se c\'è pericolo nel ritardo il presidente del tribunale può autorizzare l\'esecuzione immediata.</p>'),
    step(3, 'Scopri cosa pignorare', '<p>Passati i 10 giorni chiedi all\'ufficiale giudiziario la ricerca telematica dei beni: interroga le banche dati pubbliche su conti, rapporti di lavoro e veicoli. Mentre la ricerca è in corso i 90 giorni restano sospesi.</p>'),
    step(4, 'Scegli il pignoramento', '<p>Conto corrente e crediti verso terzi sono di solito la via più rapida. Gli immobili sono la più lunga e costosa.</p>'),
    step(5, 'Se arriva un acconto, rifai il conto', '<p>I pagamenti parziali coprono prima spese e interessi, poi il capitale. Il <a href="/">calcolo delle somme del precetto</a> lo fa da solo.</p>'),
    step(6, 'Se arriva una proposta di rate, valutala', '<p>Ma non lasciare scadere i 90 giorni senza un accordo scritto.</p>'),
    '</ol>',
    '</section>',
])

GUIDA3 = {
    'path': G3,
    'crumb': 'Precetto notificato',
    'title': 'Precetto notificato: cosa succede adesso e cosa fare',
    'desc': ('Hai ricevuto un precetto, o lo hai notificato? I termini di 10 e 90 giorni, cosa può fare il debitore, '
             'cosa deve fare il creditore e quando parte il pignoramento.'),
    'og': 'I 10 e i 90 giorni del precetto, cosa può fare chi lo riceve e cosa deve fare chi lo ha notificato.',
    'h1': 'Precetto notificato: <mark>cosa succede adesso</mark>',
    'lead': 'Che tu l\'abbia ricevuto o fatto notificare, da oggi contano due numeri: 10 e 90.',
    'per': 'Per chi l\'ha ricevuto e per chi l\'ha notificato',
    'brief': [
        '<mark>Il precetto è l\'ultimo avviso.</mark> Chi lo riceve ha almeno 10 giorni per pagare.',
        '<mark>Dal giorno 11 può partire il pignoramento,</mark> senza altri avvisi: conto corrente, stipendio, beni, immobili.',
        '<mark>Dopo 90 giorni il precetto scade.</mark> Se il creditore non ha iniziato il pignoramento, deve notificarne uno nuovo.',
    ],
    'toc': [('cose', 'Cos\'è, in parole semplici'), ('termini', 'I due termini: 10 e 90 giorni'), ('strumento', 'Lo strumento: le tue date'),
            ('ricevuto', 'Se l\'hai ricevuto'), ('notificato', 'Se l\'hai notificato'), ('parole', 'Parole difficili, tradotte'),
            ('domande', 'Domande frequenti'), ('mossa', 'La mossa da fare oggi')],
    'body': G3_BODY,
    'gloss': [
        ('Titolo esecutivo', 'Il documento che dà diritto di pignorare: sentenza, decreto ingiuntivo esecutivo, cambiale, assegno, atto del notaio.'),
        ('Notifica', 'La consegna ufficiale di un atto, per PEC o tramite ufficiale giudiziario. Da quel giorno partono i termini.'),
        ('Esecuzione forzata', 'L\'insieme delle procedure con cui il creditore si fa pagare anche contro la volontà del debitore.'),
        ('Pignoramento presso terzi', 'Il blocco di somme che altri devono al debitore: la banca per il conto, il datore di lavoro per lo stipendio.'),
        ('Quietanza', 'La dichiarazione scritta del creditore di aver ricevuto il pagamento.'),
        ('Sovraindebitamento', 'La situazione di chi non riesce più a pagare i propri debiti. La legge prevede procedure per uscirne.'),
    ],
    'faqs': [
        ('Il precetto arriva dal tribunale?',
         'No. Lo scrive l\'avvocato del creditore e te lo fa notificare. Il giudice interviene dopo, se parte il pignoramento o se fai opposizione.'),
        ('Dopo il precetto ricevo un altro avviso prima del pignoramento?',
         'No. Passati i 10 giorni il creditore può procedere direttamente.'),
        ('Quanto dura un precetto?',
         '90 giorni dalla notifica. Se in quel tempo il pignoramento non inizia il precetto perde efficacia, ma il creditore può notificarne uno nuovo finché il credito non è prescritto.'),
        ('Posso pagare a rate?',
         'Prima del pignoramento solo se il creditore è d\'accordo. Dopo il pignoramento puoi chiedere al giudice la conversione: versi subito almeno un sesto del dovuto e il resto in rate mensili, fino a 48.'),
        ('Avevo già pagato. Cosa faccio?',
         'Manda subito la prova del pagamento all\'avvocato del creditore, per iscritto. Se il precetto non viene ritirato serve l\'opposizione all\'esecuzione.'),
        ('Il precetto può arrivare per PEC?',
         'Sì, se hai un indirizzo PEC negli elenchi pubblici, come imprese e professionisti. Vale la data della ricevuta di consegna.'),
    ],
    'mossa': '''<section class="g-move" id="mossa">
<h2>La mossa da fare <mark>oggi</mark></h2>
<p>Segna le date sul calendario, adesso.</p>
<ul>
<li>Se l'hai ricevuto: il decimo giorno. Entro quella data paghi, tratti o ti opponi.</li>
<li>Se l'hai notificato: il giorno 11 e il giorno 90.</li>
</ul>
<div class="actions"><a class="btn btn-primary" href="/termini-precetto/">Calcola i termini del precetto</a><a class="btn btn-secondary" href="/">Calcola le somme del precetto</a></div>
</section>''',
    'norme': ('Codice di procedura civile, artt. 474, 479, 480, 481, 482, 492-bis, 495, 545, 615 e 617. Codice civile, art. 1194. '
              'D.P.R. 29 settembre 1973, n. 602, art. 76. D.Lgs. 12 gennaio 2019, n. 14 (Codice della crisi d\'impresa e dell\'insolvenza). '
              'Legge 7 ottobre 1969, n. 742, art. 3.'),
}


# =========================================================================== indice
CARDS = {  # titolo e riassunto di ogni guida negli indici (anche nella bozza del sito professionale)
    G1: ('Fattura non pagata: cosa fare, passo per passo',
         'I sei passi dal sollecito al pignoramento, e quanto ti spetta tra interessi di mora e € 40.'),
    G2: ('Decreto ingiuntivo: tempi e costi',
         'Quanto ci vuole, quanto anticipi e chi paga alla fine. Con i numeri, tappa per tappa.'),
    G3: ('Precetto notificato: cosa succede adesso',
         'I 10 e i 90 giorni, cosa può fare chi lo riceve e cosa deve fare chi lo ha notificato.'),
}
for _g in (GUIDA1, GUIDA2, GUIDA3):
    _g['index_title'] = CARDS[_g['path']][0]


def cards(info, href=lambda path: path):
    """Le schede delle guide negli indici e la lista per i dati strutturati."""
    out, items = [], []
    for n, (g, mins, blurb) in enumerate(info, 1):
        out.append('\n'.join([
            '<li><a class="g-card" href="%s">' % href(g['path']),
            '<span class="g-num" aria-hidden="true">%d</span>' % n,
            '<h3>%s</h3>' % g['index_title'],
            '<p>%s</p>' % blurb,
            '<span class="g-for">%s · %d minuti</span>' % (g['per'], mins),
            '<span class="g-go">Leggi la guida</span>',
            '</a></li>']))
        items.append({"@type": "ListItem", "position": n, "name": g['index_title'], "url": BASE + g['path']})
    return '\n'.join(out), items


ATTO = [  # scaffale per l'avvocato: le pagine tecniche, con il calcolo accanto
    ('/termini-precetto/', 'Calcolo e regole', 'Termini del precetto',
     'I 10 e i 90 giorni, la proroga dei festivi e la sospensione per la ricerca dei beni.'),
    ('/interessi-moratori/', 'Calcolo e tabella', 'Interessi moratori',
     'Tasso BCE più 8 punti semestre per semestre, la tabella dal 2002 e i casi particolari.'),
    ('/tassi/', 'Tabelle e verifiche', 'Tassi, fonti e verifiche',
     'Interessi legali e moratori, compenso del precetto, casi svolti a mano e registro.'),
]


def index_page(info):
    path = '/guide/'
    title = "Guide sul recupero crediti: per l'atto e per i clienti"
    desc = ('Approfondimenti per scrivere il precetto (termini, interessi, tassi) e guide semplici da mandare ai clienti: '
            'fattura non pagata, decreto ingiuntivo, precetto notificato.')
    card_list, items = cards(info)
    atto = '\n'.join('<li><a href="%s"><span class="k">%s</span><strong>%s</strong><span class="d">%s</span></a></li>' % a for a in ATTO)
    bp = comuni()
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": title, "description": desc, "url": BASE + path, "inLanguage": "it-IT",
         "isPartOf": {"@id": bp.SITO_ID}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guide", "item": BASE + path}]},
        {"@type": "ItemList", "itemListElement": items}]}
    ld = bp.con_nodi(ld)
    parts = [
        head(title, desc, path, "Gli approfondimenti per scrivere il precetto e le guide semplici da mandare ai clienti.", ld, og_type='website'),
        '<body class="guide">',
        nav('guide'),
        '',
        '<div class="wrap g-hero">',
        '  <div>',
        '    <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> Guide</nav>',
        '    <h1 class="g-title">Guide <mark>per te e per i tuoi clienti</mark></h1>',
        "    <p class=\"g-lead\">Due scaffali: gli approfondimenti che servono a te per scrivere l'atto e le guide semplici da mandare a chi deve farsi pagare.</p>",
        '  </div>',
        '  <aside class="g-brief" aria-labelledby="briefTitle">',
        '    <h2 id="briefTitle">Come usarle</h2>',
        '    <ul>',
        "      <li><mark>Per l'atto.</mark> Le regole tecniche, con il calcolo accanto e le fonti.</li>",
        '      <li><mark>Per i clienti.</mark> Cosa fare, in che ordine, con quali tempi e costi, senza gergo.</li>',
        '      <li><mark>Da mandare.</mark> Ogni guida ha il suo collegamento: copialo e mandalo per mail o in un messaggio.</li>',
        '    </ul>',
        '  </aside>',
        '</div>',
        '',
        '<main class="wrap g-index">',
        "<h2 id=\"atto\">Approfondimenti per l'atto</h2>",
        '<p class="g-sub">Per chi scrive il precetto: le regole, il calcolo accanto e le fonti di ogni numero.</p>',
        '<ul class="g-atto">',
        atto,
        '</ul>',
        '<h2 id="clienti">Da mandare ai clienti</h2>',
        '<p class="g-sub">Il percorso dal primo sollecito al pignoramento, in tre guide brevi. Ognuna si apre con il tasto per copiarne il collegamento.</p>',
        '<ol class="g-path">',
        card_list,
        '</ol>',
        '</main>',
        '',
        CONTACT,
        '',
        FOOTER,
        TAIL,
    ]
    return '\n'.join(parts)
