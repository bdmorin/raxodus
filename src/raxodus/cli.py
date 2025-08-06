"""Command-line interface for raxodus."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .client import RackspaceClient
from .exceptions import AuthenticationError, RaxodusError
from .formatters import format_csv, format_json, format_table

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="raxodus")
@click.pass_context
def cli(ctx):
    """raxodus - Escape from Rackspace ticket hell.
    
    Set credentials via environment variables:
    
        export RACKSPACE_USERNAME="your-username"
        export RACKSPACE_API_KEY="your-api-key"
        export RACKSPACE_ACCOUNT="123456"
    """
    ctx.ensure_object(dict)


@cli.group()
def auth():
    """Authentication commands."""
    pass


@auth.command()
def test():
    """Test authentication credentials."""
    try:
        with RackspaceClient() as client:
            token = client.authenticate()
            console.print("[green]✓[/green] Authentication successful!")
            console.print(f"  User ID: {token.user_id}")
            console.print(f"  Token expires: {token.expires_at}")
            if token.accounts:
                console.print(f"  Accounts: {', '.join(token.accounts)}")
    except AuthenticationError as e:
        console.print(f"[red]✗[/red] Authentication failed: {e}")
        sys.exit(1)
    except RaxodusError as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.group()
def tickets():
    """Ticket management commands."""
    pass


@tickets.command("list")
@click.option("--account", help="Rackspace account number")
@click.option("--status", help="Filter by status (open, closed, pending)")
@click.option("--days", type=int, help="Show tickets from last N days")
@click.option("--page", type=int, default=1, help="Page number")
@click.option("--per-page", type=int, default=100, help="Results per page")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="json",
    help="Output format",
)
def list_tickets(account, status, days, page, per_page, output_format):
    """List support tickets."""
    try:
        with RackspaceClient() as client:
            result = client.list_tickets(
                account=account,
                status=status,
                days=days,
                page=page,
                per_page=per_page,
            )
            
            if output_format == "json":
                click.echo(format_json(result.to_summary()))
            elif output_format == "table":
                click.echo(format_table(result))
            elif output_format == "csv":
                click.echo(format_csv(result))
                
    except RaxodusError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)


@tickets.command("get")
@click.argument("ticket_id")
@click.option("--account", help="Rackspace account number")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table"]),
    default="json",
    help="Output format",
)
def get_ticket(ticket_id, account, output_format):
    """Get a specific ticket."""
    try:
        with RackspaceClient() as client:
            ticket = client.get_ticket(ticket_id, account=account)
            
            if output_format == "json":
                click.echo(format_json(ticket.model_dump(mode="json")))
            elif output_format == "table":
                # Create detailed table
                table = Table(title=f"Ticket {ticket.id}")
                table.add_column("Field", style="cyan")
                table.add_column("Value")
                
                table.add_row("ID", ticket.id)
                table.add_row("Subject", ticket.subject)
                table.add_row("Status", ticket.status)
                table.add_row("Severity", ticket.severity or "N/A")
                table.add_row("Created", ticket.created_at.isoformat())
                table.add_row("Updated", ticket.updated_at.isoformat())
                table.add_row("Requester", ticket.requester or "N/A")
                table.add_row("Assigned To", ticket.assigned_to or "N/A")
                
                console.print(table)
                
    except RaxodusError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)


@tickets.command("search")
@click.argument("query")
@click.option("--account", help="Rackspace account number")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "csv"]),
    default="json",
    help="Output format",
)
def search_tickets(query, account, output_format):
    """Search for tickets."""
    try:
        with RackspaceClient() as client:
            result = client.search_tickets(query, account=account)
            
            if output_format == "json":
                click.echo(format_json(result.to_summary()))
            elif output_format == "table":
                click.echo(format_table(result))
            elif output_format == "csv":
                click.echo(format_csv(result))
                
    except RaxodusError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()