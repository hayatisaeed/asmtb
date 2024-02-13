from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_payment', methods=['GET'])
def new_payment():
    pass


@app.route('/verify', methods=['GET'])
def verify_payment():
    payment_id = request.args.get('payment_id')
    security_code = request.args.get('security_code')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
