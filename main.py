import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from configparser import ConfigParser
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')


conn=sqlite3.connect('prison.db')
c= conn.cursor()


def createDb():
    c = conn.cursor()
    c.execute('CREATE TABLE offence (id num primary key, name text)')
    c.execute('CREATE TABLE dungeon (id num primary key, name text,size num)')
    c.execute(
        'CREATE TABLE person (id num primary key,firstname text,father text, lastname text,gender text,birthyear num ,address text)')
    c.execute(
        'CREATE TABLE visitings (id num primary key,datevisited date,personid num,visitorname text, mountainminutes num, foreign key(personid) references person(id) )')
    c.execute(
        'CREATE TABLE convicts (id num primary key,fromdate date,todate date,personid num, offenceid num, foreign key(personid) references person(id) ,foreign key(offenceid) references offence(id))')
    c.execute(
        'CREATE TABLE dungeonmove (id num primary key,fromdate date,personid num, dungeonid num, foreign key(personid) references person(id) ,foreign key(dungeonid) references dungeon(id))')
    c.execute('PRAGMA foreign_keys = ON')

    # Dungeon
    c.execute('insert into dungeon values (1 ,"Sednaya", 500)')
    c.execute('insert into dungeon values (2 ,"Palestine", 500)')
    c.execute('insert into dungeon values (3 ,"Mazzah", 500)')

    # offence
    c.execute('insert into offence values (1 ,"Theft")')
    c.execute('insert into offence values (2 ,"Murder")')
    c.execute('insert into offence values (3 ,"Hacking")')

    # Person
    c.execute('insert into person values (1 , "ahmad","fady", "hsan","male",1993,"hama")')
    c.execute('insert into person values (2 , "naji","ahmad", "saleh","male",1995,"aleppo")')
    c.execute('insert into person values (3 , "khaled","jasem", "aljasem","male",1990,"homs")')
    c.execute('insert into person values (4 , "jane","smith", "smith","female",1985,"damascus")')

    # visitor
    c.execute('insert into visitings values (1 , 2019,1,"ahmad",60)')
    c.execute('insert into visitings values (2 , 2015,2,"mhmd",60)')

    # convicts
    c.execute('insert into convicts values (1 ,2010,2022,1 , 1)')
    c.execute('insert into convicts values (2 ,2015,2020,2 , 2)')
    c.execute('insert into convicts values (3 ,2013,2019,3 , 3)')
    c.execute('insert into convicts values (4 ,2014,2021,4 , 1)')

    # DungeonMove
    c.execute('insert into dungeonmove values (1 ,2016,1,1)')
    c.execute('insert into dungeonmove values (2 ,2018,2,2)')
    c.execute('insert into dungeonmove values (3 ,2019,3,3)')
    c.execute('insert into dungeonmove values (4 ,2017,1,2)')
    c.execute('insert into dungeonmove values (5 ,2018,1,3)')
    conn.commit()
# createDb()

class PersonWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('550x550')
        self.title('Person Insert')
        def select_record(e):
            pid.delete(0, tk.END)
            fname.delete(0, tk.END)
            father.delete(0, tk.END)
            lname.delete(0, tk.END)
            gender.delete(0, tk.END)
            birth.delete(0, tk.END)
            address.delete(0, tk.END)
            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                fname.insert(0, values[1])
                father.insert(0, values[2])
                lname.insert(0, values[3])
                gender.insert(0, values[4])
                birth.insert(0, values[5])
                address.insert(0, values[6])
            except:
                pass
        def tree_view():
            for record in out.get_children():
                out.delete(record)
            c.execute("SELECT rowid, * FROM person")
            records = c.fetchall()
            global count
            count = 0
            for record in records:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                                   values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                                   tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                                   values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                                   tags=('oddrow',))
                count += 1
        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from person where id=:id',{'id': pid.get()})
                    messagebox.showinfo('',f'تم حذف خانة التسلسل'
                                           f'\n {id}')
                except sqlite3.IntegrityError as e:
                    if str(e)=="FOREIGN KEY constraint failed":
                        messagebox.showerror('',f'احذف بيانات الشخص من باقي الجداول أولاً!'
                                                f'\n{e}')
                    else:
                        messagebox.showerror('',f'خطأ'
                                                f'\n{e}')
            else:
                messagebox.showerror('','الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            tree_view()
        def insert():
            id, firstName, fath, lastName, gend, birthYear, addr = \
                pid.get(), fname.get(), father.get(), lname.get(), gender.get(), birth.get(), address.get()
            if id.isdigit() and birthYear.isdigit():
                with conn:
                    try:
                        c.execute('insert into person values (:id , :first,:father, :last,:gender ,:birth,:address)',
                                  {'id': id, 'first': firstName, 'father': fath, 'last': lastName,
                                   'gender': gend, 'birth': birthYear, 'address': addr})
                        messagebox.showinfo('','تمت إضافة خانة')

                    except sqlite3.IntegrityError as e:
                        messagebox.showerror('',' يجب أن يكون الرقم التسلسلي\n غير مكرر')

            else:
                messagebox.showerror('','يجب إدخال رقم في خانة الرقم \nالتسلسلي و تاريخ الميلاد')
            conn.commit()
            tree_view()
        def update_rec():
            c.execute("""UPDATE person SET
            		firstname = :first,
            		lastname = :last,
            		father = :father,
            		gender = :gender,
            		birthyear = :birth,
            		address = :address
            		WHERE id = :pid""",
                      {
                          'first': fname.get(),
                          'last': lname.get(),
                          'gender': gender.get(),
                          'father': father.get(),
                          'birth': birth.get(),
                          'address': address.get(),
                          'pid': pid.get(),
                      })
            pid.delete(0, tk.END)
            fname.delete(0, tk.END)
            father.delete(0, tk.END)
            lname.delete(0, tk.END)
            gender.delete(0, tk.END)
            birth.delete(0, tk.END)
            address.delete(0, tk.END)
            conn.commit()
            tree_view()

        frame = tk.LabelFrame(self, text='إدخال بيانات سجين', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        f_btn=tk.LabelFrame(self,padx=10,pady=10)
        f_btn.grid(padx=10,pady=10)
        inf=tk.LabelFrame(self,text='عرض البيانات', padx=10, pady=10)
        inf.grid(pady=10, padx=10)
        out=tk.ttk.Treeview(inf, selectmode="extended")
        out.grid()
        out['columns']=( "ID","First Name", "Father","Last Name","Gender","Birth","Address")
        out.column("#0", width=0)
        out.column("ID", width=0)
        out.column("First Name",  width=70)
        out.column("Father", width=70)
        out.column("Last Name", width=70)
        out.column("Gender",  width=50)
        out.column("Birth",  width=50)
        out.column("Address", width=100)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("First Name",  text='الاسم')
        out.heading("Father", text='الأب')
        out.heading("Last Name", text='الكنية')
        out.heading("Gender",  text='الجنس')
        out.heading("Birth",  text='الميلاد')
        out.heading("Address", text='العنوان')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        ttk.Label(frame,
                  text="ID").grid(row=0,column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="الاسم الأول").grid(row=1, column=1,padx=10,pady=5)
        ttk.Label(frame,
                  text="اسم الأب").grid(row=1,column=3, padx=10,pady=5)
        ttk.Label(frame,
                  text="الكنية").grid(row=2,column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="الجنس ").grid(row=2,column=3, padx=10,pady=5)
        ttk.Label(frame,
                  text="تاريخ الميلاد").grid(row=3,column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="العنوان").grid(row=3,column=3, padx=10,pady=5)
        pid = ttk.Entry(frame)
        pid.grid(row=0, column=0, padx=10,pady=5)
        fname = ttk.Entry(frame)
        fname.grid(row=1,  padx=10,pady=5)
        father = ttk.Entry(frame)
        father.grid(row=1,column=2, padx=10,pady=5)
        lname = ttk.Entry(frame)
        lname.grid(row=2,column=0,  padx=10,pady=5)
        gender = ttk.Entry(frame)
        gender.grid(row=2,column=2, padx=10,pady=5)
        birth = ttk.Entry(frame)
        birth.grid(row=3,column=0, padx=10,pady=5)
        address = ttk.Entry(frame);
        address.grid(row=3,column=2, padx=10,pady=5)
        ttk.Button(f_btn,
                   text='إدخال',width=15,
                   command=lambda: insert()).grid(row=0, column=0, padx=20,pady=5)
        ttk.Button(f_btn,
                   text='حذف ', width=15,
                   command=lambda: delete()).grid(row=0, column=2, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='عرض البيانات', width=15,
                   command=lambda: (tree_view())).grid(row=0, column=3, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='تعديل البيانات', width=15,
                   command=lambda: (update_rec())).grid(row=0, column=1, padx=10, pady=5)
        tree_view()
class ConvictWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('600x500')
        self.title('Convict Insert')
        def select():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                'SELECT  convicts.rowid,convicts.id , firstname, lastname,convicts.fromdate, convicts.todate,convicts.personid,convicts.offenceid from person INNER JOIN convicts ON person.id= convicts.personid')
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7]),
                               tags=('oddrow',))
                count += 1
        def select_record(e):
            pid.delete(0, tk.END)
            fromdate.delete(0, tk.END)
            todate.delete(0, tk.END)
            personid.delete(0, tk.END)
            offid.delete(0, tk.END)

            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                fromdate.insert(0, values[3])
                todate.insert(0, values[4])
                personid.insert(0, values[5])
                offid.insert(0, values[6])

            except:
                pass
        def customselect():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                'SELECT  convicts.rowid,convicts.id , firstname, lastname,convicts.fromdate, convicts.todate,convicts.personid,convicts.offenceid from person INNER JOIN convicts ON person.id= convicts.personid where fromdate>:fromdate and convicts.todate<:todate',
                {'fromdate': sfrom.get(), 'todate': sto.get()})
            convs = c.fetchall()
            global count
            count=0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                                   values=(conv[1], conv[2], conv[3], conv[4],conv[5],conv[6],conv[7]),
                                   tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                                   values=(conv[1], conv[2], conv[3], conv[4],conv[5],conv[6],conv[7]),
                                   tags=('oddrow',))
                count += 1
        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from convicts where id=:id',{'id': pid.get()})
                    messagebox.showinfo('',f'تم حذف خانة التسلسل'
                                           f'\n{pid.get()}')
                except sqlite3.IntegrityError as e:
                    messagebox.showerror('',f'{e}')
            else:
                messagebox.showerror('','الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()

        def insert():
            self.id, self.fromdate, self.todate, self.personid, self.offid= \
                pid.get(), fromdate.get(), todate.get(), personid.get(), offid.get()
            if self.id.isdigit() and self.fromdate.isdigit() and self.todate.isdigit() and self.personid.isdigit() and self.offid.isdigit():
                with conn:
                    try:
                        c.execute('insert into convicts values (:id , :fromdate,:todate, :convs,:offid )',
                                  {'id': self.id, 'fromdate': self.fromdate, 'todate': self.todate, 'convs': self.personid,
                                   'offid': self.offid})
                        messagebox.showinfo('','تمت إضافة خانة')
                    except sqlite3.IntegrityError as e:
                        if str(e)=='FOREIGN KEY constraint failed':
                            messagebox.showerror('','الرجاء التأكد من تسلسل الشخص/التهمة')
                        if str(e)=='UNIQUE constraint failed: convicts.id':
                            messagebox.showerror('',' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                        else:
                            messagebox.showerror('',f'{e}')


            else:
                messagebox.showerror('','الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def update_rec():
            c.execute("""UPDATE convicts SET
            		fromdate = :fromdate,
            		todate = :todate,
            		personid = :personid,
            		offenceid = :offenceid
            		WHERE id = :pid""",
                      {
                          'fromdate': fromdate.get(),
                          'todate': todate.get(),
                          'personid': personid.get(),
                          'offenceid': offid.get(),
                          'pid': pid.get(),
                      })
            conn.commit()
            select()

        frame = tk.LabelFrame(self, text='إدخال بيانات أحكام', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        btn_frame=tk.LabelFrame(self, padx=10, pady=10)
        btn_frame.grid(padx=5)
        search = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        search.grid(pady=5, padx=5)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="من تاريخ").grid(row=1, column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="إلى تاريخ").grid(row=1, column=3, padx=10,pady=5)
        ttk.Label(frame,
                  text="تسلسل السجين").grid(row=2, column=1, padx=10,pady=5)
        ttk.Label(frame,
                  text="تسلسل الجريمة ").grid(row=2, column=3, padx=10,pady=5)

        pid = ttk.Entry(frame);
        pid.grid(row=0, padx=10,pady=5)
        fromdate = ttk.Entry(frame)
        fromdate.grid(row=1, padx=10,pady=5)
        todate = ttk.Entry(frame);
        todate.grid(row=1,column=2, padx=10,pady=5)
        personid = ttk.Entry(frame);
        personid.grid(row=2, padx=10,pady=5)
        offid = ttk.Entry(frame);
        offid.grid(row=2,column=2, padx=10,pady=5)
        ttk.Button(btn_frame,
                   text='إدخال',
                   command=lambda: insert(),width=20).grid(row=0, column=0, padx=20,pady=5)
        ttk.Button(btn_frame,
                   text='عرض جميع البيانات',width=20,
                   command=lambda: (select())).grid(row=0, column=1, padx=20,pady=5)
        ttk.Button(btn_frame,
                   text='تعديل', width=20,
                   command=lambda: (update_rec())).grid(row=1, column=0, padx=20, pady=5)
        ttk.Label(search,
                  text="من تاريخ").grid(row=0, column=3, padx=10,pady=5)
        ttk.Label(search,
                  text="إلى تاريخ").grid(row=0, column=1, padx=10,pady=5)
        sfrom = ttk.Entry(search);
        sfrom.grid(row=0, column=2,padx=10,pady=5)
        sto = ttk.Entry(search);
        sto.grid(row=0,column=0, padx=20,pady=5)
        ttk.Button(search,
                   text='بـــحـــث',width=20,
                   command=lambda: (customselect())).grid(row=2, column=1, padx=20,pady=5)
        ttk.Button(btn_frame,
                   text='حذف بحسب التسلسل',width=20,
                   command=lambda: (delete())).grid(row=1, column=1, padx=20,pady=5)
        out = tk.ttk.Treeview(search, selectmode="extended")
        out.grid(row=3,columnspan=5)
        out['columns'] = ("ID", "First Name", "Last Name", "from date", "to date", "person id", "offence id")
        out.column("#0", width=0)
        out.column("ID", width=2)
        out.column("First Name", width=70)
        out.column("Last Name", width=70)
        out.column("from date", width=50)
        out.column("to date", width=50)
        out.column("person id", width=100)
        out.column("offence id", width=120)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("First Name", text='الاسم')
        out.heading("from date", text='من تاريخ')
        out.heading("Last Name", text='الكنية')
        out.heading("to date", text='الى تاريخ')
        out.heading("person id", text='تسلسل السجين')
        out.heading("offence id", text='تسلسل التهمة')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=15,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        select()
class OffenceWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('370x500')
        self.title('التهم')
        def select():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                'SELECT rowid, * from offence')
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2]),
                               tags=('oddrow',))
                count += 1
        def select_record(e):
            pid.delete(0, tk.END)
            offname.delete(0, tk.END)

            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                offname.insert(0, values[1])


            except:
                pass
        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from offence where id=:id', {'id': pid.get()})
                    messagebox.showinfo('', f'تم حذف خانة التسلسل'
                                            f'\n{pid.get()}')
                except sqlite3.IntegrityError as e:
                    messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def insert():
            if pid.get().isdigit() :
                with conn:
                    try:
                        c.execute('insert into offence values (:id , :offname)',
                                  {'id': pid.get(), 'offname': offname.get()})
                        messagebox.showinfo('', 'تمت إضافة خانة')
                    except sqlite3.IntegrityError as e:
                        if str(e) == 'FOREIGN KEY constraint failed':
                            messagebox.showerror('', 'الرجاء التأكد من تسلسل الشخص/التهمة')
                        if str(e) == 'UNIQUE constraint failed: convicts.id':
                            messagebox.showerror('', ' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                        else:
                            messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def update_rec():
            c.execute("""UPDATE offence SET
            		name = :offname
            		WHERE id = :pid""",
                      {
                          'pid':pid.get(),
                          'offname': offname.get()
                      })
            conn.commit()
            select()
        frame = tk.LabelFrame(self, text='إدخال بيانات التهم', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        btn_frame = tk.LabelFrame(self, padx=10, pady=10)
        btn_frame.grid(padx=5)
        search = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        search.grid(pady=5, padx=5)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="اسم التهمة").grid(row=1, column=1, padx=10, pady=5)
        pid = ttk.Entry(frame);
        pid.grid(row=0, padx=10, pady=5)
        offname = ttk.Entry(frame)
        offname.grid(row=1, padx=10, pady=5)
        ttk.Button(btn_frame,
                   text='إدخال',
                   command=lambda: insert(), width=20).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='عرض جميع البيانات', width=20,
                   command=lambda: (select())).grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='تعديل', width=20,
                   command=lambda: (update_rec())).grid(row=1, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='حذف بحسب التسلسل', width=20,
                   command=lambda: (delete())).grid(row=1, column=1, padx=20, pady=5)
        out = tk.ttk.Treeview(search, selectmode="extended")
        out.grid(row=3, columnspan=5)
        out['columns'] = ("ID", "Name")
        out.column("#0", width=0)
        out.column("ID", width=50)
        out.column("Name", width=200)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("Name", text='الاسم')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        select()
class VisitWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('600x500')
        self.title('Convict Insert')

        def select():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                '''SELECT visitings.rowid,visitings.id, firstname, lastname,visitings.visitorname, visitings.datevisited,person.id,visitings.mountainminutes from person INNER JOIN visitings ON
                  person.id= visitings.personid''')
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5],conv[6],conv[7]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5],conv[6],conv[7]),
                               tags=('oddrow',))
                count += 1
        def select_record(e):
            pid.delete(0, tk.END)
            vdate.delete(0, tk.END)
            vname.delete(0, tk.END)
            personid.delete(0, tk.END)
            vtime.delete(0, tk.END)

            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                vdate.insert(0, values[4])
                vname.insert(0, values[3])
                personid.insert(0, values[5])
                vtime.insert(0, values[6])

            except:
                pass
        def customselect():
            for inf in out.get_children():
                out.delete(inf)
            c.execute('''SELECT visitings.rowid,visitings.id, firstname, lastname,visitings.visitorname, visitings.datevisited,person.id,visitings.mountainminutes from person INNER JOIN visitings ON
                  person.id= visitings.personid where datevisited between :fdate and :todate''',
                      {'fdate': sfrom.get(), 'todate': sto.get()})
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7]),
                               tags=('oddrow',))
                count += 1
        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from visitings where id=:id', {'id': pid.get()})
                    messagebox.showinfo('', f'تم حذف خانة التسلسل'
                                            f'\n{pid.get()}')
                except sqlite3.IntegrityError as e:
                    messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def insert():
            if pid.get().isdigit() and vdate.get().isdigit() and personid.get().isdigit() :
                with conn:
                    try:
                        c.execute('insert into visitings values (:id , :vdate,:person ,:vname,:vtime )',
                                  {'id': pid.get(), 'vdate': vdate.get(),'person':personid.get(), 'vname': vname.get(),
                                   'vtime': vtime.get()})
                        messagebox.showinfo('', 'تمت إضافة خانة')
                    except sqlite3.IntegrityError as e:
                        if str(e) == 'FOREIGN KEY constraint failed':
                            messagebox.showerror('', 'الرجاء التأكد من تسلسل الشخص/التهمة')
                        if str(e) == 'UNIQUE constraint failed: convicts.id':
                            messagebox.showerror('', ' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                        else:
                            messagebox.showerror('', f'{e}')


            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def update_rec():
            with conn:
                try:
                    c.execute("""UPDATE visitings SET
                            datevisited = :vdate,
                            visitorname = :vname,
                            personid = :personid,
                            mountainminutes = :time
                            WHERE id = :pid""",
                              {
                                  'vdate': vdate.get(),
                                  'vname': vname.get(),
                                  'personid': personid.get(),
                                  'time': vtime.get(),
                                  'pid': pid.get(),
                              })
                except sqlite3.IntegrityError as e:
                    if str(e) == 'FOREIGN KEY constraint failed':
                        messagebox.showerror('', 'الرجاء التأكد من تسلسل الشخص/التهمة')
                    elif str(e) == 'UNIQUE constraint failed: convicts.id':
                        messagebox.showerror('', ' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                    else:
                        messagebox.showerror('', f'{e}')
            conn.commit()
            select()

        frame = tk.LabelFrame(self, text='إدخال بيانات زيارات', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        btn_frame = tk.LabelFrame(self, padx=10, pady=10)
        btn_frame.grid(padx=5)
        search = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        search.grid(pady=5, padx=5)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="تاريخ الزيارة").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="تسلسل السجين").grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="اسم الزائر").grid(row=1, column=3, padx=10, pady=5)
        ttk.Label(frame,
                  text="مدة الزيارة ").grid(row=2, column=3, padx=10, pady=5)

        pid = ttk.Entry(frame);
        pid.grid(row=0, padx=10, pady=5)
        vdate = ttk.Entry(frame)
        vdate.grid(row=1, padx=10, pady=5)
        vname = ttk.Entry(frame);
        vname.grid(row=1, column=2, padx=10, pady=5)
        personid = ttk.Entry(frame);
        personid.grid(row=2, padx=10, pady=5)
        vtime = ttk.Entry(frame);
        vtime.grid(row=2, column=2, padx=10, pady=5)
        ttk.Button(btn_frame,
                   text='إدخال',
                   command=lambda: insert(), width=20).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='عرض جميع البيانات', width=20,
                   command=lambda: (select())).grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='تعديل', width=20,
                   command=lambda: (update_rec())).grid(row=1, column=0, padx=20, pady=5)
        ttk.Label(search,
                  text="من تاريخ").grid(row=0, column=3, padx=10, pady=5)
        ttk.Label(search,
                  text="إلى تاريخ").grid(row=0, column=1, padx=10, pady=5)
        sfrom = ttk.Entry(search);
        sfrom.grid(row=0, column=2, padx=10, pady=5)
        sto = ttk.Entry(search);
        sto.grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(search,
                   text='بـــحـــث', width=20,
                   command=lambda: (customselect())).grid(row=2, column=1, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='حذف بحسب التسلسل', width=20,
                   command=lambda: (delete())).grid(row=1, column=1, padx=20, pady=5)
        out = tk.ttk.Treeview(search, selectmode="extended")
        out.grid(row=3, columnspan=5)
        out['columns'] = ("ID", "First Name", "Last Name",  "vname","Date", "person id", "Vtime")
        out.column("#0", width=0)
        out.column("ID", width=2)
        out.column("First Name", width=70)
        out.column("Last Name", width=70)
        out.column("Date", width=50)
        out.column("vname", width=50)
        out.column("person id", width=100)
        out.column("Vtime", width=120)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("First Name", text='اسم السجين')
        out.heading("Date", text='التاريخ')
        out.heading("Last Name", text='الكنية')
        out.heading("vname", text='اسم الزائر')
        out.heading("person id", text='تسلسل السجين')
        out.heading("Vtime", text='المدة')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=15,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        select()
class DungeonWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('370x500')
        self.title('الزنازين')

        def select():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                'SELECT rowid, * from dungeon')
            dungs = c.fetchall()
            global count
            count = 0
            for dung in dungs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(dung[1], dung[2], dung[3]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(dung[1], dung[2], dung[3]),
                               tags=('oddrow',))
                count += 1
        def select_record(e):
            pid.delete(0, tk.END)
            offname.delete(0, tk.END)
            size.delete(0,tk.END)

            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                offname.insert(0, values[1])
                size.insert(0, values[2])



            except:
                pass
        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from dungeon where id=:id', {'id': pid.get()})
                    messagebox.showinfo('', f'تم حذف خانة التسلسل'
                                            f'\n{pid.get()}')
                except sqlite3.IntegrityError as e:
                    messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def insert():
            if pid.get().isdigit():
                with conn:
                    try:
                        c.execute('insert into dungeon values (:id , :offname,:size)',
                                  {'id': pid.get(), 'offname': offname.get(), 'size': size.get()})
                        messagebox.showinfo('', 'تمت إضافة خانة')
                    except sqlite3.IntegrityError as e:
                        if str(e) == 'FOREIGN KEY constraint failed':
                            messagebox.showerror('', 'الرجاء التأكد من تسلسل الشخص/التهمة')
                        if str(e) == 'UNIQUE constraint failed: convicts.id':
                            messagebox.showerror('', ' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                        else:
                            messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def update_rec():
            c.execute("""UPDATE dungeon SET
                    name = :offname,
                    size=:size
                    WHERE id = :pid
                    """,
                      {
                          'pid': pid.get(),
                          'offname': offname.get(),
                          'size': size.get()
                      })
            conn.commit()
            select()
        frame = tk.LabelFrame(self, text='إدخال بيانات الزنازين', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        btn_frame = tk.LabelFrame(self, padx=10, pady=10)
        btn_frame.grid(padx=5)
        search = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        search.grid(pady=5, padx=5)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="اسم الزنزانة").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="الحجم").grid(row=2, column=1, padx=10, pady=5)
        pid = ttk.Entry(frame);
        pid.grid(row=0, padx=10, pady=5)
        offname = ttk.Entry(frame)
        offname.grid(row=1, padx=10, pady=5)
        size = ttk.Entry(frame)
        size.grid(row=2, padx=10, pady=5)
        ttk.Button(btn_frame,
                   text='إدخال',
                   command=lambda: insert(), width=20).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='عرض جميع البيانات', width=20,
                   command=lambda: (select())).grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='تعديل', width=20,
                   command=lambda: (update_rec())).grid(row=1, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='حذف بحسب التسلسل', width=20,
                   command=lambda: (delete())).grid(row=1, column=1, padx=20, pady=5)
        out = tk.ttk.Treeview(search, selectmode="extended")
        out.grid(row=3, columnspan=5)
        out['columns'] = ("ID", "Name", "size")
        out.column("#0", width=0)
        out.column("ID", width=50)
        out.column("Name", width=100)
        out.column("size", width=100)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("Name", text='الاسم')
        out.heading("size", text='الحجم')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        select()
