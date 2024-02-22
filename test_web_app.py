from flask import Flask, render_template, request

app = Flask(__name__)

# Sample data for dynamic form generation
fields = ['Name', 'Email', 'Phone']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the "Add Field" button is clicked
        if 'add_field' in request.form:
            # Add a new field to the list
            fields.append('New Field')
            # Redirect to the same route to render the updated form
            return render_template('new_report.html', fields=fields, form_data=request.form)

    return render_template('new_report.html', fields=fields)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
