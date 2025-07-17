from flask import request
from flask_restx import Namespace, Resource
from models import Book
from setup_db import db

book_ns = Namespace('books')

@book_ns.route("")
class BooksVieq(Resource):
    def get(self):
        books = Book.query.all()
        res = []
        for book in books:
            sm_d = book.__dict__
            del sm_d['_sa_instance_state']
            res.append(book.__dict__)
        return res, 200

    def post(self):
        data = request.json
        new_book = Book(**data)
        with db.session.begin():
            db.session.add(new_book)
        return "", 201

@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        book = Book.query.get(bid)
        result = book.__dict__
        del result['_sa_instance_state']
        return result, 200

    def put(self, bid):
        book = Book.query.get(bid)
        req_json = request.json
        book.name = req_json.get('name')
        book.author = req_json.get("author")
        book.year = req_json.get("year")
        book.pages = req_json.get("pages")
        db.session.add(book)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        book = Book.query.get(bid)
        with db.session.begin():
            db.session.delete(book)
        return "", 204
