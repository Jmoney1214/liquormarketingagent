import click, json
from .dataio import read_json
from .pusher import render_email_html, render_subject, render_sms
@click.command()
@click.option("--plan", "plan_path", required=True, type=click.Path(exists=True))
@click.option("--mode", type=click.Choice(["email","sms","both"]), default="email", show_default=True)
@click.option("--limit", default=10, show_default=True)
def main(plan_path, mode, limit):
    plan = read_json(plan_path)
    sends = plan.get("sends", [])[:limit]
    print(f"Pretend sending {len(sends)} '{mode}' messages. Configure providers in pusher.py.")
if __name__ == "__main__":
    main()
