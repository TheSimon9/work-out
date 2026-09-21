# Scheda Full Body A·B·C

Webapp statica della scheda di allenamento: 3 sedute a settimana, foto reali animate di ogni esercizio, alternative per ogni macchina, registro di kg e ripetizioni, timer di recupero. Funziona offline dopo la prima apertura.

## Pubblicarla su Vercel

Sito statico, nessun build.

1. Su [vercel.com](https://vercel.com) → **Add New → Project** → importa il repo `TheSimon9/work-out`.
2. Framework preset: **Other**. Build command e output directory vuoti (la root è già il sito).
3. **Deploy**. Ogni push su `main` ripubblica in automatico.

`vercel.json` imposta `no-cache` su `index.html` e `sw.js`, così i telefoni vedono subito le nuove versioni.

## Usarla in palestra senza rete

1. Apri il link dal telefono **con la connessione attiva**: al primo caricamento l'app salva tutto (pagine, font, GIF).
2. Aggiungila alla schermata Home: su iPhone da Safari → Condividi → *Aggiungi alla schermata Home*; su Android da Chrome → menu → *Installa app*.
3. Da lì in poi si apre anche offline.

Se modifichi i contenuti, cambia `CACHE = "scheda-v3"` in `sw.js` (es. `v4`) così i telefoni scaricano la versione nuova.

## Registro e backup

Kg, ripetizioni e alternative scelte vengono salvati nel `localStorage` del browser, solo su quel telefono. Da *Regole → I tuoi dati* puoi esportare un file `.json` di backup e reimportarlo. Il registro è per esercizio: la leg press del lunedì e del venerdì condividono lo storico.

## Struttura

- `index.html` — tutta l'app (dati degli esercizi in cima allo script)
- `sw.js` — service worker per l'uso offline
- `anim/` — animazioni degli esercizi (WebP animati)
- `fonts/` — Barlow e Barlow Condensed (SIL Open Font License)

## Crediti

Foto degli esercizi dal progetto [Free Exercise DB](https://github.com/yuhonas/free-exercise-db), rilasciato nel pubblico dominio (Unlicense). Il dataset ha due foto per esercizio; i fotogrammi intermedi sono generati con interpolazione ottica (OpenCV) per rendere il movimento più fluido.
