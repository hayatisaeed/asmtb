from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new_report.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {}
    for key, value in request.form.items():
        data.setdefault(key, []).append(value)
    return 'Got it! Data: {}'.format(data)

if __name__ == '__main__':
    app.run(debug=True)
