import os
import base64
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def lookup_barcode_info(barcode: str) -> dict:
    """
    Look up product information from multiple barcode databases.
    Tries Open Food Facts (food), Open Products Facts (non-food), and UPC Item DB.
    
    Args:
        barcode: UPC/EAN/ISBN barcode number
    
    Returns:
        dict with product details from the database
    """
    try:
        # 1. Try Open Food Facts (food products)
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:  # Product found
                product = data.get("product", {})
                product_name = product.get("product_name", "")
                if product_name:  # Only use if we got a real name
                    return {
                        "found": True,
                        "product_name": product_name,
                        "brands": product.get("brands", ""),
                        "categories": product.get("categories", ""),
                        "packaging": product.get("packaging", ""),
                        "materials": product.get("packaging_materials", ""),
                        "quantity": product.get("quantity", ""),
                        "image_url": product.get("image_url", ""),
                        "source": "Open Food Facts"
                    }
        
        # 2. Try Open Products Facts (non-food: electronics, beauty, pet food, etc.)
        url2 = f"https://world.openproductsfacts.org/api/v0/product/{barcode}.json"
        response2 = requests.get(url2, timeout=5)
        
        if response2.status_code == 200:
            data2 = response2.json()
            if data2.get("status") == 1:
                product = data2.get("product", {})
                product_name = product.get("product_name", "")
                if product_name:
                    return {
                        "found": True,
                        "product_name": product_name,
                        "brands": product.get("brands", ""),
                        "categories": product.get("categories", ""),
                        "packaging": product.get("packaging", ""),
                        "materials": product.get("packaging_materials", ""),
                        "quantity": product.get("quantity", ""),
                        "image_url": product.get("image_url", ""),
                        "source": "Open Products Facts"
                    }
        
        # 3. Try UPC Item DB (general products database)
        url3 = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
        response3 = requests.get(url3, timeout=5)
        
        if response3.status_code == 200:
            data3 = response3.json()
            if data3.get("items"):
                item = data3["items"][0]
                return {
                    "found": True,
                    "product_name": item.get("title", "Unknown"),
                    "brands": item.get("brand", ""),
                    "categories": item.get("category", ""),
                    "packaging": "",
                    "materials": "",
                    "quantity": "",
                    "image_url": item.get("images", [None])[0] if item.get("images") else "",
                    "source": "UPC Item DB"
                }
        
        return {"found": False}
        
    except Exception as e:
        print(f"Barcode lookup error: {e}")
        return {"found": False}

def identify_product_with_gemini(image_bytes: bytes, barcode: str = None) -> dict:
    """
    Use Gemini Vision API to identify a product from an image and provide recycling guidance.
    
    Args:
        image_bytes: Raw image bytes
        barcode: Optional barcode number for additional context
    
    Returns:
        dict with product_name, category, material, and recycling_guidance
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set")
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Prepare the image
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_bytes).decode()
        }
    ]
    
    # Craft a detailed prompt
    prompt = f"""Analyze this product image and provide recycling information.
    
{"Barcode detected: " + barcode if barcode else ""}

Please provide the following information in JSON format:
{{
    "product_name": "name of the product",
    "category": "product category (e.g., 'Food, Beverages & Tobacco', 'Plastics', 'Electronics')",
    "material": "primary material (e.g., 'plastic', 'aluminum', 'glass', 'paper', 'mixed')",
    "recyclable": true/false,
    "recycling_guidance": "specific recycling instructions for this item",
    "bin_type": "which bin to use (e.g., 'Blue Recycling', 'Green Organics', 'Gray Trash')",
    "special_notes": "any special handling notes (e.g., 'rinse before recycling', 'remove cap')"
}}

