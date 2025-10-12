from dotenv import load_dotenv
import resend
import os

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

FROM_EMAIL = os.getenv("RESEND_FROM", "onboarding@resend.dev")


def _render_html(address: str, city: str, state: str, items: list) -> str:
    """Generate HTML email from schedule data"""
    if not items:
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Waste Collection Schedule</h2>
            <p><strong>Address:</strong> {address}</p>
            <p><strong>Location:</strong> {city}, {state}</p>
            <p>No upcoming collection dates found.</p>
        </div>
        """
    
    # Build collection dates list
    items_html = ""
    for item in items:
        items_html += f"""
        <div style="padding: 12px; margin: 8px 0; background: #f5f5f5; border-radius: 6px;">
            <strong>{item['date']}</strong> - {item['type']}
        </div>
        """
    
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2d6a4f;">Your Waste Collection Schedule</h2>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Location:</strong> {city}, {state}</p>
        
        <h3 style="color: #40916c;">Upcoming Collections:</h3>
        {items_html}
        
        <p style="margin-top: 20px; color: #666; font-size: 14px;">
            This is your waste collection schedule. Please place bins out by 6 AM on collection day.
        </p>
    </div>
    """


def send_notification(email: str, schedule: dict):
    """Send collection schedule email notification"""
    if not resend.api_key:
        raise RuntimeError("RESEND_API_KEY is not set")
    if not email:
        raise ValueError("email is required")
    
    # Extract data from schedule dict
    address = schedule.get("address", "Unknown")
    city = schedule.get("city", "Unknown")
    state = schedule.get("state", "Unknown")
    items = schedule.get("schedule", [])  
    
    if city == "san jose" or city == "San José" or city == "San Jose":
        # Generate HTML email
        html_content = _render_html(address, city, state, items)
    else:
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Waste Collection Schedule</h2>
            <p><strong>Address:</strong> {address}</p>
            <p><strong>Location:</strong> {city}, {state}</p>
            <p>Your collection schedule can be found here: <a href="{items}">{items}</a></p>
        </div>
        """
    
    # Send email
    r = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": email,
        "subject": f"Waste Collection Schedule for {address}",
        "html": html_content
    })
    
    return r