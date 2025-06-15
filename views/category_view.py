from flask import render_template

def list(categories):
    return render_template('categories/index.html', categories =categories)

def create(form): #sending form for wtforms
    return render_template('categories/create.html', form=form)

def edit(form, category):
    return render_template('categories/edit.html', form=form, category=category)

#optional
def list_active(categories_active):
    return render_template('categories/page.html', categories_active =categories_active)
