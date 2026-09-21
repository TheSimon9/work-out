# Scheda Full Body A·B·C

Webapp statica della scheda di allenamento: 3 sedute a settimana, foto reali animate di ogni esercizio, alternative per ogni macchina, registro di kg e ripetizioni, timer di recupero. Funziona offline dopo la prima apertura.

## Pubblicarla su GitHub Pages

1. Crea un repository nuovo (es. `scheda`) e carica il contenuto di questa cartella nella root.
   ```bash
   git init && git add . && git commit -m "Scheda full body"
   git branch -M main
   git remote add origin git@github.com:<utente>/scheda.git
   git push -u origin main
   ```
2. Su GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**, scegli `main` e cartella `/ (root)`.
3. Dopo un minuto la trovi su `https://<utente>.github.io/scheda/`.

## Usarla in palestra senza rete

1. Apri il link dal telefono **con la connessione attiva**: al primo caricamento l'app salva tutto (pagine, font, GIF).
2. Aggiungila alla schermata Home: su iPhone da Safari → Condividi → *Aggiungi alla schermata Home*; su Android da Chrome → menu → *Installa app*.
3. Da lì in poi si apre anche offline.

Se modifichi i contenuti, cambia `CACHE = "scheda-v2"` in `sw.js` (es. `v3`) così i telefoni scaricano la versione nuova.

## Registro e backup

Kg, ripetizioni e alternative scelte vengono salvati nel `localStorage` del browser, solo su quel telefono. Da *Regole → I tuoi dati* puoi esportare un file `.json` di backup e reimportarlo. Il registro è per esercizio: la leg press del lunedì e del venerdì condividono lo storico.

## Struttura

- `index.html` — tutta l'app (dati degli esercizi in cima allo script)
- `sw.js` — service worker per l'uso offline
- `anim/` — animazioni degli esercizi (WebP animati)
- `fonts/` — Barlow e Barlow Condensed (SIL Open Font License)

## Crediti

Foto degli esercizi dal progetto [Free Exercise DB](https://github.com/yuhonas/free-exercise-db), rilasciato nel pubblico dominio (Unlicense). Il dataset ha due foto per esercizio; i fotogrammi intermedi sono generati con interpolazione ottica (OpenCV) per rendere il movimento più fluido.
