# Rackspace Ticket API Response Structure

## Ticket List Response (`GET /tickets`)

```json
{
  "tickets": [
    {
      "ticketId": "250722-03057",                    // Always present
      "subject": "RSDP Successful Transition",       // Always present
      "status": "Pending Customer",                  // Always present
      "modified": "2025-08-05T21:56:32.000Z",       // Always present
      
      // Additional fields in list view
      "accountId": "hybrid:844792",
      "severity": "",                                // Can be empty string
      "favorite": false,
      "resources": ["https://..."],
      "createdAt": "0001-01-01T00:00:00Z",          // Often invalid date in list!
      "modifiedBy": {
        "id": "",
        "name": "Aaditya Kumar",
        "roles": ["Racker"],
        "type": "racker"
      },
      "createdBy": {
        "id": "RPN-100-001-470-862",              // Can be empty
        "name": "Name Here",
        "roles": ["Technical"],
        "type": "customer"                        // or "racker"
      },
      "classification": "",                       // Can be empty
      "lastComment": {
        "text": "truncated comment text..."
      },
      "permission": "admin",
      "recipients": null                          // Often null in list view
    }
  ],
  "total": 12145,
  "_links": {
    "self": "https://demo.ticketing.api.rackspace.com/tickets?limit=2&offset=0",
    "first": "...",
    "last": "...",
    "prev": "",
    "next": "..."
  }
}
```

## Single Ticket Response (`GET /tickets/{ticketId}`)

```json
{
  "ticketId": "250722-03057",                        // Same as list
  "subject": "RSDP Successful Transition",           // Same as list
  "status": "Pending Customer",                      // Same as list
  "modified": "2025-08-05T21:56:32.000Z",           // Same as list
  
  "created": "2025-07-22T20:45:18.000Z",            // Valid date in detail!
  "accountId": "hybrid:844792",
  "severity": "Urgent",                              // More likely to have value
  "favorite": false,
  "resources": ["https://..."],
  
  "modifiedBy": { /* same structure */ },
  "createdBy": { /* same structure */ },
  
  "classification": "Incident",                      // More complete in detail
  "category": "Migration",                           // Only in detail view
  "subcategory": "Cohesity",                        // Only in detail view
  
  "recipients": [                                    // Full list in detail
    {
      "firstName": "David",
      "lastName": "Levy",
      "id": "RPN-160-868-186",
      "username": "davelevy",
      "roles": ["Primary", "Technical", "Billing", "Nps"],
      "email": "david.levy@gerberlife.com"
    }
  ],
  
  "comments": [                                      // Full comments in detail
    {
      "created": "2025-07-24T18:26:48.000Z",
      "id": "531126898",
      "text": "Full comment text...",
      "author": {
        "id": "",
        "name": "Aaditya Kumar",
        "roles": ["Racker"],
        "type": "racker"
      },
      "attachments": [],
      "format": "bbcode"
    }
  ],
  
  "permission": "admin"
}
```

## Key Differences Between List and Detail

| Field | List View | Detail View |
|-------|-----------|-------------|
| **created** | Not present | Full ISO timestamp |
| **createdAt** | Invalid date (0001-01-01) | Not present |
| **category** | Not present | Full value |
| **subcategory** | Not present | Full value |
| **recipients** | Usually null | Full array |
| **comments** | Not present | Full array |
| **lastComment** | Truncated text | Not present |
| **classification** | Often empty | Full value |

## Model Requirements

Based on this analysis, our Pydantic model needs:
1. `ticketId` not `id`
2. `modified` not `updated_at`
3. `created` (optional - only in detail view)
4. `createdAt` (optional - only in list view, often invalid)
5. Flexible handling of empty strings vs None
6. Comments array that's empty in list view
7. Recipients that can be null or array