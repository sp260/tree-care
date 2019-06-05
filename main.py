import datetime
import datastore
import spreadsheet
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/list')
def list_requests():
    requests = datastore.fetch_times(100)
    return render_template('list.html', data=requests)

@app.route('/update')
def add_volunteers():
    volunteers = spreadsheet.get_volunteers()
    datastore.put_volunteers(volunteers)
    return 'Le datastore a été mis à jour avec succès.'

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        infos = {
            'last_name': request.form['last_name'],
            'first_name': request.form['first_name'],
            'adress': request.form['adress'],
            'email': request.form['email'],
            'id_tree': request.form['id_tree']
        }
        spreadsheet.insert_row(infos)
        return render_template('validation.html', data=infos)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

#http://canopy.org/tree-info/caring-for-trees/young-trees/
