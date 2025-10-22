import os
from typing import Dict, Any, Optional

def render_subject(item: Dict[str, Any]) -> str:
    return f"{item.get('primary_category','Your favorites')} • {item.get('offer','Special offer')}"

def render_email_html(item: Dict[str, Any]) -> str:
    offer = item.get("offer", "Special offer")
    hint = item.get("creative_hint", "")
    seg = item.get("segment", "Customer")
    disclaimer = os.getenv("LEGAL_DISCLAIMER", "Please drink responsibly. Must be 21+. Opt-out anytime.")
    return """<html>
  <body>
    <h2>{offer}</h2>
    <p>{hint}</p>
    <p><em>Segment:</em> {seg}</p>
    <hr/><small>{disclaimer}</small>
  </body>
</html>""".format(offer=offer, hint=hint, seg=seg, disclaimer=disclaimer)

def render_sms(item: Dict[str, Any]) -> str:
    disclaimer = os.getenv("LEGAL_DISCLAIMER_SMS", "21+ only. Reply STOP to opt out.")
    return f"{item.get('offer','Special offer')} | {disclaimer}"

def send_email_mailgun(to_email: str, subject: str, html: str, text: Optional[str] = None) -> Dict[str, Any]:
    # lazy import so module loads even if requests not installed
    import requests
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")
    sender = os.getenv("MAILGUN_FROM", f"postmaster@{domain}" if domain else "noreply@example.com")
    if not api_key or not domain:
        raise RuntimeError("MAILGUN_API_KEY and MAILGUN_DOMAIN are required for Mailgun email.")
    resp = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": sender,
            "to": [to_email],
            "subject": subject,
            "text": text or "",
            "html": html
        },
        timeout=20
    )
    return {"status_code": resp.status_code, "body": resp.text}

def send_sms_twilio(to_number: str, body: str) -> Dict[str, Any]:
    # lazy import Twilio so module import errors are clearer at runtime
    from twilio.rest import Client
    account = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    if not all([account, token, from_number]):
        raise RuntimeError("TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER are required for Twilio SMS.")
    client = Client(account, token)
    msg = client.messages.create(from_=from_number, to=to_number, body=body)
    return {"sid": getattr(msg, "sid", None), "status": getattr(msg, "status", None)}
