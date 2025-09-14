from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
socketio = SocketIO(app, cors_allowed_origins="*")

# Database initialization
def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            pdf_link TEXT NOT NULL,
            product_id TEXT,
            other_ids TEXT,
            status TEXT DEFAULT 'Open',
            description TEXT DEFAULT '',
            comments TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# API Endpoint - Create Ticket
@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'pdf_link' not in data:
            return jsonify({'error': 'user_id and pdf_link are required'}), 400
        
        user_id = data['user_id']
        pdf_link = data['pdf_link']
        product_id = data.get('product_id', '')
        other_ids = data.get('other_ids', '')
        
        # Insert into database
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (user_id, pdf_link, product_id, other_ids)
            VALUES (?, ?, ?, ?)
        ''', (user_id, pdf_link, product_id, other_ids))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        
        # Get the created ticket for real-time broadcast
        cursor.execute('''
            SELECT id, user_id, pdf_link, product_id, other_ids, status, description, comments, created_at
            FROM tickets WHERE id = ?
        ''', (ticket_id,))
        ticket = cursor.fetchone()
        conn.close()
        
        # Prepare ticket data for broadcasting
        ticket_data = {
            'id': ticket[0],
            'user_id': ticket[1],
            'pdf_link': ticket[2],
            'product_id': ticket[3],
            'other_ids': ticket[4],
            'status': ticket[5],
            'description': ticket[6],
            'comments': ticket[7],
            'created_at': ticket[8]
        }
        
        # Broadcast new ticket to all connected clients
        socketio.emit('new_ticket', ticket_data)
        
        return jsonify({
            'success': True,
            'ticket_id': ticket_id,
            'message': 'Ticket created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard - View all tickets
@app.route('/')
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, pdf_link, product_id, status, description, comments, created_at
        FROM tickets
        ORDER BY created_at DESC
    ''')
    tickets = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries for easier template usage
    ticket_list = []
    for ticket in tickets:
        ticket_list.append({
            'id': ticket[0],
            'user_id': ticket[1],
            'pdf_link': ticket[2],
            'product_id': ticket[3],
            'status': ticket[4],
            'description': ticket[5],
            'comments': ticket[6],
            'created_at': ticket[7]
        })
    
    return render_template('dashboard.html', tickets=ticket_list)

# Individual ticket view/edit
@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, pdf_link, product_id, other_ids, status, description, comments, created_at
        FROM tickets WHERE id = ?
    ''', (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect(url_for('dashboard'))
    
    ticket_data = {
        'id': ticket[0],
        'user_id': ticket[1],
        'pdf_link': ticket[2],
        'product_id': ticket[3],
        'other_ids': ticket[4],
        'status': ticket[5],
        'description': ticket[6],
        'comments': ticket[7],
        'created_at': ticket[8]
    }
    
    return render_template('ticket_detail.html', ticket=ticket_data)

# Update ticket
@app.route('/ticket/<int:ticket_id>/update', methods=['POST'])
def update_ticket(ticket_id):
    try:
        description = request.form.get('description', '')
        comments = request.form.get('comments', '')
        status = request.form.get('status', 'Open')
        
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tickets 
            SET description = ?, comments = ?, status = ?
            WHERE id = ?
        ''', (description, comments, status, ticket_id))
        conn.commit()
        
        # Get updated ticket for broadcasting
        cursor.execute('''
            SELECT id, user_id, pdf_link, product_id, other_ids, status, description, comments, created_at
            FROM tickets WHERE id = ?
        ''', (ticket_id,))
        ticket = cursor.fetchone()
        conn.close()
        
        if ticket:
            ticket_data = {
                'id': ticket[0],
                'user_id': ticket[1],
                'pdf_link': ticket[2],
                'product_id': ticket[3],
                'other_ids': ticket[4],
                'status': ticket[5],
                'description': ticket[6],
                'comments': ticket[7],
                'created_at': ticket[8]
            }
            # Broadcast ticket update to all connected clients
            socketio.emit('ticket_updated', ticket_data)
        
        flash('Ticket updated successfully', 'success')
        return redirect(url_for('view_ticket', ticket_id=ticket_id))
        
    except Exception as e:
        flash(f'Error updating ticket: {str(e)}', 'error')
        return redirect(url_for('view_ticket', ticket_id=ticket_id))

# Update ticket status (quick action)
@app.route('/ticket/<int:ticket_id>/status/<status>')
def update_status(ticket_id, status):
    valid_statuses = ['Open', 'Pending', 'Closed']
    if status not in valid_statuses:
        flash('Invalid status', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tickets SET status = ? WHERE id = ?', (status, ticket_id))
        conn.commit()
        
        # Get updated ticket for broadcasting
        cursor.execute('''
            SELECT id, user_id, pdf_link, product_id, other_ids, status, description, comments, created_at
            FROM tickets WHERE id = ?
        ''', (ticket_id,))
        ticket = cursor.fetchone()
        conn.close()
        
        if ticket:
            ticket_data = {
                'id': ticket[0],
                'user_id': ticket[1],
                'pdf_link': ticket[2],
                'product_id': ticket[3],
                'other_ids': ticket[4],
                'status': ticket[5],
                'description': ticket[6],
                'comments': ticket[7],
                'created_at': ticket[8]
            }
            # Broadcast ticket update to all connected clients
            socketio.emit('ticket_updated', ticket_data)
        
        flash(f'Ticket status updated to {status}', 'success')
        
    except Exception as e:
        flash(f'Error updating status: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to ticket system'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
