from datetime import datetime, timedelta
from pymongo import MongoClient
from utils import *
from settings import USERNAME, PASSWORD

days_back = -0.5
range = 2.2
start_date = datetime(2020, 2, 3, 15)
search = 0


class DbWrapper:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://{}:{}@cluster0.0e5pv.mongodb.net/air?retryWrites=true&w=majority'.format(USERNAME, PASSWORD))
        self.db = self.client.air

    def get_data(self, limit=None, minute=False):
        if minute:
            if search:
                start_dt = start_date
                end_dt = start_date + timedelta(days=range)
                cursor = self.db.air_minute.find({'at': {'$gte': start_dt, '$lte': end_dt}}).sort([('_id', -1)])
            else:
                day_ago = datetime.now(timezone.utc) + timedelta(days=days_back)
                cursor = self.db.air_minute.find({'at': {'$gte': day_ago}}).sort([('_id', -1)])
        else:
            if limit:
                cursor = self.db.air.find().sort([('_id', -1)]).limit(limit)
            else:
                cursor = self.db.air.find().sort([('_id', -1)])

        if not cursor:
            print('cursor empty! in get_data')
            cursor = []
        # print(cursor)
        return list(cursor)

    def is_online(self):
        cursor = list(self.db.air.find().sort([('_id', -1)]).limit(1))
        if not cursor:
            print('cursor empty! in is_online')
            return False

        now = datetime.now(timezone.utc)
        dt = utc_to_local(cursor[-1]['at'])

        diff = now - dt
        if diff > timedelta(minutes=5):
            return False

        return True

    def clear_db(self):
        # day_ago = datetime.now(timezone.utc) + timedelta(days=-10)
        # self.db.air.remove({'at': {'$lte': day_ago}})
        self.db.air.remove()
        print('done')
