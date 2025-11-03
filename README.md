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
cd backend && uvicorn main:app --reload --port 8000
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
## Schedule API (Only works with San Jose + Santa Clara)

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
## Scanner API
-   **POST /api/scanner/uploadfile/?zip_code=...**
    ```
    curl -s -X POST 'http://127.0.0.1:8000/api/scanner/uploadfile/?zip_code=95056' \
    -F 'file=@backend/data/barcodes/test_bc.png;type=image/png'
    ```
    -   **Example response**
        ```
        {
        "City of Santa Clara Curbside Recycling Program":"https://search.earth911.com/program/Q1RQNVBbU1dAVQ/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "Sunnyvale Materials Recovery and Transfer Station (SMaRT)":"https://search.earth911.com/location/Q1RQNVJYXF1GVQ/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "SMaRT Recycling Center":"https://search.earth911.com/location/Q1RQNVBRUltGXQ/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "San Jose Conservation Corps Recycling Drop-Off Center":"https://search.earth911.com/location/Q1RTNVBRWFlK/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "1-800-Got-Junk? ":"https://search.earth911.com/program/Q1RQNVJZW19DUg/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "Zanker Materials Recovery Facility":"https://search.earth911.com/location/Q1RQNVJYUllDXQ/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "International Paper":"https://search.earth911.com/location/Q1RTNVNYXlZE/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "Shoreway Environmental Center":"https://search.earth911.com/location/Q1RTNVVdWFdC/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all",
        "Pleasanton Transfer Station":"https://search.earth911.com/location/Q1RTNVJeXF1H/?what=Food%2C+Beverages+%26+Tobacco&where=95051&max_distance=25&country=US&province=CA&city=Santa+Clara&region=Santa+Clara&postal_code=95051&latitude=37.346878776894&longitude=-121.98557937233&sponsor=&list_filter=all"
        }
        ```
-   **POST /api/scanner/scanbarcode/?zip_code=...&barcode=...**
    ```
    curl -s 'http://127.0.0.1:8000/api/scanner/scanbarcode/?zip_code=95112&barcode=5449000009067'
    ```

## Bin Locations API (Find public bins near an address)
-   **GET /api/bin/near?addr=...&radius_miles=...&max_results=...**
    ```
    curl -sG 'http://127.0.0.1:8000/api/bin/near' \
    --data-urlencode 'addr=150 Alviso St, Santa Clara, CA' \
    --data-urlencode 'radius_miles=5' \
    --data-urlencode 'max_results=5'
    ```
    -   **Example response:**
        ```
        [
            {
                "id": 12610817977,
                "lat": 37.3483783,
                "lon": -121.9467481,
                "tags": {
                    "amenity": "waste_basket",
                    "waste": "trash"
                },
                "distance_miles": 0.7
            },...
        ]
        ```
