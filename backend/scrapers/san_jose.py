import re
from typing import Optional, Dict, List
from datetime import datetime

async def get_san_jose_schedule(address: str) -> Optional[List[Dict]]:
    """
    Scrape San Jose 311 collection schedule using Playwright automation.
    Address required (e.g., "200 E Santa Clara St, San Jose, CA").
    Returns schedule with collection types and dates.
    """
    if not address or len(address.strip()) < 5:
        return None
    
    try:
        from playwright.async_api import async_playwright
        from playwright_stealth import Stealth
        
        async with async_playwright() as p:
            # Launch browser in headless mode with stealth settings
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            # Apply stealth mode to avoid detection
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            
            try:
                # Navigate to San Jose 311 Collection Schedule page
                await page.goto(
                    "https://311.sanjoseca.gov/?osvcProductName=My%20Collection%20Schedule&page=shell&shell=home&home=home-collectionschedule_opa",
                    wait_until="networkidle",
                    timeout=60000
                )
                
                # Wait for the address input to be visible and ready
                await page.wait_for_selector('input[role="combobox"]', state='visible', timeout=30000)
                await page.wait_for_timeout(1500)
                
                # Get the input element and click it
                combobox = page.locator('input[role="combobox"]').first
                box = await combobox.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                    await page.wait_for_timeout(100)
                    await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                    await page.wait_for_timeout(300)
                else:
                    await combobox.click()
                    await page.wait_for_timeout(300)
                
                # Type the address character by character
                for char in address:
                    await page.keyboard.press(char)
                    await page.wait_for_timeout(80)
                
                # Wait for autocomplete to render
                await page.wait_for_timeout(1500)
                
                # Use keyboard navigation to select first autocomplete option
                await page.keyboard.press('ArrowDown')
                await page.wait_for_timeout(300)
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(800)
                
                # Click the Search button
                search_button = page.get_by_text('Search', exact=False).first
                await search_button.click()
                
                # Wait for results table to appear
                await page.wait_for_selector('table tbody tr', state='visible', timeout=15000)
                await page.wait_for_timeout(2000)
                
                # Extract schedule data from the calendar
                schedule = []
                
                # Get current month/year from calendar header
                current_month = datetime.now().month
                current_year = datetime.now().year
                
                try:
                    month_header = await page.locator('h2, h3, [role="heading"]').filter(has_text=re.compile(r'(January|February|March|April|May|June|July|August|September|October|November|December)')).first.inner_text()
                    month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', month_header)
                    if month_match:
                        month_name, year_str = month_match.groups()
                        current_year = int(year_str)
                        month_map = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4,
                            'May': 5, 'June': 6, 'July': 7, 'August': 8,
                            'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        current_month = month_map[month_name]
                except:
                    pass
                
                # Extract collection dates from grid cells
                grid_cells = await page.query_selector_all('[role="gridcell"]')
                
                for cell in grid_cells:
                    try:
                        cell_text = await cell.inner_text()
                        cell_text = cell_text.strip()
                        
                        # Check if cell has multiple lines (day + collection type)
                        lines = cell_text.split('\n')
                        if len(lines) >= 2:
                            day_str = lines[0].strip()
                            collection_info = '\n'.join(lines[1:]).strip()
                            
                            if day_str.isdigit():
                                day = int(day_str)
                                
                                # Check for waste collection keywords
                                has_collection = any(keyword in collection_info for keyword in 
                                                   ['Yard', 'yard', 'Garbage', 'garbage', 'Recycling', 'recycling'])
                                
                                if has_collection:
                                    try:
                                        date_obj = datetime(current_year, current_month, day)
                                        date_str = date_obj.strftime("%Y-%m-%d")
                                        
                                        # Parse collection types
                                        types = []
                                        if 'Yard' in collection_info or 'yard' in collection_info:
                                            types.append('Yard waste')
                                        if 'Garbage' in collection_info or 'garbage' in collection_info:
                                            types.append('Garbage')
                                        if 'Recycling' in collection_info or 'recycling' in collection_info:
                                            types.append('Recycling')
                                        
                                        if types:
                                            schedule.append({
                                                "date": date_str,
                                                "type": ", ".join(types)
                                            })
                                    except ValueError:
                                        pass
                    except:
                        continue
                
                await browser.close()
                return schedule if schedule else None
                
            except Exception as e:
                await browser.close()
                return None
                
    except Exception as e:
        return None
