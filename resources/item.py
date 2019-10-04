import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Resource,reqparse, Api
from security import authenticate,identity
from flask_jwt import JWT, jwt_required, current_identity
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = float,required= True, help ="the field cannot be left blank" )
    # here name of item will be given in the url similarly for post

    # @jwt_required()
    def get(self, name):
        res = ItemModel.findByName(name)
        if res:
            return res.json(),200
        else:
            return {"item":"item not found"},404

    def post(self, name):
        res = ItemModel.findByName(name)
        print(res)
        if res:
            return {"message":"bad request item already present"},400
        args = Item.parser.parse_args()
        item = ItemModel(name,args['price'])
        try:
            item.insert()
        except:
            return {"message":"An error occured while inserting the item"},500 #internal server error
        return {'name':name,'price':args['price']},201

    def delete(self, name):
        res = ItemModel.findByName(name)
        if res:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('delete from items where name = ?',(name,))
            conn.commit()
            cur.close()
            return {'message':'item has been deleted'},201
        return {'message':'you entered incorrect name or Item not found'},400


# no matter how many times you call put function the output never changes
    def put(self,name):
        res = ItemModel.findByName(name)
        args = Item.parser.parse_args()
        if res:
            item = ItemModel(name,args['price'])
            item.update()
            return {"message":"item updated"},201
        #insert
        try:
            item = ItemModel(name,args['price'])
            item.insert()
        except:
            return {"message": "An error occured while inserting"},500
        return {"message":"item updated"},201

class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items')
        items = query.fetchall()
        cur.close()
        itemsList = []
        if items:
            for item in items:
                itemsList.append({"name":item[1],"price":item[2]})
            return {"items":itemsList}
        return {"message":"database is empty"}
