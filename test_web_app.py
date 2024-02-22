# test-web-app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample dictionary of subjects and under-subjects
subjects = {
    "sub1": {"under_sub1-1": ["under_under_sub1-1-1", "under_under_sub1-1-2"], "under_sub1-2": ["under_under_sub1-2-1", "under_under_sub1-2-2"]},
    "sub2": {"under_sub2-1": ["under_under_sub2-1-1", "under_under_sub2-1-2"], "under_sub2-2": ["under_under_sub2-2-1", "under_under_sub2-2-2"]}
}


@app.route('/showForm')
def index():
    return render_template('dynamic_form.html', subjects=subjects)


@app.route('/report', methods=['POST'])
def report():
    data = request.form.to_dict()
    return render_template('report.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
