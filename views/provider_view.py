from flask import render_template

def list(providers):
    return render_template('providers/index.html', providers =providers)

def create(form): #sending form for wtforms
    return render_template('providers/create.html', form=form)

def edit(form, provider):
    return render_template('providers/edit.html', form=form, provider=provider)

#optional
def list_active(providers_active):
    return render_template('providers/page.html', providers_active =providers_active)
