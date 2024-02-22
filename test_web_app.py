from flask import Flask, render_template, request, redirect, url_for

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
            return render_template('new_report.html', fields=fields,
                                   num_additional_fields=num_additional_fields, form_data=request.form)
        elif 'submit' in request.form:
            # Process the form data here
            # Redirect or render success page
            pass

    return render_template('new_report.html', fields=fields,
                           num_additional_fields=num_additional_fields, form_data=request.form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
