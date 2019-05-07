from flask import Flask, render_template, request, redirect
from redisearch import AutoCompleter, Suggestion, Client, TextField, Query
import json
import redis
import csv

app = Flask(__name__)

def load_data():
    ac = AutoCompleter('ac')

    client.create_index([
        TextField('Rank'),
        TextField('Title'),
        TextField('Website'),
        TextField('Employees'),
        TextField('Sector'),
        TextField('Industry'),
        TextField('Hqlocation'),
        TextField('Hqaddr'),
        TextField('Hqcity'),
        TextField('Hqstate'),
        TextField('Hqzip'),
        TextField('Hqtel'),
        TextField('Ceo'),
        TextField('Ceotitle'),
        TextField('Address'),
        TextField('Ticker'),
        TextField('Fullname'),
        TextField('Revenues'),
        TextField('Revchange'),
        TextField('Profits'),
        TextField('Prftchange'),
        TextField('Assets'),
        TextField('Totshequity')
        ])

    with open('./fortune500.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                ac.add_suggestions(Suggestion(row[1].replace('"', ''), payload=row[0]))
                client.add_document(row[1],
                                    Rank=row[0],
                                    Title=row[1],
                                    Website=row[2],
                                    Employees=row[3],
                                    Sector=row[4],
                                    Industry=row[5],
                                    Hqlocation=row[6],
                                    Hqaddr=row[7],
                                    Hqcity=row[8],
                                    Hqstate=row[9],
                                    Hqzip=row[10],
                                    Hqtel=row[11],
                                    Ceo=row[12],
                                    Ceotitle=row[13],
                                    Address=row[14],
                                    Ticker=row[15],
                                    Fullname=row[16],
                                    Revenues=row[17],
                                    Revchange=row[18],
                                    Profits=row[19],
                                    Prftchange=row[20],
                                    Assets=row[21],
                                    Totshequity=row[22])
            line_count += 1




client = Client('Fortune500',
                host='localhost',
                port=6379)

@app.route('/')
def hello_world():
   r = redis.Redis()
   if len(r.keys('ac')) < 1:
       load_data()
   return render_template('search.html')

@app.route('/autocomplete')
def auto_complete():
    ac = AutoCompleter('ac')
    name = request.args.get('term')
    suggest = ac.get_suggestions(name, fuzzy=True, with_payloads=True, with_scores=True)
    return(json.dumps([
        {'value': item.string, 'label': item.string, 'id': item.payload, 'score': item.score}
        for item in suggest]))

@app.route('/rank/<int:rank_id>')
def show_rank(rank_id):
    thecompany = client.search(Query(rank_id).limit_fields('Rank'))
    return render_template('company.html', company=thecompany.docs)

if __name__ == '__main__':
   app.run()
