"""Contact resources for GoHighLevel MCP integration"""

# Import the mcp instance and ghl_client from main
# This will be set during import in main.py
mcp = None
ghl_client = None


def _register_contact_resources(_mcp, _ghl_client):
    """Register contact resources with the MCP instance"""
    global mcp, ghl_client
    mcp = _mcp
    ghl_client = _ghl_client

    @mcp.resource("contacts://{location_id}")
    async def list_contacts_resource(location_id: str) -> str:
        """List all contacts for a location as a resource"""
        if ghl_client is None:
            raise RuntimeError(
                "MCP server not properly initialized. Please restart the server."
            )
        result = await ghl_client.get_contacts(location_id=location_id, limit=100)

        # Format contacts as readable text
        lines = [f"# Contacts for Location {location_id}\n"]
        lines.append(f"Total contacts: {result.total or result.count}\n")

        for contact in result.contacts:
            name = (
                contact.name
                or f"{contact.firstName or ''} {contact.lastName or ''}".strip()
                or "Unknown"
            )
            lines.append(f"\n## {name}")
            lines.append(f"- ID: {contact.id}")
            lines.append(f"- Email: {contact.email or 'N/A'}")
            lines.append(f"- Phone: {contact.phone or 'N/A'}")
            if contact.tags:
                lines.append(f"- Tags: {', '.join(contact.tags)}")
            lines.append(f"- Date Added: {contact.dateAdded}")

        return "\n".join(lines)

    @mcp.resource("contact://{location_id}/{contact_id}")
    async def get_contact_resource(location_id: str, contact_id: str) -> str:
        """Get a single contact as a resource"""
        if ghl_client is None:
            raise RuntimeError(
                "MCP server not properly initialized. Please restart the server."
            )
        contact = await ghl_client.get_contact(contact_id, location_id)

        # Format contact as readable text
        name = (
            contact.name
            or f"{contact.firstName or ''} {contact.lastName or ''}".strip()
            or "Unknown"
        )
        lines = [f"# Contact: {name}\n"]
        lines.append(f"- ID: {contact.id}")
        lines.append(f"- Location: {contact.locationId}")
        lines.append(f"- Email: {contact.email or 'N/A'}")
        lines.append(f"- Phone: {contact.phone or 'N/A'}")
        if contact.tags:
            lines.append(f"- Tags: {', '.join(contact.tags)}")
        if contact.source:
            lines.append(f"- Source: {contact.source}")
        if contact.companyName:
            lines.append(f"- Company: {contact.companyName}")
        if contact.address1:
            lines.append(f"- Address: {contact.address1}")
            if contact.city:
                lines.append(f"- City: {contact.city}")
            if contact.state:
                lines.append(f"- State: {contact.state}")
            if contact.postalCode:
                lines.append(f"- Postal Code: {contact.postalCode}")
        lines.append(f"- Date Added: {contact.dateAdded}")
        lines.append(f"- Last Updated: {contact.dateUpdated}")

        return "\n".join(lines)
