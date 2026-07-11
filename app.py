from flask import Flask, render_template, request, redirect, session
from models import db, Task, User

app = Flask(__name__)
app.secret_key = "taskmanager123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    description = request.form['description']

    new_task = Task(
        title=title,
        description=description,
        user_id=session['user_id']
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect('/')
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', task=task)
@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    task.status = "Completed"
    db.session.commit()
    return redirect('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect('/')

        return "Invalid Username or Password"

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)