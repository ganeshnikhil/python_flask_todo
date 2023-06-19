from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   if request.method=='POST':
      title = request.form['title']
      desc = request.form['desc']
      todo = Todo(title=title, desc=desc)
      db.session.add(todo)
      db.session.commit()
        
   allTodo = Todo.query.all() 
   return render_template('index.html', allTodo=allTodo)


@app.route('/base', methods=['GET', 'POST'])
def search():
   if request.method=='POST':
      search_query=request.form['search']
      allTodo = Todo.query.all()
      for todo in allTodo:
         if search_query==todo.title:
            return render_template('search.html',Sno=todo.sno,Title=todo.title,Desc=todo.desc,Date=todo.date_created)
            #return render_temf"{todo.sno}-{todo.title}-{todo.desc}-{todo.date_created}"
   return "<h1> Not found !.........................<h1>"+'<hr >'*100
   
   
@app.route('/show')
def products():
   alltodo=Todo.query.all()
   
   return 'This is true'


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
 
   
@app.route('/delete/<int:sno>')
def delete(sno):
   todo = Todo.query.filter_by(sno=sno).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect("/")

@app.route('/about')
def about():
   return render_template('about.html')
   


if __name__ == "__main__":
   with app.app_context():
      db.create_all()
   app.run(debug=True, port=8000)
