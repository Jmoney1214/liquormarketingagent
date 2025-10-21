import os
def render_email_html(item): return f"<h2>{item.get('offer','Special')}</h2>"
def render_subject(item): return f"{item.get('primary_category','Your favorites')} • {item.get('offer','Special')}"
def render_sms(item): return f"{item.get('offer','Special offer')} | 21+ only. Reply STOP to opt out."
# Mailgun/Twilio senders can be added here (see README)
