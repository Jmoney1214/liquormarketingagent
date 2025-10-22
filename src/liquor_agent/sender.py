import os
import time

import click

from .dataio import read_json
from .pusher import render_email_html, render_subject, render_sms

_TRUTHY_VALUES = ("1", "true", "yes")


@click.command()
@click.option("--plan", "plan_path", required=True, type=click.Path(exists=True))
@click.option(
    "--mode",
    type=click.Choice(["email", "sms", "both"]),
    default="email",
    show_default=True,
)
@click.option("--limit", default=10, show_default=True)
def main(plan_path, mode, limit):
    plan = read_json(plan_path)
    sends = plan.get("sends", [])[:limit]

    providers_enabled = os.getenv("ENABLE_PROVIDERS", "0").lower() in _TRUTHY_VALUES
    if not providers_enabled:
        print(
            f"Pretend sending {len(sends)} '{mode}' messages. Configure providers in "
            "pusher.py or set ENABLE_PROVIDERS=1 in .env to go live."
        )
        return

    from .pusher import send_email_mailgun, send_sms_twilio

    for item in sends:
        try:
            if mode in ("email", "both") and item.get("email"):
                subj = render_subject(item)
                html = render_email_html(item)
                text = item.get("text", "")
                resp = send_email_mailgun(item["email"], subj, html, text)
                print("EMAIL_SENT:", item.get("email"), "->", resp.get("status_code", resp))

            if mode in ("sms", "both") and item.get("phone"):
                sms_body = render_sms(item)
                resp = send_sms_twilio(item["phone"], sms_body)
                print("SMS_SENT:", item.get("phone"), "->", resp.get("sid", resp))

            time.sleep(0.5)
        except Exception as exc:
            print("SEND_ERROR:", repr(exc))


if __name__ == "__main__":
    main()
