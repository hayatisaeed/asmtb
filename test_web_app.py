# test-web-app.py
from flask import Flask, render_template, request, redirect, url_for
import core.data_handler

app = Flask(__name__)

# Sample dictionary of subjects and under-subjects
subjects = {
    "sub1": {"under_sub1-1": ["under_under_sub1-1-1", "under_under_sub1-1-2"], "under_sub1-2": ["under_under_sub1-2-1", "under_under_sub1-2-2"]},
    "sub2": {"under_sub2-1": ["under_under_sub2-1-1", "under_under_sub2-1-2"], "under_sub2-2": ["under_under_sub2-2-1", "under_under_sub2-2-2"]}
}


@app.route('/showReportForm')
def show_report_form():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    subjects = core.data_handler.get_subjects_dict()
    return render_template('dynamic_form.html', subjects=subjects, user_name=user_name,
                           user_id=user_id)


@app.route('/saveNewReport', methods=['POST'])
def save_new_report():
    form_data = request.form
    data = {}
    for i in form_data:
        data[i] = form_data[i]

    usable_data = {}
    for i in data:
        row = int(i.split('[')[1].replace(']', '')) + 1
        title = i.split('[')[0]
        if row not in usable_data:
            usable_data[row] = {}

        usable_data[row][title] = data[i]

    print(usable_data)
    return render_template('saveNewReport.html', data=usable_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
