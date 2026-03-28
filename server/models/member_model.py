from infrastructure.connection import get_connection

class MemberModel:
    @staticmethod
    def get_member_by_email(email):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM member WHERE email=%s",[email])
                    return cursor.fetchone()
        except Exception as e:
            print(e)
    @staticmethod
    def increase_member(email, password):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("INSERT INTO member(email,password) VALUES(%s,%s)",[email, password])
                    con.commit()
            return True
        except Exception as e:
            print(e)
