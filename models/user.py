import sqlite3
class UserModel():
    def __init__(self, id, username, password):
        self.id = id
        self.username  = username
        self.password = password

    @classmethod
    def findByUsername(cls,username):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from users where username = ?',[username])
        res = query.fetchone()
        cur.close()
        if res:
             user = cls(*res)
        else:
            user = None

        # * res will take all the returned columns like we can also use res[0],res[1],res[2]
        return user
    @classmethod
    def findById(cls,id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from users where id = ?',[id])
        res = query.fetchone()
        cur.close()
        if res:
             user = cls(*res)
        else:
            user = None
        # * res will take all the returned columns like we can also use res[0],res[1],res[2]
        return user
