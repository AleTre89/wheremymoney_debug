#test numero 2

import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

from UIArc_Imp import Import,Archive
from UICategories import Categories
from UIMatching import Matching

mask = tk.Tk()
mask.title("Family Budget")
mask.geometry("700x400")



def add_record():
    con = sqlite3.connect('database/database.db')
    cur = con.cursor()

    id_rec = 1
    date_rec = date_entry.get()
    amount_rec = float(amount_entry.get())
    id_cat = "cat1"
    id_subcat = "subcat1"

    data= [id_rec,date_rec,amount_rec,id_cat,id_subcat]

    cur.execute("INSERT INTO record VALUES (?,?,?,?,?)", data)
    con.commit()

    con.close()

def goto_cat_mask():
    open_cat_mask = Categories()

def goto_import():
    open_import = Import()

def goto_archive():
    open_archive = Archive()

def goto_match():
    open_match = Matching()

#labels
insert = tk.Label(mask, text="Insert manually")
date = tk.Label(mask, text="Date")
amount = tk.Label(mask, text="Amount")
category = tk.Label(mask, text="Category")
subcategory = tk.Label(mask, text="SubCategory")

#entry
date_entry = tk.Entry(mask)
amount_entry = tk.Entry(mask)

#combobox
#TODO bind cbx values to sql database
category_cbx = ttk.Combobox(mask, values=["House"])
subcategory_cbx = ttk.Combobox(mask, values=["Furniture","Maintenance"])

#buttons
add_button = tk.Button(mask, text="Add",command=add_record)
import_button = tk.Button(mask, text="Import excel",
                          command= goto_import)
archive_button = tk.Button(mask, text="Archive",
                           command=goto_archive)
categories_button = tk.Button(mask, text="Categories",command=goto_cat_mask)
cat_matching_button = tk.Button(mask, text="Categories matching", command=goto_match)

#posizionamento
insert.grid(row=0, column =0,pady=20)

date.grid(row=1, column=0, pady=10, padx=10)
date_entry.grid(row=1, column=1, pady=10, padx=10)
amount.grid(row=1, column=2, pady=10, padx=10)
amount_entry.grid(row=1, column=3, pady=10, padx=10)

category.grid(row=2, column=0, pady=10, padx=10)
category_cbx.grid(row=2, column=1, pady=10, padx=10)
subcategory.grid(row=2, column=2, pady=10, padx=10)
subcategory_cbx.grid(row=2, column=3, pady=10, padx=10)

add_button.grid(row=3, column=0, pady=10, padx=10)

import_button.grid(row=4,column=0,pady=10, padx=10)
archive_button.grid(row=4,column=1,pady=10, padx=10)
categories_button.grid(row=4,column=2,pady=10, padx=10)
cat_matching_button.grid(row=4,column=3, pady=10, padx=10)

mask.mainloop()