class DungeonMove(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('600x600')
        self.title('الانتقالات')
        def customselect():
            for inf in out.get_children():
                out.delete(inf)
            c.execute('SELECT dungeonmove.rowid,dungeonmove.id,dungeonmove.fromdate,dungeonmove.personid,dungeonmove.dungeonid, firstname, lastname from person INNER JOIN dungeonmove ON person.id= dungeonmove.personid where person.id=:personid',{'personid':sperson.get()})
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6]),
                               tags=('oddrow',))
                count += 1
        def select():
            for inf in out.get_children():
                out.delete(inf)
            c.execute(
                '''SELECT dungeonmove.rowid,dungeonmove.id,dungeonmove.fromdate,dungeonmove.personid,dungeonmove.dungeonid, firstname, lastname from person INNER JOIN dungeonmove ON person.id= dungeonmove.personid''')
            convs = c.fetchall()
            global count
            count = 0
            for conv in convs:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(conv[1], conv[2], conv[3], conv[4], conv[5], conv[6]),
                               tags=('oddrow',))
                count += 1

        def select_record(e):
            pid.delete(0, tk.END)
            date.delete(0, tk.END)
            dungid.delete(0, tk.END)
            personid.delete(0, tk.END)
            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                date.insert(0, values[1])
                dungid.insert(0, values[3])
                personid.insert(0, values[2])
            except:
                pass

        def delete():
            if pid.get().isdigit():
                try:
                    c.execute('delete from dungeon where id=:id', {'id': pid.get()})
                    messagebox.showinfo('', f'تم حذف خانة التسلسل'
                                            f'\n{pid.get()}')
                except sqlite3.IntegrityError as e:
                    messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def insert():
            if pid.get().isdigit():
                with conn:
                    try:
                        c.execute('insert into dungeonmove values (:id , :date,:personid,:dungid)',
                                  {'id': pid.get(), 'date': date.get(),'personid':personid.get(), 'dungid': dungid.get()})
                        messagebox.showinfo('', 'تمت إضافة خانة')
                    except sqlite3.IntegrityError as e:
                        if str(e) == 'FOREIGN KEY constraint failed':
                            messagebox.showerror('', 'الرجاء التأكد من تسلسل الشخص/التهمة')
                        if str(e) == 'UNIQUE constraint failed: convicts.id':
                            messagebox.showerror('', ' يجب أن يكون الرقم التسلسلي\n غير مكرر')
                        else:
                            messagebox.showerror('', f'{e}')
            else:
                messagebox.showerror('', 'الرجاء إدخال بيانات رقمية وليس نص')
            conn.commit()
            select()
        def update_rec():
            c.execute("""UPDATE dungeonmove SET
                    fromdate = :date,
                    dungeonid=:dungid,
                    personid=:person
                    
                    WHERE id = :pid
                    """,
                      {
                          'pid': pid.get(),
                          'date': date.get(),
                          'dungid': dungid.get(),
                          'person':personid.get()
                      })
            conn.commit()
            select()

        frame = tk.LabelFrame(self, text='إدخال بيانات الانتقالات', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        btn_frame = tk.LabelFrame(self, padx=10, pady=10)
        btn_frame.grid(padx=5)
        search = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        search.grid(pady=5, padx=5)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="التاريخ").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="تسلسل الزنزانة").grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="تسلسل السجين").grid(row=3, column=1, padx=10, pady=5)
        pid = ttk.Entry(frame)
        pid.grid(row=0, padx=10, pady=5)
        date = ttk.Entry(frame)
        date.grid(row=1, padx=10, pady=5)
        dungid = ttk.Entry(frame)
        dungid.grid(row=2, padx=10, pady=5)
        personid = ttk.Entry(frame)
        personid.grid(row=3, padx=10, pady=5)
        ttk.Label(search,
                  text="تسلسل السجين").grid(row=0, column=2, padx=10, pady=5)
        sperson = ttk.Entry(search);
        sperson.grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(search,
                   text='بحث مخصص', width=20,
                   command=lambda: (customselect())).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='إدخال',
                   command=lambda: insert(), width=20).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='عرض جميع البيانات', width=20,
                   command=lambda: (select())).grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='تعديل', width=20,
                   command=lambda: (update_rec())).grid(row=1, column=0, padx=20, pady=5)
        ttk.Button(btn_frame,
                   text='حذف بحسب التسلسل', width=20,
                   command=lambda: (delete())).grid(row=1, column=1, padx=20, pady=5)
        out = tk.ttk.Treeview(search, selectmode="extended")
        out.grid(row=3, columnspan=5)
        out['columns'] = ("ID","Date", "personid", "dungid","Name","LastName")
        out.column("#0", width=0)
        out.column("ID", width=50)
        out.column("Date", width=100)
        out.column("dungid", width=100)
        out.column("personid", width=100)
        out.column("Name", width=100)
        out.column("LastName", width=100)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("Date", text='date')
        out.heading("dungid", text='تسلسل الزنزانة')
        out.heading("personid", text='تسلسل السجين')
        out.heading("Name", text='اسم السجين')
        out.heading("LastName", text='الكنية')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        select()

