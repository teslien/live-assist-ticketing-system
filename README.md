# Ticketing System

A Flask-based ticketing system with API endpoints for ticket creation and a web dashboard for ticket management.

## Features

- **API Endpoint**: POST `/create_ticket` for creating tickets via JSON
- **Real-time Updates**: WebSocket-powered live dashboard updates
- **Web Dashboard**: View all tickets in a responsive card layout
- **Ticket Management**: Update status, add descriptions, and comments
- **SQLite Database**: Simple file-based database storage
- **Responsive UI**: Bootstrap-powered interface with modern design
- **Live Notifications**: Instant notifications when tickets are created or updated

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Dashboard: http://localhost:5000/dashboard
   - API Endpoint: http://localhost:5000/create_ticket

## API Usage

### Create Ticket

**Endpoint**: `POST /create_ticket`

**Request Body**:
```json
{
  "user_id": "john_doe",
  "pdf_link": "https://example.com/product-guide.pdf",
  "product_id": "optional_product_id",
  "other_ids": "optional_other_ids"
}
```

**Response**:
```json
{
  "success": true,
  "ticket_id": 1,
  "message": "Ticket created successfully"
}
```

### Example using curl:
```bash
curl -X POST http://localhost:5000/create_ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_doe",
    "pdf_link": "https://example.com/guide.pdf",
    "product_id": "PROD123"
  }'
```

## Database Schema

The SQLite database contains a `tickets` table with the following structure:

| Column     | Type      | Description                    |
|------------|-----------|--------------------------------|
| id         | INTEGER   | Auto-incrementing primary key  |
| user_id    | TEXT      | Username or user identifier    |
| pdf_link   | TEXT      | URL to the product guide PDF   |
| product_id | TEXT      | Optional product identifier    |
| other_ids  | TEXT      | Optional additional identifiers|
| status     | TEXT      | Open, Pending, or Closed       |
| description| TEXT      | Ticket description/notes       |
| comments   | TEXT      | Additional comments            |
| created_at | TIMESTAMP | Ticket creation timestamp      |

## Workflow

1. **Mobile App** → Sends POST request to `/create_ticket`
2. **System** → Creates ticket with auto-incremented ID
3. **Admin/Expert** → Views tickets on `/dashboard`
4. **Admin/Expert** → Clicks on ticket to view/edit details
5. **Admin/Expert** → Updates description, adds comments, changes status
6. **System** → Tracks ticket lifecycle (Open → Pending → Closed)

## File Structure

```
ticketing-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── tickets.db            # SQLite database (auto-created)
└── templates/
    ├── base.html         # Base template with Bootstrap
    ├── dashboard.html    # Main dashboard view
    └── ticket_detail.html # Individual ticket view/edit
```

## Status Flow

- **Open**: New tickets (default status)
- **Pending**: Tickets being worked on
- **Closed**: Resolved tickets

Admins can change status through the dashboard or use quick action buttons.

## Real-time Features

The dashboard now includes WebSocket-powered real-time updates:

- **Instant Ticket Display**: New tickets appear immediately without page refresh
- **Live Status Updates**: Status changes are reflected across all connected clients
- **Desktop Notifications**: Visual notifications for new tickets and updates
- **Connection Status**: Shows connection status to the WebSocket server

### Testing Real-time Updates

1. **Start the application**: `python app.py`
2. **Open dashboard**: http://localhost:5000/dashboard in multiple browser tabs
3. **Use test script**: `python test_api.py` to create sample tickets
4. **Watch live updates**: Tickets will appear instantly on all open dashboard tabs

## Development

The application runs in debug mode by default. For production deployment:

1. Set `app.secret_key` to a secure random value
2. Set `debug=False` in `socketio.run()`
3. Use a production WSGI server compatible with WebSockets (like Gunicorn with eventlet)
4. Consider using a more robust database like PostgreSQL
5. Configure WebSocket CORS settings for production domains

## Security Notes

- Change the `app.secret_key` in production
- Add input validation and sanitization for production use
- Consider adding authentication for the dashboard
- Implement rate limiting for the API endpoint
- Configure WebSocket CORS properly for production
