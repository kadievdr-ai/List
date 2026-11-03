import json
from flask import Flask,render_template,request,redirect,url_for
import os


app = Flask(__name__)
tasks_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(tasks_FILE):
        return []
    with open(tasks_FILE,"r", encoding="utf-8") as file:
        tasks = json.load(file)
    return tasks

def save_tasks(tasks):
    with open(tasks_FILE,"w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html",tasks = tasks)

@app.route("/add",methods = ["POST"])
def add_task():
    task_text = request.form.get("task")
    if task_text:
        tasks = load_tasks()
        tasks.append(task_text)
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_index>",methods = ["POST"])
def delete_task(task_index):
    tasks = load_tasks()
    if 0<=task_index<len(tasks):
        
        tasks.pop(task_index)
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_index>",methods = ["POST"])
def edit_task(task_index):
    tasks = load_tasks()
    if 0<=task_index<len(tasks):
        new_text= request.form.get("task")
        if new_text:
            tasks[task_index] = new_text
            save_tasks(tasks)
    return redirect(url_for("index"))

 
if __name__ == "__main__":
    app.run(debug=True)