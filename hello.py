from flask import Flask, request, abort, render_template, redirect
import tasks
import redis

app = Flask(__name__)

# REDIS CONFIGS:
host = "127.0.0.1"
port = "6379"
db = 2
rdb = redis.StrictRedis(host=host, port=port, db=db)


@app.route("/")
def initialize():
    return render_template('form.html')


def result(result):
    return render_template('result.html', result=result)


@app.route("/calculate", methods=['POST'])
def calculate():
    tasks.download_html.delay('http://www.subinsapkota.com')
    number = request.form['link']
    if is_int(number):
        if int(number) < 0:
            abort(418)
        if is_in_redis(number):
            return result(float(rdb.get(number)))
        else:
            r = tasks.calculate.delay(int(number))
            squareroot = r.get()
            rdb.set(number, str(squareroot))
        return result(squareroot)
    else:
        abort(418)


if __name__ == '__main__':
    app.run()