Be specific and provide practical recycling advice based on common California recycling programs."""

    response = model.generate_content([prompt, image_parts[0]])
    
    # Parse the response
    try:
        import json
        import re
        # Extract JSON from markdown code blocks if present
        text = response.text.strip()
        
        # Try to find JSON in the response - it might be wrapped in markdown or have extra text
        # Look for content between triple backticks with optional 'json' label
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
        else:
            # If no code blocks, try to find a JSON object in the text
            json_match = re.search(r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                json_text = text
        
        result = json.loads(json_text)
        result["data_source"] = "Gemini Vision AI"
        return result
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response.text[:500]}")
        # Fallback if JSON parsing fails
        return {
            "product_name": "Unknown",
            "category": "General",
            "material": "unknown",
            "recyclable": False,
            "recycling_guidance": response.text,
            "bin_type": "Contact local facility",
            "special_notes": "Could not parse structured data"
        }


def get_recycling_info_from_barcode(barcode: str) -> dict:
    """
    Use barcode lookup API + Gemini to get accurate recycling information.
    
    Args:
        barcode: UPC/EAN barcode number
    
    Returns:
        dict with recycling information
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set")
    
    # First, lookup the product in barcode database
    product_info = lookup_barcode_info(barcode)
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Build a more informed prompt with product data
    if product_info.get("found"):
        product_context = f"""
Product Information from barcode database:
- Name: {product_info.get('product_name', 'Unknown')}
- Brand: {product_info.get('brands', 'Unknown')}
- Categories: {product_info.get('categories', 'Unknown')}
- Packaging: {product_info.get('packaging', 'Unknown')}
- Materials: {product_info.get('materials', 'Unknown')}
- Quantity: {product_info.get('quantity', 'Unknown')}
"""
        prompt = f"""Based on the following verified product information for barcode {barcode}:

{product_context}

Please provide ACCURATE recycling information in JSON format. Pay special attention to the packaging and materials fields to determine the correct material type (plastic, aluminum, glass, etc.):

{{
    "product_name": "name of the product",
    "category": "product category",
    "material": "primary material - MUST be accurate based on packaging info above",
    "recyclable": true/false,
    "recycling_guidance": "specific recycling instructions",
    "bin_type": "which bin to use in California",
    "special_notes": "any special handling notes"
}}

If the packaging shows 'PET', 'HDPE', 'plastic bottle', etc., the material should be 'plastic'.
If it shows 'aluminum can', the material should be 'aluminum'.
If it shows 'glass bottle', the material should be 'glass'.
Be precise and accurate."""
    else:
        # Fallback to barcode-only lookup
        prompt = f"""Given this product barcode: {barcode}

The barcode was not found in product databases. Please try to identify what product this might be and provide recycling information in JSON format:
{{
    "product_name": "name of the product (if recognizable)",
    "category": "product category",
    "material": "primary material",
    "recyclable": true/false,
    "recycling_guidance": "specific recycling instructions",
    "bin_type": "which bin to use in California",
    "special_notes": "Note: Product not found in database, information may be uncertain"
}}"""

    response = model.generate_content(prompt)
    
    try:
        import json
        import re
        text = response.text.strip()
        
        # Try to find JSON in the response - it might be wrapped in markdown or have extra text
        # Look for content between triple backticks with optional 'json' label
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
        else:
            # If no code blocks, try to find a JSON object in the text
            json_match = re.search(r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                json_text = text
        
        result = json.loads(json_text)
        
        # Add source info - show which database was used
        if product_info.get("found"):
            result["data_source"] = product_info.get("source", "Barcode Database")
        else:
            result["data_source"] = "Gemini Vision AI"
        
        return result
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response.text[:500]}")
        # Fallback if JSON parsing fails
        return {
            "product_name": product_info.get("product_name", "Unknown") if product_info.get("found") else "Unknown",
            "category": "General",
            "material": "unknown",
            "recyclable": False,
            "recycling_guidance": response.text,
            "bin_type": "Contact local facility",
            "special_notes": "Could not parse structured data",
            "data_source": "Parse error"
        }
