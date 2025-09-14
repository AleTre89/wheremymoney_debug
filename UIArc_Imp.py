import os.path
import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import datetime as dt
from tkinter import messagebox

from UIMatching import Matching

#TODO create 2 different archives for importing and visualizing historical data
class Archive:
    def __init__(self,root):
        self.arc_mask = tk.Toplevel(root)
        self.arc_mask.title("Archive")
        self.arc_mask.geometry("1200x600")

        self.arc_tree = ttk.Treeview(self.arc_mask, columns=(
                                                "Date",
                                                "Amount",
                                                "Description",
                                                "Category",
                                                "Sub-Category"))

        self.arc_tree.column("#0",width=15)
        self.arc_tree.column("Date",width=100)
        self.arc_tree.heading("Date", text="Date")
        self.arc_tree.column("Amount",width=100)
        self.arc_tree.heading("Amount", text="Amount")
        self.arc_tree.column("Description",width=300)
        self.arc_tree.heading("Description", text="Description")
        self.arc_tree.column("Category",width=150)
        self.arc_tree.heading("Category", text="Category")
        self.arc_tree.column("Sub-Category",width=150)
        self.arc_tree.heading("Sub-Category", text="Sub-Category")



        self.description_text= tk.Text(self.arc_mask,height=3,width=100,wrap="word")


        self.date_lbl = tk.Label(self.arc_mask,text='Date')
        self.amount_lbl = tk.Label(self.arc_mask, text='Amount')
        self.category_lbl = tk.Label(self.arc_mask, text='Category')
        self.subcategory_lbl = tk.Label(self.arc_mask, text='Subcategory')

        self.date_text = tk.Label(self.arc_mask)
        self.amount_text = tk.Label(self.arc_mask)
        self.cat_cbx = ttk.Combobox(self.arc_mask,state='readonly')
        self.subcat_cbx = ttk.Combobox(self.arc_mask, state='readonly')

        self.update_button = tk.Button(self.arc_mask,text='Update', command=self.update_item)
        self.upload_button = tk.Button(self.arc_mask,text='Upload', command=self.upload_to_db)
        self.cat_match_button = tk.Button(self.arc_mask,text='Category Matching',command=self.goto_match)

        self.arc_tree.grid(row=1,column=0,padx=10,pady=10,rowspan=7)

        self.date_lbl.grid(row=1,column=1,padx=10,pady=10)
        self.date_text.grid(row=1, column=2, padx=10, pady=10)
        self.amount_lbl.grid(row=2, column=1, padx=10, pady=10)
        self.amount_text.grid(row=2, column=2, padx=10, pady=10)
        self.category_lbl.grid(row=3, column=1, padx=10, pady=10)
        self.cat_cbx.grid(row=3, column=2, padx=10, pady=10)
        self.subcategory_lbl.grid(row=4, column=1, padx=10, pady=10)
        self.subcat_cbx.grid(row=4, column=2, padx=10, pady=10)

        self.update_button.grid(row=5, column=2, padx=10, pady=10)
        self.upload_button.grid(row=6, column=2, padx=10, pady=10)
        self.cat_match_button.grid(row=7, column=2, padx=10, pady=10)

        self.description_text.grid(row=8,column=0,padx=10,pady=10)


        self.arc_tree.bind('<<TreeviewSelect>>',self.get_descr)
        self.cat_cbx.bind('<<ComboboxSelected>>',self.get_subcat)

        self.getdata()
        self.cbx_filling()


    def goto_match(self):
        match=Matching()

    def upload_to_db(self):
        tot_rec = self.arc_tree.get_children()

        for c in tot_rec:
            con = sqlite3.connect('database/database.db')
            cur = con.cursor()
            id_record = cur.execute('SELECT COALESCE(MAX(id_record)+1,0) FROM record').fetchone()[0]

            values_import = self.arc_tree.item(c)['values']
            #id_cat
            cat_name = values_import[3]
            try:
                id_cat = cur.execute('SELECT id_cat FROM categories WHERE category = ?',
                                    (cat_name,)).fetchone()[0]
            except TypeError:
                id_cat=1000

            #id_subcat
            subcat_name = values_import[4]
            try:
                id_subcat = cur.execute('SELECT id_subcat FROM sub_categories WHERE subcategory = ?',
                                 (subcat_name,)).fetchone()[0]
            except TypeError:
                id_subcat =1000

            #date
            date_full = values_import[0]
            date = dt.datetime.strptime(date_full,'%Y-%m-%d %H:%M:%S')
            date_to_insert = dt.datetime.strftime(date,'%Y-%m-%d')

            #amount
            amount = values_import[1]


            cur.execute('INSERT INTO record VALUES (?,?,?,?,?)',
                        (id_record,id_cat,id_subcat,date_to_insert,amount))
            con.commit()
            con.close()

            if os.path.exists('estratti/elenco.xlsx'):
                os.remove('estratti/elenco.xlsx')



    def update_item(self):
        #TODO if cbx emtpy error
        cat_value = self.cat_cbx.get()
        subcat_value = self.subcat_cbx.get()


        item=self.arc_tree.selection()[0]
        date = self.arc_tree.item(item)['values'][0]
        amount = self.arc_tree.item(item)['values'][1]
        description = self.arc_tree.item(item)['values'][2]

        self.arc_tree.item(item, values=(date,amount,description,cat_value,subcat_value))




    def get_descr(self,event):
        desc_text = self.arc_tree.selection()[0]
        description = self.arc_tree.item(desc_text)['values']

        self.description_text.config(state='normal')
        self.description_text.delete('1.0','end')
        self.description_text.insert('end',description[2])
        self.description_text.config(state='disabled')

        self.date_text.config(text=description[0])
        self.amount_text.config(text=description[1])

    def cbx_filling(self):
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        category_list = [cat[0] for cat in cur.execute("SELECT category FROM categories").fetchall()]
        self.cat_cbx.config(values=category_list)

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

        if subcat_list[0] != None:
            self.subcat_cbx.config(values=subcat_list)
        else:
            self.subcat_cbx.config(values=[''])

        con.close()

    # DATA CONTABILE
    # DATA VALUTA
    # CAUSALE
    # DESCRIZIONE OPERAZIONE
    # IMPORTO IN EURO
    def getdata(self):
        try:
            df = pd.read_excel("./estratti/elenco.xlsx")
        except FileNotFoundError:
            messagebox.showinfo('Nessun File', 'Inserire file nella cartella estratti ')
            return
        df_dict = df.to_dict(orient="dict")

        tot_rec =len(df_dict["CAUSALE"])

        count = 0
        for rec in range(0,tot_rec):
            con = sqlite3.connect("database/database.db")
            cur = con.cursor()

            string_list = cur.execute("SELECT c.category,s.subcategory,m.string "
                           "FROM matching AS m "
                           "LEFT JOIN categories AS c ON c.id_cat = m.id_cat "
                           "LEFT JOIN sub_categories AS s ON s.id_subcat = m.id_subcat").fetchall()
            string_to_search = df_dict["DESCRIZIONE OPERAZIONE"][rec].upper()

            cat_subcat_match = ['', '']
            for element in string_list:
                if string_to_search.find(element[2]) >=0:
                    cat_subcat_match = [element[0],element[1]]



            self.arc_tree.insert('',index="end",iid=count,values=(
                df_dict["DATA CONTABILE"][rec],
                df_dict["IMPORTO IN EURO"][rec],
                df_dict["DESCRIZIONE OPERAZIONE"][rec],
                cat_subcat_match[0],
                cat_subcat_match[1]
            ))
            count+=1