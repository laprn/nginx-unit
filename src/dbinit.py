from wsgi import db

# DB initiate. Once you initiate the db, then run patch.py to add images contained in `uploads` directory to db.
if __name__=='__main__':
    db.create_all()