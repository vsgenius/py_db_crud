import psycopg2


class Crud:
    def __init__(self, database, user, password):
        self.connect = psycopg2.connect(database=database, user=user, password=password)
        with self.connect as con:
            with con.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    lastname VARCHAR(40) NOT NULL,
                    email VARCHAR(40) NOT NULL
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS phone(
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(40) NOT NULL,
                    client_id INTEGER NOT NULL REFERENCES client(id) on delete cascade
                );
                """)
                con.commit()

    def add_new_client(self, name, lastname, email, phone=None):
        with self.connect as con:
            with con.cursor() as cur:
                if phone is not None:
                    cur.execute("""
                    INSERT INTO client(name,lastname,email) VALUES(%s, %s, %s) returning id;
                        """, (name, lastname, email))
                    cur.execute("""
                    INSERT INTO phone(phone,client_id) VALUES(%s,%s);
                    """, (phone, cur.fetchone()[0]))
                    con.commit()
                else:
                    cur.execute("""
                        INSERT INTO client(name,lastname,email) VALUES(%s, %s, %s);
                        """, (name, lastname, email))
                    con.commit()

    def add_phone(self, client_id, phone):
        with self.connect as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT id FROM client WHERE id=%s;
                """, (client_id,))
                find_id = cur.fetchone()
                if find_id is not None:
                    cur.execute("""
                    INSERT INTO phone(phone,client_id) VALUES(%s,%s);
                    """, (phone, client_id))
                    con.commit()
                else:
                    print('клиента с таким ID нет')

    def update_data_client(self, id, name, lastname, email):
        with self.connect as con:
            with con.cursor() as cur:
                cur.execute("""
                    UPDATE client SET name=%s, lastname=%s, email=%s WHERE id=%s;
                    """, (name, lastname, email, id))
                con.commit()

    def del_phone(self, id):
        with self.connect as con:
            with con.cursor() as cur:
                cur.execute("""
                        DELETE FROM phone WHERE id=%s;
                        """, (id,))
                con.commit()

    def del_client(self, id):
        with self.connect as con:
            with con.cursor() as cur:
                cur.execute("""
                        DELETE FROM client WHERE id=%s;
                        """, (id,))
                con.commit()

    def find_client(self, name=None, lastname=None, email=None, phone=None):
        with self.connect as con:
            with con.cursor() as cur:
                if phone is None:
                    cur.execute("""
                    SELECT name,lastname FROM client WHERE name=%s or lastname=%s or email=%s;
                    """, (name, lastname, email))
                    return cur.fetchall()
                else:
                    cur.execute("""
                    select name,lastname from client where id=(SELECT id FROM phone WHERE phone=%s) 
                    or name=%s or lastname=%s or email=%s;
                    """, (phone, name, lastname, email))
                    return cur.fetchall()

