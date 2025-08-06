#!/usr/bin/env python3
"""Test script to examine actual Rackspace API responses."""

import httpx
import json
import os
from pprint import pprint

def main():
    # Set credentials
    username = 'bmorin-provision'
    api_key = 'e09cdbe3e8294630aa5ca13bd0d56cde'
    
    # Authenticate
    auth_url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    auth_data = {
        'auth': {
            'RAX-KSKEY:apiKeyCredentials': {
                'username': username,
                'apiKey': api_key
            }
        }
    }
    
    print("Authenticating...")
    client = httpx.Client(timeout=60.0)  # Longer timeout
    auth_response = client.post(auth_url, json=auth_data)
    auth_response.raise_for_status()
    
    auth_json = auth_response.json()
    token = auth_json['access']['token']['id']
    print(f"Got token: {token[:20]}...")
    
    # Check service catalog for ticket endpoints
    print("\n=== SERVICE CATALOG ===")
    service_catalog = auth_json['access'].get('serviceCatalog', [])
    for service in service_catalog:
        if 'ticket' in service.get('name', '').lower() or 'support' in service.get('name', '').lower():
            print(f"Service: {service['name']}")
            print(f"Type: {service.get('type')}")
            for endpoint in service.get('endpoints', []):
                print(f"  - {endpoint.get('publicURL')}")
    
    # Also list all services
    print("\n=== ALL SERVICES ===")
    for service in service_catalog:
        print(f"- {service['name']} ({service.get('type')})")
        for endpoint in service.get('endpoints', [])[:1]:  # Just first endpoint
            print(f"  URL: {endpoint.get('publicURL')}")
    
    # Get ticket list
    headers = {
        'X-Auth-Token': token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("\nFetching ticket list...")
    list_url = 'https://demo.ticketing.api.rackspace.com/tickets'
    list_response = client.get(list_url, headers=headers, params={'limit': 2})
    list_response.raise_for_status()
    
    list_data = list_response.json()
    
    print('\n=== TICKET LIST RESPONSE ===')
    print(json.dumps(list_data, indent=2, default=str))
    
    # If we have tickets, get detailed view of first one
    if list_data.get('tickets'):
        first_ticket_id = list_data['tickets'][0]['ticketId']
        print(f"\n\nFetching detailed view of ticket {first_ticket_id}...")
        
        detail_url = f'https://demo.ticketing.api.rackspace.com/tickets/{first_ticket_id}'
        detail_response = client.get(detail_url, headers=headers)
        detail_response.raise_for_status()
        
        detail_data = detail_response.json()
        
        print('\n=== SINGLE TICKET RESPONSE ===')
        print(json.dumps(detail_data, indent=2, default=str))
    
    # Test search endpoint
    print("\n\nTesting search endpoints...")
    
    # Try different search patterns
    search_queries = [
        ('q', 'backup'),  # Common search parameter
        ('search', 'backup'),
        ('query', 'backup'),
        ('subject', 'backup'),
    ]
    
    for param_name, query in search_queries:
        try:
            print(f"\nTrying search with {param_name}={query}...")
            search_url = 'https://demo.ticketing.api.rackspace.com/tickets/search'
            search_response = client.get(
                search_url, 
                headers=headers, 
                params={param_name: query, 'limit': 2},
                timeout=30.0
            )
            if search_response.status_code == 200:
                print(f"SUCCESS! Search endpoint works with {param_name}")
                search_data = search_response.json()
                print('\n=== SEARCH RESPONSE ===')
                print(json.dumps(search_data, indent=2, default=str))
                break
            else:
                print(f"  Status {search_response.status_code}")
        except Exception as e:
            print(f"  Failed: {e}")
    
    # Also try search as part of regular tickets endpoint
    print("\n\nTrying search on main tickets endpoint...")
    try:
        filtered_response = client.get(
            'https://demo.ticketing.api.rackspace.com/tickets',
            headers=headers,
            params={'search': 'backup', 'limit': 2},
            timeout=30.0
        )
        if filtered_response.status_code == 200:
            print("Search on main endpoint successful!")
            filtered_data = filtered_response.json()
            print('\n=== FILTERED TICKETS RESPONSE ===')
            print(json.dumps(filtered_data, indent=2, default=str))
    except Exception as e:
        print(f"Failed: {e}")
    
    client.close()

if __name__ == '__main__':
    main()