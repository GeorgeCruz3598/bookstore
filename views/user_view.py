from flask import render_template

def list(users):
    return render_template('users/index.html', users =users)

def create(form): #sending form for wtforms
    return render_template('users/create.html', form=form)

def edit(form, user):
    return render_template('users/edit.html', form=form, user=user)

def signup(form): #sending form for wtforms
    return render_template('users/signup.html', form=form)

def login(form):
    return render_template('users/login.html', form = form)
#it could be necessary to add customized-list showing methods