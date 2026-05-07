import click
from rich.console import Console
from rich.table import Table
from rich import box
from . import calendar_client as cal

console = Console()


@click.group()
def cli():
    """TechJourneyJosh Planner — powered by Google Calendar MCP."""


@cli.command("list")
@click.option("--max", "max_results", default=10, show_default=True, help="Max events to show")
@click.option("--calendar", default="primary", show_default=True, help="Calendar ID")
def list_events(max_results, calendar):
    """List upcoming calendar events."""
    events = cal.list_events(max_results=max_results, calendar_id=calendar)
    if not events:
        console.print("[yellow]No upcoming events found.[/yellow]")
        return

    table = Table(title="Upcoming Events", box=box.ROUNDED)
    table.add_column("#", style="dim", width=3)
    table.add_column("Event", style="bold")
    table.add_column("Start", style="cyan")
    table.add_column("ID", style="dim")

    for i, event in enumerate(events, 1):
        start = event["start"].get("dateTime", event["start"].get("date", ""))
        table.add_row(str(i), event.get("summary", "(no title)"), start, event["id"])

    console.print(table)


@cli.command("add")
@click.argument("summary")
@click.argument("start")  # ISO 8601 e.g. 2026-05-10T09:00:00Z
@click.argument("end")
@click.option("--desc", default="", help="Event description")
@click.option("--calendar", default="primary", show_default=True, help="Calendar ID")
def add_event(summary, start, end, desc, calendar):
    """Add a new event to the calendar.

    START and END must be ISO 8601 datetime strings, e.g. 2026-05-10T09:00:00Z
    """
    event = cal.create_event(
        summary=summary,
        start=start,
        end=end,
        description=desc,
        calendar_id=calendar,
    )
    console.print(f"[green]Created:[/green] {event.get('summary')} — {event.get('htmlLink')}")


@cli.command("delete")
@click.argument("event_id")
@click.option("--calendar", default="primary", show_default=True, help="Calendar ID")
@click.confirmation_option(prompt="Are you sure you want to delete this event?")
def delete_event(event_id, calendar):
    """Delete an event by its ID."""
    cal.delete_event(event_id=event_id, calendar_id=calendar)
    console.print(f"[red]Deleted[/red] event {event_id}")
