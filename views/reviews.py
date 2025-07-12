from flask import request
from flask_restx import Resource, Namespace
from models import Review
from setup_db import db
review_ns = Namespace('reviews')

@review_ns.route('/')
class ReviewsView(Resource):
    def get(self):
        Rs = Review.query.all()
        res = []
        for r in Rs:
            sm_d = r.__dict__
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        req_json = request.json
        ent = Review(**req_json)
        db.session.add(ent)
        db.session.commit()
        return "", 201


@review_ns.route('/<int:bid>')
class ReviewView(Resource):
    def get(self, bid):
        r = Review.query.get(bid)
        sm_d = r.__dict__
        del sm_d['_sa_instance_state']
        return sm_d, 200

    def put(self, bid):
        review = Review.query.get(bid)
        req_json = request.json
        review.user = req_json.get("user")
        review.rating = req_json.get("rating")
        review.book_id = req_json.get("book_id")
        db.session.add(review)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        review = Review.query.get(bid)

        db.session.delete(review)
        db.session.commit()
        return "", 204