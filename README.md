# Instagram AI Agent

Automaticky odesílá zprávy novým followerům a odpovídá na komentáře.

## Nastavení na Render.com

1. Nahraj kód na GitHub (bez .env souboru!)
2. Na Render.com vytvoř **New Web Service** → propoj GitHub repozitář
3. Nastav **Environment Variables** v Render dashboardu:

| Proměnná | Hodnota |
|---|---|
| `INSTAGRAM_ACCESS_TOKEN` | tvůj nový token |
| `INSTAGRAM_PAGE_ID` | `17841407937159484` |
| `APP_SECRET` | tvůj nový app secret |
| `VERIFY_TOKEN` | `mojetajneheslo6769` |

4. Start Command: `gunicorn main:app --bind 0.0.0.0:$PORT --workers 2`
5. Po deployi zkopíruj URL ze Render (např. `https://instagram-agent.onrender.com`)
6. V Meta Developer Console nastav Webhook na tuto URL + `/webhook`

## Úprava zpráv

Otevři `agent/messages.py` a uprav šablony dle libosti.
