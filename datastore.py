import datetime
import logging
import spreadsheet
from google.cloud import datastore

datastore_client = datastore.Client()

def put_volunteers(volunteers):
    entity = datastore.Entity(key=datastore_client.key('volunteer'))
    for volunteer in volunteers:
        try:
            entity.update({
                'last_name': volunteer[1][0],
                'first_name': volunteer[1][1],
                'adress': volunteer[1][2],
                'email': volunteer[1][3],
                'id_tree': volunteer[1][4],
                'timestamp': datetime.datetime.now()
            })

            datastore_client.put(entity)
            spreadsheet.update_row(volunteer[0])
        except Exception as e:
            logging.warning("A Problem has occured")
            logging.exception(e)
            continue

def fetch_times(limit):
    query = datastore_client.query(kind='volunteer')
    query.order = ['-timestamp']

    requests = query.fetch(limit=limit)
    return requests