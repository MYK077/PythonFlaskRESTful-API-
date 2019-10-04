import sqlite3

class ItemModel:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def json(self):
        return {"name":self.name,"price":self.price}

    # find if name already exists
    @classmethod
    def findByName(cls,name):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        cur.close()
        if res:
            return cls(res[1],res[2])
    # insert into items TABLE
    def insert(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('insert into items (name, price) values(?, ?)',(self.name,self.price))
        conn.commit()
        cur.close()
        return {"message":"item updated"},201

    def update(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('update items SET price = ? WHERE name = ?',(self.price,self.name));
        conn.commit()
        cur.close()
