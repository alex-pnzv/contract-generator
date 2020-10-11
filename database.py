import json
import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users(id integer primary key, name text, edrpou text, iban text, "
                       "bank_mfo text, bank_name text, postal_code text, region text,district text, city text,"
                       "street text,house_num text, telephone text, stamp boolean )")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS dk(id integer primary key, code text, desc text)")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS address(id integer primary key, institution_name text, address text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS bank_accounts (id integer primary key, name text, value text)")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS templates(id integer primary key, template_name text, contract_type text, contract text, edrpou text, dk_num text, institution_name text,"
            "score_name text, contract_term text,delivery_term text, funding text, price text)")

        # self.insert_address_data()
        # self.insert_dk_data()
        # self.insert_users_data()
        self.conn.commit()

    def set_template(self, template_name, contract_type, contract, edrpou, dk_num, institution_name, score_name,
                     contract_term,
                     delivery_term, funding, price):
        self.c.execute(
            "INSERT INTO templates(template_name,contract_type,contract,edrpou,dk_num,institution_name,score_name,"
            "contract_term,delivery_term,funding,price) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (template_name, contract_type, contract, edrpou, dk_num, institution_name, score_name, contract_term,
             delivery_term, funding, price))
        self.conn.commit()

    def get_template_by_id(self, id):
        self.c.execute("SELECT * FROM templates WHERE id=?", (id,))
        return self.c.fetchone()

    def del_template_by_id(self, id):
        self.c.execute("DELETE FROM templates WHERE id=?", (id,))
        self.conn.commit()

    def set_users(self, name, edrpou, iban, bank_mfo, bank_name, postal, region, district, city, street, house,
                  telephone, stamp):
        self.c.execute('''INSERT INTO users (name, edrpou,iban,bank_mfo,bank_name,postal_code,region,district,city,
        street,house_num,telephone,stamp) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (name, edrpou, iban, bank_mfo, bank_name, postal,
                        region, district, city, street, house, telephone, stamp))
        self.conn.commit()

    def set_address(self, institution_name, address):
        self.c.execute("INSERT INTO address (institution_name, address) VALUES(?,?)", (institution_name, address))
        self.conn.commit()

    def set_bank_account(self, name, value):
        self.c.execute("INSERT INTO bank_accounts (name,value) VALUES (?,?)", (name, value))
        self.conn.commit()

    def get_user_by_id(self, id):
        self.c.execute('''SELECT name, edrpou,iban,bank_mfo,bank_name,postal_code,region,district,city,
                street,house_num,telephone,stamp FROM users WHERE id=?''', (id,))
        return self.c.fetchone()

    def get_user_by_edrpou(self, edrpou):
        self.c.execute('''SELECT name, edrpou,iban,bank_mfo,bank_name,postal_code,region,district,city,
                street,house_num,telephone,stamp FROM users WHERE edrpou=?''', (edrpou,))
        return self.c.fetchone()

    def update_user_by_id(self, id, name, edrpou, iban, bank_mfo, bank_name, postal, region, district, city, street,
                          house, telephone, stamp):
        self.c.execute('''UPDATE users SET name=?, edrpou=?,iban=?,bank_mfo=?,bank_name=?,postal_code=?,region=?,district=?,city=?,
                street=?,house_num=?,telephone=?, stamp=? WHERE id=?''', (
            name, edrpou, iban, bank_mfo, bank_name, postal, region, district, city, street, house, telephone, stamp,
            id))
        self.conn.commit()

    def update_address_by_id(self, id, institution_name, address):
        self.c.execute("UPDATE address SET institution_name=?, address=? WHERE id=?", (institution_name, address, id))
        self.conn.commit()

    def get_address_by_id(self, id):
        self.c.execute('SELECT institution_name, address FROM address WHERE id=?', (id,))
        return self.c.fetchone()

    def get_dk_by_id(self, id):
        self.c.execute("SELECT code,desc FROM dk WHERE id=?", (id,))
        return self.c.fetchone()

    def get_bank_account_by_id(self, id):
        self.c.execute("SELECT name,value FROM bank_accounts WHERE id=?", (id,))
        return self.c.fetchone()

    def update_dk_by_id(self, id, code, desc):
        self.c.execute("UPDATE dk SET code=?, desc=? WHERE id=?", (code, desc, id))
        self.conn.commit()

    def update_bank_account_by_id(self, id, name, value):
        self.c.execute("UPDATE bank_accounts SET name=?, value=? WHERE id=?", (name, value, id))
        self.conn.commit()

    def search_bank_account(self, value: str):
        self.c.execute("SELECT * FROM bank_accounts WHERE name LIKE ? or value LIKE ? ORDER BY name",
                       (value + '%', '%' + value + "%"))
        return self.c.fetchall()

    def search_address(self, value:str):
        self.c.execute("SELECT * FROM address WHERE institution_name LIKE ? ORDER BY institution_name", ("%"+value+'%',))
        return self.c.fetchall()

    def search_dk(self,value:str):
        self.c.execute("SELECT * FROM dk WHERE code LIKE ? or desc LIKE ? ORDER BY code",(value+'%',"%"+value+'%'))
        return self.c.fetchall()

    def search_user(self,value):
        self.c.execute("SELECT id,edrpou,name FROM users WHERE edrpou LIKE ? or name LIKE ? ORDER BY name",(value+'%',"%"+value+"%"))
        return self.c.fetchall()

    def get_bank_account_by_name(self, name):
        self.c.execute("SELECT value FROM bank_accounts WHERE name=?", (name,))
        return self.c.fetchone()

    def set_dk(self, code, desc):
        self.c.execute('''INSERT INTO dk (code,desc) VALUES(?,?)''', (code, desc))
        self.conn.commit()

    def del_dk(self, id):
        self.c.execute('DELETE FROM dk WHERE id=?', (id,))
        self.conn.commit()

    def del_address(self, id):
        self.c.execute("DELETE FROM address WHERE id=?", (id,))
        self.conn.commit()

    def del_user(self, id):
        self.c.execute('DELETE FROM users WHERE id=?', (id,))
        self.conn.commit()

    def del_bank_account(self, id):
        self.c.execute("DELETE FROM bank_accounts WHERE id=?", (id))
        self.conn.commit()

    def get_edrpou_list(self):
        rows = self.c.execute("SELECT edrpou FROM users")
        edrpou_list = []
        for row in rows:
            edrpou_list.append(row[0])
        return edrpou_list

    def get_bank_account_list(self):
        rows = self.c.execute('SELECT name FROM bank_accounts')
        bank_accounts = []
        for row in rows:
            bank_accounts.append(row[0])
        return bank_accounts

    def get_institution_name_list(self):
        rows = self.c.execute("SELECT institution_name FROM address")
        institution_list = []
        for row in rows:
            institution_list.append(row[0])
        return institution_list

    def get_delivery_address_by_name(self, name):
        self.c.execute("SELECT address FROM address WHERE institution_name=?", (name,))
        return self.c.fetchone()

    def get_templates(self):
        self.c.execute("SELECT id,template_name FROM templates")
        return self.c.fetchall()

    def insert_address_data(self):
        with open('address.json', encoding='utf-8') as file:
            data = json.load(file)
            for row in data:
                self.c.execute("INSERT INTO address (institution_name, address) VALUES (?,?)", (row, data[row]))

    def insert_dk_data(self):
        with open("dk.json", encoding='utf-8') as file:
            dk = json.load(file)
            for item in dk:
                self.c.execute("INSERT INTO dk (code,desc) VALUES(?,?)", (item, dk[item]['FIELD2']))

    def insert_users_data(self):
        with open('users.json', encoding="utf-8-sig") as file:
            users = json.load(file)
            for user in users['Лист1']:
                print(user)
                self.c.execute(
                    "INSERT INTO users (name, edrpou,iban,bank_name,postal_code,region,district,city, street,house_num,telephone,stamp,bank_mfo) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (user['name'], user["edrpou"], user["iban"], user["bank_name"], user["postal"], user["region"],
                     user.get("district"), user["city "], user['street'], user['house'], user["tel"],
                     user['stamp'], user['mfo']))
