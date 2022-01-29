import get_suit
import errors
from flask import Flask, render_template, request, url_for, flash, redirect
from webbrowser import open as wop
from shutil import rmtree
app = Flask(__name__)
app.secret_key = 'madeByYHanchao'


@app.route('/', methods=['POST', 'GET'])
def main_page():
    res = list()
    total_page = 0
    now_page = 0
    if request.method == 'GET':
        res, total_page, now_page, status = get_suit.get_all_suit(refresh=0,
                                                                  page=0)

    if request.method == 'POST':
        if ('refresh-click' in request.form.keys()):
            res, total_page, now_page, status = get_suit.get_all_suit(
                refresh=1, page=0)
        elif ('query-click' in request.form.keys()):
            res, total_page, now_page, status = get_suit.get_all_suit(
                query=request.form['query'], page=0)
        else:
            page = int(list(request.form.keys())[0])
            res, total_page, now_page, status = get_suit.get_all_suit(
                refresh=0, page=page)
    if status != 100 and status != 101:
        flash(errors.errors[status])
    return render_template('index.html',
                           content=res,
                           total_page=total_page,
                           now_page=now_page)


@app.route('/res/', methods=['POST', 'GET'])
def get_page():
    if request.method == 'POST':
        item_id = int(list(request.form.keys())[0])
        res, status = get_suit.get_suit(item_id)
        if (status == 100):
            name = res['data']['item']['name']
            flash("装扮：" + name + "(ID: {})".format(item_id) + "获取完成")
        elif (status == 101):
            name = res['data']['item']['name']
            flash("装扮：" + name + "(ID: {})".format(item_id) + "获取完成，但出现错误")
        else:
            flash(errors.errors[status])
        return redirect(url_for('main_page'))


@app.route('/about/')
def about_page():
    return render_template('about.html')


@app.route('/temp/')
def clear_temp():
    if get_suit.osPathExists('./static/temp/'):
        try:
            rmtree('./static/temp')
            flash("缓存已清空")
        except:
            flash(errors.errors[6])
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    wop("http://localhost:1418")
    app.run(port=1418, debug=False)
