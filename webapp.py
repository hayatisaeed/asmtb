from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)


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
    link = f'http://103.75.197.206:5000/verify_payment?amount={amount}&paymentId={payment_id}&securityCode=1234'
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
        if verify(authority, amount).json()['status']:
            verified = True
        else:
            verified = False

    if not verified:
        return render_template('error.html')
    else:
        # ## {save payment stuff here} ## #
        message = "✅ پرداخت شما تایید شد، لطفا به بات برگشته و دکمه‌ی پرداخت کردم را بزنید."
        return render_template('verify_payment.html', message=message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
