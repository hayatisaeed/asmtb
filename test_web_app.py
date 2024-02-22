from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Sample data for dynamic form generation
fields = ['Name', 'Email', 'Phone']


@app.route('/', methods=['GET', 'POST'])
def index():
    num_additional_fields = int(request.form.get('num_additional_fields', 0))
    if request.method == 'POST':
        if 'add_field' in request.form:
            # Increment the number of additional fields
            num_additional_fields += 1
            return render_template('dynamic_form.html', fields=fields,
                                   num_additional_fields=num_additional_fields, form_data=request.form)
        else:
            # Process the form data here
            form_data = {}
            for field in fields:
                form_data[field.lower()] = request.form.get(field.lower())
            for i in range(num_additional_fields):
                new_field_name = f'new_field_{i + 1}'
                form_data[new_field_name] = request.form.get(new_field_name, '')
            # Redirect to a new route to display the submitted data
            return redirect(url_for('display_data', **form_data))

    return render_template('dynamic_form.html',
                           fields=fields, num_additional_fields=num_additional_fields)


@app.route('/display_data')
def display_data():
    # Get the submitted form data from the URL parameters
    form_data = request.args.to_dict()
    return render_template('display_data.html', form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
