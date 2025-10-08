# eco-hero

## Setup
```
cd backend && pip install -r requirements.txt
python -m playwright install chromium
```

## Set environment variables
```
cd backend && touch .env
echo "RESEND_API_KEY=YOUR_API_KEY" > .env 
```
Change YOUR_API_KEY to your resend api key (https://resend.com/)

## Run the backend

```
uvicorn main:app --reload --port 8000
```

## Rules API

-   **GET /api/rules/{zip_code}**
    ```
    curl -s http://127.0.0.1:8000/api/rules/94103 
    ```
    -   **Example response:**
        ```
        {
            "zip": "94103",
            "match_level": "state",
            "match_name": "CA",
            "region": {
                "state": "CA",
                "city": "San Francisco"
            },
            "summary": "Applied California statewide baseline.",
            "rules": {
                "organics": {
                    "guidance": "Residential and commercial organics separation program required statewide. Use green bin where available; check city for accepted items (food scraps, yard trimmings, soiled paper).",
                    "bin": "Green (Organics)",
                    "notes": "Some cities accept meat/dairy; others do not.",
                    "provenance": ["CalRecycle program guidance (SB 1383)"]
                },
                "plastics": {
                    "guidance": "Bottles, jugs, and tubs commonly accepted. Other plastics vary by city; check local list.",
                    "bin": "Blue (Recycling)",
                    "notes": "Plastic bags/film NOT curbside; take-back at participating stores.",
                    "provenance": ["Common statewide curbside guidance"]
                }
            }
        }
        ```
## Schedule API (Only works with San Jose)

-   **GET /api/collection/schedule?address=...&zip_code=...**
    ```
    curl -sG 'http://127.0.0.1:8000/api/collection/schedule' \
    --data-urlencode 'address=200 E Santa Clara St' \
    --data-urlencode 'zip_code=95112'
    ```
    -   **Example response:**
        ```
        {
        "address": "200 E Santa Clara St",
        "schedule": [
            {
            "date": "2025-10-06",
            "type": "Yard waste"
            },
            {
            "date": "2025-10-13",
            "type": "Yard waste"
            },
            {
            "date": "2025-10-20",
            "type": "Yard waste"
            },
            {
            "date": "2025-10-27",
            "type": "Yard waste"
            }
        ],
        "city": "San Jose",
        "state": "CA"
        }
        ```

-   **POST /api/collection/notify?email=...&address=...&zip_code=...**
    ```
    curl -s -X POST 'http://127.0.0.1:8000/api/collection/notify' \
    -H 'Content-Type: application/json' \
    -d '{"email":"you@example.com","address":"200 E Santa Clara St","zip_code":"95112"}'
    ```
    -   Send collection schedule to email