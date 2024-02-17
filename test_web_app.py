from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('new_report.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    return 'Got it! Data: {}'.format(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
