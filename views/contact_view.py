from flask import render_template

def list(contacts):
    return render_template('contacts/index.html', contacts =contacts)

def create(form): #sending form for wtforms
    return render_template('contacts/create.html', form=form)

def edit(form, contact):
    return render_template('contacts/edit.html', form=form, contact=contact)
