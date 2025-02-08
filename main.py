from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
import pymysql 
import random
import csv
from datetime import datetime
import numpy as np

window = tkinter.Tk()
window.title("Stock Management System")
window.geometry("720x640")
my_tree = ttk.Treeview(window,show="headings",height=20)
style = ttk.Style()


placeHolderArray = ["","","","",""]
numeric = "0123456789"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def connect_to_database():
    conn = pymysql.connect(host="localhost",user="root",password="",database="stock_management_system")
    return conn
conn = connect_to_database()
cursor = conn.cursor()



for i in range(0,5):
    placeHolderArray[i] = tkinter.StringVar()


def read_data_from_database():
    cursor.connection.ping()
    sql=f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM `stocks` order by `id` desc"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data



def refreshtable():

    for data in my_tree.get_children():

        my_tree.delete(data)
    for item in read_data_from_database():
        my_tree.insert(parent="",index="end",iid=item,text="",values=(item))
    my_tree.tag_configure("oddrow",background="white")
    my_tree.tag_configure("evenrow",background="lightgray")
    my_tree.pack(expand=True,fill=BOTH)

def setItemId(word,number):
    for i in range(0,5):
        if i == number:
            placeHolderArray[i].set(word)


def generateRand():
    itemId = ''
    for i in range(0,5):
        randomNumber = random.randrange(0,(len(numeric)-1))
        itemId = itemId + str(numeric[randomNumber])
    randomNumber=random.randrange(0,(len(alphabet)-1))
    itemId = itemId + '~'+ str(alphabet[randomNumber])
    print("generated id: ",itemId)
    setItemId(itemId,0)

