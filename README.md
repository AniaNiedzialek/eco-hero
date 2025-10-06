# eco-hero

## Setup
```
cd backend && pip install -r requirements.txt
```

## Run the backend

```
uvicorn main:app --reload --port 8000
```

## Rules API

-   **GET api/rules/{zip_code}**
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
