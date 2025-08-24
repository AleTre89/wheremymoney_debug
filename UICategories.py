import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import sqlite3


class Categories:
    def __init__(self):
        self.cat_mask = tk.Toplevel()
        self.cat_mask.title("Categories")
        self.cat_mask.geometry("400x600")

        #labels
        self.cat_label= tk.Label(self.cat_mask, text="Category")
        self.subcat_label = tk.Label(self.cat_mask, text="Subcategory")

        #combobox
        self.cat_cbx= ttk.Combobox(self.cat_mask)
        self.subcat_cbx = ttk.Combobox(self.cat_mask)

        #buttons
        self.cat_button = tk.Button(self.cat_mask,text="Add Category",width=15,command=self.add_category)
        self.subcat_button = tk.Button(self.cat_mask,text="Add SubCategory",width=15, command=self.add_subcategory)

        #positioning
        self.cat_label.grid(row=0, column=0, padx=10, pady=10)
        self.cat_cbx.grid(row=0, column=1, padx=10, pady=10)
        self.cat_button.grid(row=0, column=2, padx=10, pady=10)

        self.subcat_label.grid(row=1, column=0, padx=10, pady=10)
        self.subcat_cbx.grid(row=1, column=1, padx=10, pady=10)
        self.subcat_button.grid(row=1, column=2, padx=10, pady=10)

        #treeview
        self.cat_tree = ttk.Treeview(self.cat_mask, columns="Category")
        self.cat_tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.cat_tree.column("#0",width=50,minwidth=0)
        self.cat_tree.column("Category", width=300,minwidth=100)
        self.cat_tree.heading("Category", text="Category")

        self.cat_cbx.bind('<<ComboboxSelected>>', self.get_subcat)

        self.populate_tree()

        self.cat_mask.mainloop()


    def get_subcat(self,event):
        self.subcat_cbx.delete(0, 'end')
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

#TODO create column active - True by default
#TODO create gestione button to activate / deactivate categories
    def add_category(self):
        """Add data from categories combobox to db table categories"""
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()

        #TODO id_cat as str - number not in sequence
        id_cat = int(cur.execute("SELECT MAX(id_cat) FROM categories").fetchone()[0])
        if id_cat == None:
            id_cat = 0
        else:
            id_cat+=1
        category=self.cat_cbx.get()

        category_list= [cat[0] for cat in cur.execute("SELECT category FROM categories").fetchall()]

        if category == "":
            error_no_record = messagebox.showerror("Error: No category digited",
                                                   "You didn't insert new category.\n"
                                                           "Digit category in combobox.")
        elif category in category_list:
            error_already_exixst = messagebox.showerror("Error: Category already exists",
                                                        "Category already exists")
        else:
            want_to_insert = messagebox.askokcancel("insert new category?",
                                   f"Do you want to insert the category: {category}?",)
            if want_to_insert:
                cur.execute("INSERT INTO categories VALUES (?,?)", (id_cat,category))
                con.commit()
                con.close()

        self.populate_tree()

    def add_subcategory(self):
        """Add data from subcategories combobox to db table sub_categories"""
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()

        #TODO fix max value in integer type
        id_subcat = cur.execute("SELECT MAX(id_subcat) FROM sub_categories").fetchone()[0]
        if id_subcat == None:
            id_subcat = 0
        else:
            id_subcat+=1
        subcat=self.subcat_cbx.get()
        category = self.cat_cbx.get()

        subcat_list= [subcat[0] for subcat in cur.execute("SELECT subcategory FROM sub_categories").fetchall()]
        category_list = [cat[0] for cat in cur.execute("SELECT category FROM categories").fetchall()]

        id_cat = cur.execute(f"SELECT id_cat FROM categories WHERE category = '{category}'").fetchone()[0]

        cod_subcat = f"{subcat}_{id_subcat}"

        if subcat == "":
            error_no_record = messagebox.showerror("Error: No subcategory digited",
                                                   "You didn't insert new subcategory.\n"
                                                           "Digit subcategory in combobox.")
        elif subcat in subcat_list:
            error_already_exixst = messagebox.showerror("Error: subcategory already exists",
                                                        "subcategory already exists")
        elif category == "" or category not in category_list:
            error_category = messagebox.showerror("Error: category",
                                                        "category empty or not exists")
        else:
            want_to_insert = messagebox.askokcancel("insert new subcategory?",
                                   f"Do you want to insert the subcategory: {subcat}?",)
            if want_to_insert:
                cur.execute("INSERT INTO sub_categories VALUES (?,?,?,?)", (id_subcat,id_cat,cod_subcat,subcat))
                con.commit()
                con.close()

        self.populate_tree()


    def populate_tree(self):
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        category_list = [cat[0] for cat in cur.execute("SELECT category FROM categories").fetchall()]

        count=0
        for cat in category_list:
            if self.cat_tree.exists(str(count)) ==1:
                count+=1
            else:
                self.cat_tree.insert(parent='',index="end",id=count, values=(cat,))
                count +=1

        #TODO insert subcategories in treeview
        complete_cat_list = cur.execute('SELECT categories.category, sub_categories.subcategory '
             'FROM categories '
             'LEFT JOIN sub_categories ON categories.id_cat=sub_categories.id_cat').fetchall()

        n_sub=0
        for cat in self.cat_tree.get_children():
            nome_cat = self.cat_tree.item(cat)["values"][0]
            for sub in complete_cat_list:
                if sub[0] == nome_cat and sub[1]!=None:
                    subcount = f"S{n_sub}"
                    self.cat_tree.insert(parent=cat, index="end", id=subcount, values=(sub[1],))
                    n_sub+=1



        #TODO insert subcategories in treeview
        self.cat_cbx.config(values=category_list)
        #TODO insert subcat in cbx in relation to category
