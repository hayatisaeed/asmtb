# test-web-app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample dictionary of subjects and under-subjects
subjects = {
    "sub1": {"under_sub1-1": ["under_under_sub1-1-1", "under_under_sub1-1-2"], "under_sub1-2": ["under_under_sub1-2-1", "under_under_sub1-2-2"]},
    "sub2": {"under_sub2-1": ["under_under_sub2-1-1", "under_under_sub2-1-2"], "under_sub2-2": ["under_under_sub2-2-1", "under_under_sub2-2-2"]}
}


@app.route('/showReportForm')
def show_report_form():
    return render_template('dynamic_form.html', subjects=subjects, user_name="Saeed", user_id="1234")


@app.route('/saveNewReport', methods=['POST'])
def save_new_report():
    form_data = request.form
    data = {}
    for i in form_data:
        data[i] = form_data[i]

    print(data)
    return render_template('saveNewReport.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
