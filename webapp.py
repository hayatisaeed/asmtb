from flask import Flask, request, render_template

app = Flask(__name__)


merchant = "4390ca27-e428-4c4a-b2e4-cfde882355ba"


def get_link_to_zp(amount, payment_id):
    link = f'http://103.75.197.206:5000/verify_payment?amount={amount}&paymentId={payment_id}&securityCode=1234'
    return link


def get_callback_link(amount, payment_id, security_code):
    return ""


def get_security_code(amount, payment_id):
    return "1234"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_payment', methods=['GET'])
def new_payment():
    amount = request.args.get('amount')
    payment_id = request.args.get('paymentId')
    link = get_link_to_zp(amount, payment_id)
    return render_template('new_payment.html', amount=amount, link=link, payment_id=payment_id)


@app.route('/verify_payment', methods=['GET'])
def verify_payment():
    amount = request.args.get('amount')
    payment_id = request.args.get('paymentId')
    expected_security_code = get_security_code(amount, payment_id)
    security_code = request.args.get('securityCode')

    if not str(security_code) == str(expected_security_code):
        message = "❌ پرداخت شما تایید نشد ❌"
    else:
        # ## {save payment stuff here} ## #
        message = "✅ پرداخت شما تایید شد، لطفا به بات برگشته و دکمه‌ی پرداخت کردم را بزنید."

    return render_template('verify_payment.html', message=message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
