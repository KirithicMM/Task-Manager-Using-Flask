from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        category = request.form.get('category')
        completed = 'completed' in request.form


        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            category=category,
            completed=completed
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!')
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.category = request.form.get('category')
        task.completed = 'completed' in request.form


        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('index'))

    return render_template('add.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