class Charges(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('550x400')
        self.title('Charges Insert')

        def tree_view():
            for record in out.get_children():
                out.delete(record)
            c.execute('''SELECT offence.rowid,offence.id,offence.name,firstname,father, lastname,gender,birthyear,address from person,offence INNER JOIN convicts ON
              person.id= convicts.personid where offence.id=convicts.offenceid''')
            records = c.fetchall()
            global count
            count = 0
            for record in records:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3], record[4], record[5],record[6],record[7],record[8]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3], record[4], record[5],record[6],record[7],record[8]),
                               tags=('oddrow',))
                count += 1

        def custom_select():
            for record in out.get_children():
                out.delete(record)
            c.execute('''SELECT offence.rowid,offence.id,offence.name,firstname,father, lastname,gender,birthyear,address from person,offence INNER JOIN convicts ON
                     person.id= convicts.personid where offenceid=:offid and offence.id=convicts.offenceid''',
                      {'offid': offid.get()})
            records = c.fetchall()
            global count
            count = 0
            for record in records:
                if count % 2 == 0:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(
                               record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                               tags=('evenrow',))
                else:
                    out.insert(parent='', index='end', iid=count, text='',
                               values=(
                               record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                               tags=('oddrow',))
                count += 1
        f_btn = tk.LabelFrame(self, padx=10, pady=10)
        f_btn.grid(padx=10, pady=10)
        inf = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        inf.grid(pady=10, padx=10)
        out = tk.ttk.Treeview(inf, selectmode="extended")
        out.grid()
        out['columns'] = ("ID", "charge", "First Name", "Father", "Last Name", "Gender", "Birth", "Address")
        out.column("#0", width=0)
        out.column("ID", width=0)
        out.column("charge", width=70)
        out.column("First Name", width=70)
        out.column("Father", width=70)
        out.column("Last Name", width=70)
        out.column("Gender", width=50)
        out.column("Birth", width=50)
        out.column("Address", width=100)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("charge", text='التهمة')
        out.heading("First Name", text='الاسم')
        out.heading("Father", text='الأب')
        out.heading("Last Name", text='الكنية')
        out.heading("Gender", text='الجنس')
        out.heading("Birth", text='الميلاد')
        out.heading("Address", text='العنوان')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        tk.Label(f_btn,text='تسلسل الجريمة').grid(row=0,column=1)
        offid = ttk.Entry(f_btn)
        offid.grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='عرض البيانات', width=15,
                   command=lambda: (tree_view())).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='بحث مخصص', width=15,
                   command=lambda: (custom_select())).grid(row=1, column=1, padx=10, pady=5)
        tree_view()

class FileManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.file='Fdb.txt'
        self.geometry('550x550')
        self.title('File Manager')
        def select_record(e):
            pid.delete(0, tk.END)
            fname.delete(0, tk.END)
            father.delete(0, tk.END)
            lname.delete(0, tk.END)
            gender.delete(0, tk.END)
            birth.delete(0, tk.END)
            address.delete(0, tk.END)
            selected = out.focus()
            values = out.item(selected, 'values')
            try:
                pid.insert(0, values[0])
                fname.insert(0, values[1])
                father.insert(0, values[2])
                lname.insert(0, values[3])
                gender.insert(0, values[4])
                birth.insert(0, values[5])
                address.insert(0, values[6])
            except:
                pass
        def tree_view():
            lst = []
            with open(self.file, 'r') as f:

                for line in f:
                    ls = line.strip().split(',')
                    lst.append(ls)
            for record in out.get_children():
                out.delete(record)
            global count
            count = 0
            for record in lst:
                if len(record)>6:
                    if count % 2 == 0:
                        out.insert(parent='', index='end', iid=count, text='',
                                   values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6]),
                                   tags=('evenrow',))
                    else:
                        out.insert(parent='', index='end', iid=count, text='',
                                   values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6]),
                                   tags=('oddrow',))
                    count += 1

        def delete():
            with open(self.file, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i[0] != pid.get():
                        f.write(i)
                f.truncate()
            tree_view()

        def insert():
            lst=[pid.get(), fname.get(), father.get(), lname.get(), gender.get(), birth.get(), address.get()]
            ins = ','
            ins = ins.join(lst)
            with open(self.file, 'a') as f:
                f.write(f'\n{ins}')
            tree_view()

        def update_rec():
            with open(self.file, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i[0] != pid.get():
                        f.write(i)
                f.truncate()
            lst = [pid.get(), fname.get(), father.get(), lname.get(), gender.get(), birth.get(), address.get()]
            ins = ','
            ins = ins.join(lst)
            with open(self.file, 'a') as f:
                f.truncate()
                f.write(f'\n{ins}')
            tree_view()
            pid.delete(0, tk.END)
            fname.delete(0, tk.END)
            father.delete(0, tk.END)
            lname.delete(0, tk.END)
            gender.delete(0, tk.END)
            birth.delete(0, tk.END)
            address.delete(0, tk.END)
            tree_view()

        frame = tk.LabelFrame(self, text='إدخال بيانات سجين', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        f_btn = tk.LabelFrame(self, padx=10, pady=10)
        f_btn.grid(padx=10, pady=10)
        inf = tk.LabelFrame(self, text='عرض البيانات', padx=10, pady=10)
        inf.grid(pady=10, padx=10)
        out = tk.ttk.Treeview(inf, selectmode="extended")
        out.grid()
        out['columns'] = ("ID", "First Name", "Father", "Last Name", "Gender", "Birth", "Address")
        out.column("#0", width=0)
        out.column("ID", width=0)
        out.column("First Name", width=70)
        out.column("Father", width=70)
        out.column("Last Name", width=70)
        out.column("Gender", width=50)
        out.column("Birth", width=50)
        out.column("Address", width=100)
        out.heading("#0", text='')
        out.heading("ID", text='ID')
        out.heading("First Name", text='الاسم')
        out.heading("Father", text='الأب')
        out.heading("Last Name", text='الكنية')
        out.heading("Gender", text='الجنس')
        out.heading("Birth", text='الميلاد')
        out.heading("Address", text='العنوان')
        style = ttk.Style()
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3")
        style.map('Treeview',
                  background=[('selected', saved_highlight_color)])
        out.tag_configure('oddrow', background=saved_secondary_color)
        out.tag_configure('evenrow', background=saved_primary_color)
        out.bind("<ButtonRelease-1>", select_record)
        ttk.Label(frame,
                  text="ID").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="الاسم الأول").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="اسم الأب").grid(row=1, column=3, padx=10, pady=5)
        ttk.Label(frame,
                  text="الكنية").grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="الجنس ").grid(row=2, column=3, padx=10, pady=5)
        ttk.Label(frame,
                  text="تاريخ الميلاد").grid(row=3, column=1, padx=10, pady=5)
        ttk.Label(frame,
                  text="العنوان").grid(row=3, column=3, padx=10, pady=5)
        pid = ttk.Entry(frame)
        pid.grid(row=0, column=0, padx=10, pady=5)
        fname = ttk.Entry(frame)
        fname.grid(row=1, padx=10, pady=5)
        father = ttk.Entry(frame)
        father.grid(row=1, column=2, padx=10, pady=5)
        lname = ttk.Entry(frame)
        lname.grid(row=2, column=0, padx=10, pady=5)
        gender = ttk.Entry(frame)
        gender.grid(row=2, column=2, padx=10, pady=5)
        birth = ttk.Entry(frame)
        birth.grid(row=3, column=0, padx=10, pady=5)
        address = ttk.Entry(frame);
        address.grid(row=3, column=2, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='إدخال', width=15,
                   command=lambda: insert()).grid(row=0, column=0, padx=20, pady=5)
        ttk.Button(f_btn,
                   text='حذف ', width=15,
                   command=lambda: delete()).grid(row=0, column=2, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='عرض البيانات', width=15,
                   command=lambda: (tree_view())).grid(row=0, column=3, padx=10, pady=5)
        ttk.Button(f_btn,
                   text='تعديل البيانات', width=15,
                   command=lambda: (update_rec())).grid(row=0, column=1, padx=10, pady=5)
        tree_view()
