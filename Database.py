import psycopg2   ##This is the library we will use to connect to our database 

def connection():
        con = psycopg2.connect(
            host="localhost",
            database="ecommerce",
            user ="postgres",
            password="1234",
            port =5432
        )

        if con :
                print("Connection to database successful")
        else:
                print("Connection to database failed")

        return con

conn = connection()
