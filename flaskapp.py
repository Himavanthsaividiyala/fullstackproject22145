import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, jsonify

# --- App Configuration ---
DATABASE = 'expenses.db'
app = Flask(__name__)
app.config.from_object(__name__)

# --- Database Setup ---

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database; creates the table."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Routes ---

@app.route('/')
def index():
    """Main page: displays expenses and the form to add new ones."""
    db = get_db()
    cur = db.execute('SELECT id, description, category, amount, date, payment_method FROM expenses ORDER BY date DESC, id DESC')
    expenses = cur.fetchall()

    total_cur = db.execute('SELECT SUM(amount) as total FROM expenses')
    total_result = total_cur.fetchone()
    total_expenses = total_result['total'] if total_result['total'] else 0.0

    return render_template('index.html', expenses=expenses, total_expenses=total_expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    """Handles adding a new expense."""
    db = get_db()
    db.execute('INSERT INTO expenses (description, category, amount, date, payment_method) VALUES (?, ?, ?, ?, ?)',
               [request.form['description'], request.form['category'], request.form['amount'], request.form['date'], request.form['payment_method']])
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Handles deletion of an expense."""
    db = get_db()
    db.execute('DELETE FROM expenses WHERE id = ?', [expense_id])
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    """Handles editing an existing expense."""
    db = get_db()
    db.execute('UPDATE expenses SET description = ?, category = ?, amount = ?, date = ?, payment_method = ? WHERE id = ?',
               [request.form['description'], request.form['category'], request.form['amount'], request.form['date'], request.form['payment_method'], expense_id])
    db.commit()
    return redirect(url_for('index'))

@app.route('/expense/<int:expense_id>')
def get_expense(expense_id):
    """API endpoint to get a single expense's data for editing."""
    db = get_db()
    cur = db.execute('SELECT * FROM expenses WHERE id = ?', [expense_id])
    expense = cur.fetchone()
    if expense:
        # Convert the sqlite3.Row object to a dictionary to be easily converted to JSON
        return jsonify(dict(expense))
    return jsonify({'error': 'Expense not found'}), 404

# --- Main Execution ---

if __name__ == '__main__':
    # Initialize the database if it doesn't exist upon first run
    try:
        with open(DATABASE) as f: pass
    except IOError:
        print("Database not found. Initializing...")
        init_db()
        print("Database initialized.")

    app.run(debug=True)