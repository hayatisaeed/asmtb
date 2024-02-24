from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests
import json
import core.data_handler

app = Flask(__name__)

app.secret_key = """eo't!7£Az[95m`&5nz33S$y+kX^!xJqn"""
admin_username = '1234'
admin_password = '1234'


merchant = "4390ca27-e428-4c4a-b2e4-cfde882355ba"
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
call_back_template = "http://103.75.197.206:5000/verify_payment"
description = "شارژ کیف پول مشاوره تحصیلی"


def send_request(payment_id, amount):
    data = {
        "MerchantID": merchant,
        "Amount": amount,
        "Description": description,
        "CallbackURL": get_callback_link(payment_id, amount),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority, amount):
    data = {
        "MerchantID": merchant,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response


def get_link_to_zp(amount, payment_id):
    link = f'http://103.75.197.206:5000/verify_payment?amount={amount}&paymentId={payment_id}'
    return link


def get_callback_link(payment_id, amount):
    return call_back_template + "?paymentId=" + payment_id + "&amount=" + str(amount)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_payment', methods=['GET'])
def new_payment():
    amount = request.args.get('amount')
    payment_id = request.args.get('paymentId')
    req = send_request(payment_id, amount)
    if req['status']:
        link = req['url']
    else:
        link = "/someError"

    return render_template('new_payment.html', amount=amount, link=link, payment_id=payment_id)


@app.route('/someError', methods=['GET'])
def show_error():
    return render_template('error.html')


@app.route('/verify_payment', methods=['GET'])
def verify_payment():
    amount = request.args.get('amount')
    payment_id = request.args.get('paymentId')
    authority = request.args.get('authority')
    status = request.args.get('Status')

    if status != 'OK':
        verified = False
    else:
        core.data_handler.change_transaction_status(payment_id)
        verified = True
    # else:
    #     if verify(authority, amount).json()['status']:
    #         verified = True
    #     else:
    #         verified = False

    if not verified:
        return render_template('error.html')
    else:
        # ## {save payment stuff here} ## #
        message = "✅ پرداخت شما تایید شد، لطفا به بات برگشته و دکمه‌ی پرداخت کردم را بزنید."
        return render_template('verify_payment.html', message=message)


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


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'logged_in' in session:
        return redirect('/admin/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('admin_manage_subjects'))
        else:
            return render_template('admin_login_form.html', error='خطا در ورود')
    return render_template('admin_login_form.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_panel.html')


@app.route('/admin/manageSubjects')
def admin_manage_subjects():
    subjects = core.data_handler.get_subjects_dict()

    if 'logged_in' in session:
        return render_template('admin_manage_subjects.html', subjects=subjects)

    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/saveSubjects', methods=['POST'])
def admin_save_subjects():
    subjects = core.data_handler.get_subjects_dict()
    subjects = request.json['subjects']
    core.data_handler.save_subjects(subjects)
    return jsonify({"message": "Subjects saved successfully."})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
