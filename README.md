# Bot Pax Dei – impostazione server

Il bot ricrea il server Discord seguendo `struttura.json` (ruoli, categorie, canali).
Per cambiare la struttura modifica solo `struttura.json`.

## Come si usa
1. Su https://discord.com/developers/applications crea un'applicazione → **Bot** → copia il token.
2. **OAuth2 → URL Generator**: spunta `bot` e il permesso `Administrator`, apri il link e invita il bot nel server.
3. Su Discord attiva *Modalità sviluppatore*, tasto destro sul server → **Copia ID server**.
4. Sul tuo computer:
   ```
   pip install -r requirements.txt
   export DISCORD_TOKEN=il_tuo_token
   export GUILD_ID=id_del_server
   python imposta_server.py --reset   # cancella i vecchi canali e ricrea tutto
   ```
   Senza `--reset` aggiunge solo ciò che manca.

⚠️ `--reset` cancella **tutti** i canali e i loro messaggi. Non si può annullare.
Non condividere mai il token con nessuno.