class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('600x400')
        self.title('مشروع السجن')

        frame=tk.LabelFrame(self, text='قواعد البيانات', padx=10, pady=10)
        frame.pack()
        files = tk.LabelFrame(self, text='إدارة الملفات', padx=10, pady=10)
        files.pack()
        ttk.Button(frame,
                   text=' بيانات السجناء',
                   command=self.open_personinsert,width=40).grid(row=0,pady=5,padx=5)
        ttk.Button(frame,
                   text=' بيانات الأحكام',width=40,
                   command=self.open_convictinsert).grid(row=0,column=1,pady=5,padx=5)
        ttk.Button(frame,
                   text='بيانات التهم',width=40,
                   command=self.open_offenceinsert).grid(row=1,column=0,pady=5,padx=5)
        ttk.Button(frame,
                   text='بيانات الزيارات',width=40,
                   command=self.open_visitinsert).grid(row=1,column=1,pady=5,padx=5)
        ttk.Button(frame,
                   text='بيانات الزنزانين',width=40,
                   command=self.open_dungeoninsert).grid(row=2,pady=5,padx=5)
        ttk.Button(frame,
                   text=' بيانات انتقال الزنازين',width=40,
                   command=self.open_dungeonminsert).grid(row=2,column=1,pady=5,padx=5)
        ttk.Button(frame,
                   text='الجرائم',width=40,
                   command=self.open_charge).grid(row=3,columnspan=2,pady=5,padx=5)
        ttk.Button(files,
                   text='مدير الملفات', width=40,
                   command=self.open_file).grid(row=3, columnspan=2, pady=5, padx=5)

    def open_personinsert(self):
            window = PersonWindow(self)
            window.grab_set()
    def open_convictinsert(self):
            window = ConvictWindow(self)
            window.grab_set()
    def open_offenceinsert(self):
            window = OffenceWindow(self)
            window.grab_set()
    def open_visitinsert(self):
            window = VisitWindow(self)
            window.grab_set()
    def open_dungeoninsert(self):
            window = DungeonWindow(self)
            window.grab_set()
    def open_dungeonminsert(self):
            window = DungeonMove(self)
            window.grab_set()
    def open_charge(self):
            window = Charges(self)
            window.grab_set()
    def open_file(self):
        window = FileManager(self)
        window.grab_set()
    def open_window(self):
            window = PersonWindow(self)
            window.grab_set()
class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)



# app = App()
App().mainloop()
# if __name__ == "__main__":
#
#     app = App()
#     app.mainloop()
