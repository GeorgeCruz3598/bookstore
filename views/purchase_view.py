from flask import render_template

def list(purchases):
    return render_template('purchases/index.html', purchases =purchases)

def create(form):
    return render_template('purchases/create.html', form=form)

def edit(form, purchase, book, provider):
    return render_template('purchases/edit.html', form=form, purchase=purchase, book=book, provider=provider)


