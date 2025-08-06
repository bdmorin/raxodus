"""raxodus - Escape from Rackspace ticket hell."""

from .version import __version__, __codename__, __tagline__, get_avatar_url, get_version_info
from .client import RackspaceClient
from .models import Ticket, TicketList

__author__ = "Brian Morin"

__all__ = [
    "RackspaceClient", 
    "Ticket", 
    "TicketList",
    "__version__",
    "__codename__",
    "__tagline__",
    "get_avatar_url",
    "get_version_info",
]