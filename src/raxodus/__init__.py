"""raxodus - Escape from Rackspace ticket hell."""

__version__ = "0.1.0"
__author__ = "Brian Morin"

from .client import RackspaceClient
from .models import Ticket, TicketList

__all__ = ["RackspaceClient", "Ticket", "TicketList"]