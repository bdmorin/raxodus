"""Pydantic models for Rackspace API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class TicketAttachment(BaseModel):
    """Attachment on a ticket."""
    
    id: str
    filename: str
    size: int
    created_at: datetime
    url: Optional[str] = None


class TicketComment(BaseModel):
    """Comment on a ticket."""
    
    id: str
    author: str
    created_at: datetime
    body: str
    is_public: bool = True
    attachments: List[TicketAttachment] = Field(default_factory=list)


class Ticket(BaseModel):
    """Rackspace support ticket."""
    
    id: str
    subject: str
    status: str
    severity: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    account_id: Optional[str] = None
    requester: Optional[str] = None
    assigned_to: Optional[str] = None
    description: Optional[str] = None
    resolution: Optional[str] = None
    comments: List[TicketComment] = Field(default_factory=list)
    
    class Config:
        extra = "ignore"  # Future-proof against API changes
    
    @field_validator("status")
    @classmethod
    def normalize_status(cls, v: str) -> str:
        """Normalize status values."""
        return v.lower().replace(" ", "_")
    
    def to_summary(self) -> Dict[str, Any]:
        """Return a summary dict for list views."""
        return {
            "id": self.id,
            "subject": self.subject,
            "status": self.status,
            "severity": self.severity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class TicketList(BaseModel):
    """List of tickets response."""
    
    tickets: List[Ticket]
    total: int
    page: int = 1
    per_page: int = 100
    
    def to_summary(self) -> Dict[str, Any]:
        """Return summary for JSON output."""
        return {
            "total": self.total,
            "page": self.page,
            "per_page": self.per_page,
            "tickets": [t.to_summary() for t in self.tickets],
        }


class AuthToken(BaseModel):
    """Authentication token response."""
    
    token: str
    expires_at: datetime
    user_id: str
    accounts: List[str] = Field(default_factory=list)
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at


class RackspaceAccount(BaseModel):
    """Rackspace account information."""
    
    id: str
    name: str
    type: str = "managed"
    status: str = "active"
    
    class Config:
        extra = "ignore"