from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://jenniejing:99V15wIaMVxFunYL@cluster0.cghskf9.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('ticket_info')
ticket_info_collection = pymongo.collection.Collection(db, 'ticket_ino')

def insert_ticket_info(data):
    ticket_info_collection.insert_one(data)