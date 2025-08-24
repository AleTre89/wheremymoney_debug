import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Matching:
    def __init__(self):
        self.match_mask = tk.Toplevel()
        self.match_mask.title = "Category Matching"
        self.match_mask.geometry = '800x800'

        #labels, comboboxes & entry
        self.cat_lbl = tk.Label(self.match_mask,text="Category")
        self.cat_cbx = ttk.Combobox(self.match_mask,state='readonly')
        self.subcat_lbl = tk.Label(self.match_mask, text="SubCategory")
        self.subcat_cbx = ttk.Combobox(self.match_mask,state='readonly')
        self.string_lbl = tk.Label(self.match_mask, text="String")
        self.string_text = tk.Entry(self.match_mask)

        #Buttons
        self.add_match_but = tk.Button(self.match_mask,text="Add matching", command=self.add_matching)
        self.del_match_but = tk.Button(self.match_mask,text="Delete matching")

        #treeview
        self.match_tree = ttk.Treeview(self.match_mask, columns=("Category","SubCategory","String"))

        self.match_tree.column("#0",width=15,minwidth=5)
        self.match_tree.column("Category", width=100, minwidth=5)
        self.match_tree.column("SubCategory", width=100, minwidth=5)
        self.match_tree.column("String", width=100, minwidth=5)

        self.match_tree.heading("Category",text="Category")
        self.match_tree.heading("SubCategory",text="SubCategory")
        self.match_tree.heading("String",text="String")

        #positioning
        self.cat_lbl.grid(row=0,column=0,padx=10, pady=10)
        self.cat_cbx.grid(row=0,column=1,padx=10, pady=10)
        self.subcat_lbl.grid(row=1,column=0,padx=10, pady=10)
        self.subcat_cbx.grid(row=1,column=1,padx=10, pady=10)
        self.string_lbl.grid(row=2,column=0,padx=10, pady=10)
        self.string_text.grid(row=2,column=1,padx=10, pady=10)
        self.add_match_but.grid(row=3,column=0,padx=10, pady=10)
        self.del_match_but.grid(row=3,column=1,padx=10, pady=10)
        self.match_tree.grid(row=4,column=0,padx=10, pady=10,columnspan=2)


        self.cbx_filling()
        self.cat_cbx.bind('<<ComboboxSelected>>',self.get_subcat)
        self.populate_tree()




        self.match_mask.mainloop()

    def populate_tree(self):
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        self.match_tree.delete(*self.match_tree.get_children())
        count=0

        match_list = cur.execute('SELECT c.category,s.subcategory, m.string '
                                 'FROM matching AS m '
                                 'LEFT JOIN sub_categories AS s ON s.id_subcat=m.id_subcat '
                                 'LEFT JOIN categories AS c ON c.id_cat=m.id_cat').fetchall()

        for match in match_list:
            self.match_tree.insert('',index='end',id=count,
                                   values=(match[0],match[1],match[2]))
            count+=1

        con.close()

    def add_matching(self):
        #global string_text
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()

        try:
            cat_text = self.cat_cbx.get()
            id_cat = cur.execute('SELECT id_cat FROM categories AS c '
                                 'WHERE c.category = ?', (cat_text,)).fetchone()[0]
            subcat_text = self.subcat_cbx.get()
            id_subcat = cur.execute('SELECT id_subcat FROM sub_categories AS s '
                                 'WHERE s.subcategory = ?', (subcat_text,)).fetchone()[0]

            string_text = self.string_text.get().upper()

            if string_text != '':
                max_id = cur.execute('SELECT MAX(id_match) FROM matching').fetchone()[0]
                if max_id is None:
                    new_id=0
                else:
                    new_id =max_id + 1

                cur.execute('INSERT INTO matching VALUES (?,?,?,?)',
                            (new_id,id_cat,id_subcat,string_text))
                con.commit()

            else:
                err_msg = messagebox.showerror('Empty String', 'Please insert a string')

        except TypeError:
            err_msg = messagebox.showerror('Empty data','Please insert all the data')

        self.populate_tree()
        con.close()

    def cbx_filling(self):
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        category_list = [cat[0] for cat in cur.execute("SELECT category FROM categories").fetchall()]
        self.cat_cbx.config(values=category_list)

        con.close()

    def get_subcat(self,event):
        self.subcat_cbx.set('')
        cat_selected =self.cat_cbx.get()
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        selected_cat_list = cur.execute("SELECT categories.category, sub_categories.subcategory "
             "FROM categories "
             "LEFT JOIN sub_categories ON categories.id_cat=sub_categories.id_cat "
                                        "WHERE categories.category=?", (cat_selected,)).fetchall()
        subcat_list = [subcat[1] for subcat in selected_cat_list]

        if subcat_list[0] is not None:
            self.subcat_cbx.config(values=subcat_list)
        else:
            self.subcat_cbx.config(values=[''])

        con.close()
