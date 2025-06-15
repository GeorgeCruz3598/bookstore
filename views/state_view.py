from flask import render_template

def list(states):
    return render_template('states/index.html', states =states)

def create(form): #sending form for wtforms
    return render_template('states/create.html', form=form)

def edit(form, state):
    return render_template('states/edit.html', form=form, state=state)
