import sqlite3

from pandas.core.accessor import delegate_names

con = sqlite3.connect('database/database.db')
cur= con.cursor()

#create tables
categories_table = ('CREATE TABLE IF NOT EXISTS categories('
                    'id_cat INTEGER NOT NULL PRIMARY KEY,'
                    'category VARCHAR NOT NULL)')
sub_categories_table = ('CREATE TABLE IF NOT EXISTS sub_categories('
                        'id_subcat INTEGER NOT NULL PRIMARY KEY,'
                        'id_cat INTEGER NOT NULL,'
                        'subcategory VARCHAR NOT NULL,'
                        'FOREIGN KEY (id_cat) REFERENCES categories (id_cat))')
matching_table = ('CREATE TABLE IF NOT EXISTS matching('
                  'id_match INTEGER NOT NULL PRIMARY KEY,'
                  'id_cat INTEGER NOT NULL,'
                  'id_subcat INTEGER NOT NULL,'
                  'string VARCHAR NOT NULL,'
                  'FOREIGN KEY (id_cat) REFERENCES categories (id_cat)'
                  'FOREIGN KEY (id_subcat) REFERENCES sub_categories (id_subcat))')
record_table = ('CREATE TABLE IF NOT EXISTS record('
                'id_record INTEGER NOT NULL PRIMARY KEY,'
                'id_cat INTEGER NOT NULL,'
                'id_subcat INTEGER NOT NULL,'
                'date DATE NOT NULL,'
                'amount DOUBLE NOT NULL,'
                'FOREIGN KEY (id_cat) REFERENCES categories (id_cat)'
                'FOREIGN KEY (id_subcat) REFERENCES sub_categories (id_subcat))')

del_cat = 'DELETE FROM categories'
del_subcat = 'DELETE FROM sub_categories'
del_record = 'DELETE FROM record'
del_match = 'DELETE FROM matching'

cur.execute(del_match)
cur.execute(del_cat)
cur.execute(del_subcat)
cur.execute(del_record)

con.commit()
con.close()