def save():
    itemId = str(itemIdEntry.get()).strip()
    name = str(nameEntry.get()).strip()
    price = str(priceEntry.get()).strip()
    qnt = str(qntEntry.get()).strip()
    cat = str(categoryCombo.get()).strip()
    valid = True

    # Empty fields validation
    if not all([itemId, name, price, qnt, cat]):
        messagebox.showwarning("", "Please fill up all entries")
        return

    # ID validation
    if len(itemId) != 7 or itemId[5] != '~':
        valid = False
    else:
        # Validate numeric part
        for i in range(0, 5):
            if itemId[i] not in numeric:
                valid = False
                break
        # Validate alphabetic part
        if valid and itemId[6] not in alphabet:
            valid = False

    if not valid:
        messagebox.showwarning("", "Invalid Item ID")
        return

    # Check for duplicate ID
    try:
        cursor.connection.ping()
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE item_id = %s", (itemId,))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("", "Item Id already used")
            return

        # Validate price and quantity are numeric
        if not all(c.isdigit() or c == '.' for c in price):
            messagebox.showwarning("", "Price must contain only numbers")
            return
        if not qnt.isdigit():
            messagebox.showwarning("", "Quantity must contain only numbers")
            return

        # Insert the data
        sql = """INSERT INTO stocks 
                (item_id, name, price, quantity, category, date) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (itemId, name, float(price), int(qnt), cat, datetime.now())
        cursor.execute(sql, values)
        conn.commit()

        # Clear fields
        itemIdEntry.delete(0, END)
        nameEntry.delete(0, END)
        priceEntry.delete(0, END)
        qntEntry.delete(0, END)
        categoryCombo.set('')

        messagebox.showinfo("Success", "Item saved successfully!")
        refreshtable()

    except Exception as e:
        messagebox.showwarning("", "Error while saving ref: " + str(e))
    finally:
        conn.close()

def update():
    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])   
    except:
        messagebox.showwarning("", "Please select a data row")
        return

    itemId = str(itemIdEntry.get()).strip()
    name = str(nameEntry.get()).strip()
    price = str(priceEntry.get()).strip()
    qnt = str(qntEntry.get()).strip()
    cat = str(categoryCombo.get()).strip()

    if not all([itemId, name, price, qnt, cat]):
        messagebox.showwarning("", "Please fill up all entries")
        return

    if selectedItemId != itemId:
        messagebox.showwarning("", "You can't change Item ID")
        return

    # Validate price and quantity are numeric
    if not all(c.isdigit() or c == '.' for c in price):
        messagebox.showwarning("", "Price must contain only numbers")
        return
    if not qnt.isdigit():
        messagebox.showwarning("", "Quantity must contain only numbers")
        return

    try:
        cursor.connection.ping()
        sql = """UPDATE stocks 
                SET name = %s, price = %s, quantity = %s, category = %s 
                WHERE item_id = %s"""
        values = (name, float(price), int(qnt), cat, itemId)
        cursor.execute(sql, values)
        conn.commit()
        
        # Clear fields
        itemIdEntry.delete(0, END)
        nameEntry.delete(0, END)
        priceEntry.delete(0, END)
        qntEntry.delete(0, END)
        categoryCombo.set('')
        
        messagebox.showinfo("Success", "Item updated successfully!")
        refreshtable()
    except Exception as err:
        messagebox.showwarning("", "Error occurred ref: " + str(err))
    finally:
        conn.close()

def delete():
    try:
        if not my_tree.selection():
            messagebox.showwarning("", "Please select a data row")
            return

        decision = messagebox.askquestion("", "Delete the selected data?")
        if decision != 'yes':
            return

        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        
        cursor.connection.ping()
        cursor.execute("DELETE FROM stocks WHERE item_id = %s", (itemId,))
        conn.commit()
        messagebox.showinfo("", "Data has been successfully deleted")
        refreshtable()
    except Exception as e:
        messagebox.showinfo("", "Sorry, an error occurred: " + str(e))

def select():
    try:
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        cat = str(my_tree.item(selectedItem)['values'][4])
        setItemId(itemId,0)
        setItemId(name,1)
        setItemId(price,2)
        setItemId(qnt,3)
        setItemId(cat,4)
    except:
        messagebox.showwarning("", "Please select a data row")

def find():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    cursor.connection.ping()
    if(itemId and itemId.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `item_id` LIKE '%{itemId}%' "
    elif(name and name.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `name` LIKE '%{name}%' "
    elif(price and price.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `price` LIKE '%{price}%' "
    elif(qnt and qnt.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `quantity` LIKE '%{qnt}%' "
    elif(cat and cat.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `category` LIKE '%{cat}%' "
    else:
        messagebox.showwarning("","Please fill up one of the entries")
        return
    cursor.execute(sql)
    try:
        result = cursor.fetchall();
        for num in range(0,5):
            setItemId(result[0][num],(num))
        conn.commit()
        conn.close()
    except:
        messagebox.showwarning("","No data found")

def clear():
    for num in range(0,5):
        setItemId('',(num))

def exportExcel():
    cursor.connection.ping()
    sql=f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC"
    cursor.execute(sql)
    dataraw=cursor.fetchall()
    date = str(datetime.now())
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:16]
    with open("stocks_"+dateFinal+".csv",'a',newline='') as f:
        w = csv.writer(f, dialect='excel')
        for record in dataraw:
            w.writerow(record)
    print("saved: stocks_"+dateFinal+".csv")
    conn.commit()
    conn.close()
    messagebox.showinfo("","Excel file downloaded")

    


frame=tkinter.Frame(window,bg="#24001f")
frame.pack()





btnColor ="#d975cb"


manageFrame = tkinter.LabelFrame(frame,text="Manage Stock",borderwidth=5,relief="groove",font=("Helvetica",12,"bold"))
manageFrame.grid(row=0,column=0,sticky="w",padx=[10,200],pady=20,ipadx=[6])

saveBtn = tkinter.Button(manageFrame,text="Save",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=save)
updateBtn = tkinter.Button(manageFrame,text="Update",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=update)
deleteBtn = tkinter.Button(manageFrame,text="Delete",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=delete)
selectBtn = tkinter.Button(manageFrame,text="Select",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=select)

findBtn = tkinter.Button(manageFrame,text="Find",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=find)
clearBtn = tkinter.Button(manageFrame,text="Clear",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=clear)
exportBtn = tkinter.Button(manageFrame,text="Export CSV",width=15,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=exportExcel)



saveBtn.grid(row=0,column=0,padx=5,pady=5)
updateBtn.grid(row=0,column=1,padx=5,pady=5)
deleteBtn.grid(row=0,column=2,padx=5,pady=5)
selectBtn.grid(row=0,column=3,padx=5,pady=5)
findBtn.grid(row=0,column=4,padx=5,pady=5)
clearBtn.grid(row=0,column=5,padx=5,pady=5)
exportBtn.grid(row=0,column=6,padx=5,pady=5)

entiresframe = tkinter.LabelFrame(frame,text="Enter Stock Details",borderwidth=5,relief="groove",font=("Helvetica",10,"bold"))
entiresframe.grid(row=1,column=0,sticky="w",padx=[10,200],pady=20,ipadx=[6])   

itemIdLabel = tkinter.Label(entiresframe,text="Item ID",anchor="e",font=("Helvetica",10,"bold"))
nameLabel = tkinter.Label(entiresframe,text="Name",anchor="e",font=("Helvetica",10,"bold"))
priceLabel = tkinter.Label(entiresframe,text="Price",anchor="e",font=("Helvetica",10,"bold"))
qntLabel = tkinter.Label(entiresframe,text="Quantity",anchor="e",font=("Helvetica",10,"bold"))
categoryLabel = tkinter.Label(entiresframe,text="Category",anchor="e",font=("Helvetica",10,"bold"))

itemIdLabel.grid(row=0,column=0,padx=10,pady=5)
nameLabel.grid(row=1,column=0,padx=10,pady=5)
priceLabel.grid(row=2,column=0,padx=10,pady=5)
qntLabel.grid(row=3,column=0,padx=10,pady=5)
categoryLabel.grid(row=4,column=0,padx=10,pady=5)

categoryArray = [
  "Electronics",
  "Computer Components",
  "Laptops & Notebooks",
  "Desktops & All-in-Ones",
  "Computer Accessories",
  "Networking Devices",
  "Printers & Scanners",
  "Storage Devices",
  "Software",
  "Gaming Hardware",
  "Peripherals (Keyboards, Mice, etc.)",
  "Monitors & Displays",
  "Power Supplies & UPS",
  "Cables & Adapters",
  "DIY PC Building Tools",
  "Hardware Tools & Equipment",
  "Other"
];
itemIdEntry = tkinter.Entry(entiresframe,width=50,textvariable=placeHolderArray[0],font=("Helvetica",10,"bold"))
nameEntry = tkinter.Entry(entiresframe,width=50,textvariable=placeHolderArray[1],font=("Helvetica",10,"bold"))
priceEntry = tkinter.Entry(entiresframe,width=50,textvariable=placeHolderArray[2],font=("Helvetica",10,"bold"))
qntEntry = tkinter.Entry(entiresframe,width=50,textvariable=placeHolderArray[3],font=("Helvetica",10,"bold"))
categoryCombo = ttk.Combobox(entiresframe,width=47,textvariable=placeHolderArray[4],values=categoryArray,font=("Helvetica",10,"bold"))


itemIdEntry.grid(row=0,column=2,padx=10,pady=5)
nameEntry.grid(row=1,column=2,padx=10,pady=5)
priceEntry.grid(row=2,column=2,padx=10,pady=5)
qntEntry.grid(row=3,column=2,padx=10,pady=5)
categoryCombo.grid(row=4,column=2,padx=10,pady=5)   

generateIdBtn = tkinter.Button(entiresframe,text="Generate ID",width=10,borderwidth=3,bg=btnColor,fg="white",font=("Helvetica",9,"bold"),command=generateRand)
generateIdBtn.grid(row=0,column=3,padx=10,pady=5)

style.configure(window)

my_tree["columns"] = ("Item ID", "Name", "Price", "Quantity", "Category", "Date")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item ID", anchor=W, width=100)
my_tree.column("Name", anchor=W, width=100)
my_tree.column("Price", anchor=W, width=100)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=100)
my_tree.column("Date", anchor=W, width=100)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Item ID", text="Item ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)

my_tree.tag_configure("oddrow",background="white")
my_tree.tag_configure("evenrow",background="lightgray")
my_tree.pack(expand=True,fill=BOTH)


refreshtable()

window.resizable(False,False)
window.mainloop()





