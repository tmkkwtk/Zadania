import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def add_shop(conn, shop):
    """
    Add a new shop into the shops table
    :param conn:
    :param shop:
    :return: shop id
    """
    sql = """INSERT INTO shops(name, type, size)
             VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, shop)
    conn.commit()
    return cur.lastrowid


def add_product(conn, product):
    """
    Add a new product into the products table
    :param conn:
    :param product:
    :return: product id
    """
    sql = """INSERT INTO products(shop_id, name, description)
             VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    return cur.lastrowid


def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


def update(conn, table, id, **kwargs):
    """
    update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f""" UPDATE {table}
             SET {parameters}
             WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)


def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f"DELETE FROM {table} WHERE {q}"
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f"DELETE FROM {table}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")


if __name__ == "__main__":
    db_file = "shopping.db"

    create_shops_sql = """
        -- shops table
        CREATE TABLE IF NOT EXISTS shops (
        id integer PRIMARY KEY,
        name text NOT NULL,
        type text,
        size real
    );
    """

    create_products_sql = """
    -- products table
    CREATE TABLE IF NOT EXISTS products (
        id integer PRIMARY KEY,
        shop_id integer NOT NULL,
        name VARCHAR(250) NOT NULL,
        description TEXT,
        FOREIGN KEY (shop_id) REFERENCES shops (id)
    );
    """
    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_shops_sql)
        execute_sql(conn, create_products_sql)

    shop = ("Biedronka", "Supermarket", 1000)

    sh_id = add_shop(conn, shop)

    product = (sh_id, "Cytryna", "Warzywo")

    pr_id = add_product(conn, product)

    print(sh_id, pr_id)
    print(select_all(conn, "shops"))
    print(select_all(conn, "products"))
    print(select_where(conn, "products", shop_id=1))
    update(conn, "shops", 1, name="Lidl")
    delete_where(conn, "products", id=1)
    delete_all(conn, "shops")
    conn.commit()
    conn.close()
