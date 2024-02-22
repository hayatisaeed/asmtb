# test-web-app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample dictionary of subjects and under-subjects
subjects = {
    "sub1": {"under_sub1-1": ["under_under_sub1-1-1", "under_under_sub1-1-2"], "under_sub1-2": ["under_under_sub1-2-1", "under_under_sub1-2-2"]},
    "sub2": {"under_sub2-1": ["under_under_sub2-1-1", "under_under_sub2-1-2"], "under_sub2-2": ["under_under_sub2-2-1", "under_under_sub2-2-2"]}
}


@app.route('/showReportForm')
def index():
    return render_template('dynamic_form.html', subjects=subjects, user_name="Saeed", user_id="1234")


@app.route('/saveNewReport', methods=['POST'])
def report():
    data = request.form
    print(data)
    for i in data:
        print(i, data[i])
    return render_template('saveNewReport.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
