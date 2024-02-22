from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data for dynamic form generation
data = {
    "subject1": {
        "under_subject1-1": ["m1", "m2", "m3"],
        "under_subject1-2": ["n1", "n2", "n3"]
    },
    "subject2": {
        "under_subject2-1": ["k1", "k2", "k3"],
        "under_subject2-2": ["p1", "p2", "p3"]
    }
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Store form data in session
        session['form_data'] = dict(request.form)
        return redirect(url_for('index'))  # Redirect to reload the page

    form_data = session.get('form_data', {})
    return render_template('dynamic_form.html', data=data, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
