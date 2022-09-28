import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import pyarabic.number as number
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from warnings import filterwarnings
from tkinter import messagebox

db = sqlite3.connect('flats.db')
cur = db.cursor()


def print_invoice():
    # ========================  Create a database ========================
    connection = sqlite3.connect('flats.db')
    cursor = connection.cursor()
    # ==================== Create PDF ====================
    pdf = FPDF()
    pdf = FPDF('L', 'mm', (105, 148))
    pdf.set_margins(0, 0, 0)
    # ==================== set Font ====================
    pdf.add_font("NotoSansArabic", style="",
                 fname="alfont_com_AlFont_com_arialbd.ttf", uni=True)
    # pdf.add_font("NotoSansArabic", style="",
    #                fname="alfont_com_Sane-Font.ttf", uni = True)
    pdf.set_font('NotoSansArabic', '', 14)
    # =============== Fix font ===================

    def fix_arabic(text):
        return get_display(reshape(text))
    # ================== read vars =================
    a = cmb1.get()
    month = a
    # =============== make a page =================
    for i in range(0, 39):
        if i != 2:
            # flat = (str(int(i/4)) + str(i % 4+1))  # get flat no
            cursor.execute('select * from flats')
            a = cursor.fetchall()
            owner = (a[i][1])
            flat = (a[i][0])
            money = (a[i][2])
            pdf.add_page()
            pdf.text(101, 20, fix_arabic('اتحاد ملاك العمارة'))
            pdf.text(86, 27, fix_arabic('رقم 22 عمارات المهندسين'))
            pdf.text(90, 34, fix_arabic('رابعة العدوية مدينة نصر'))
            pdf.text(90, 50, fix_arabic('استلمت انا : سامى فهمى'))
            pdf.text(111, 60, fix_arabic('من السيد : '))
            pdf.text(55, 60, fix_arabic(owner).center(30, "."))
            pdf.text(20, 60, fix_arabic(' مالك الشقة رقم : '))
            pdf.text(15, 60, flat)
            pdf.text(117, 70, fix_arabic('المبلغ : '))
            pdf.text(95, 70, fix_arabic('  جنيه ')+str(money))
            pdf.text(15, 70, (fix_arabic(" جنية فقط لاغير ") +
                              fix_arabic(number.number2text(money))).center(40, "*"))
            pdf.text(73, 80, fix_arabic('وذلك نظير اعمال الصيانة عن شهر '))
            pdf.text(63, 80, fix_arabic(month))
            pdf.text(20, 90, fix_arabic('مأمور العمارة'))
            pdf.rect(.5, .5, 147.5, 104.5, 'D')

    filterwarnings('ignore')
    pdf.output('INVOICES.pdf')
    filterwarnings('default')
    lbl1 = ttk.Label(root, text="تم الطباعة", font=60, foreground="red")
    lbl1.place(x=750, y=450)


root = tk.Tk()
root.title(" نظام طباعةالفواتير اصدار 1.0.0")
root.geometry("900x850" + "+0+0")
flat = tk.IntVar()
name = tk.IntVar()
money = tk.IntVar()
# ================ logo =================
logo = tk.PhotoImage(file="logo.png")
lbl_logo = ttk.Label(root, image=logo).place(x=530, y=5)
# =============================================
lbl1 = ttk.Label(root, text="الشقة", font=14).place(x=800, y=210)
lbl2 = ttk.Label(root, text="المالك", font=14).place(x=800, y=260)
lbl3 = ttk.Label(root, text="المبلغ", font=14).place(x=800, y=310)
lbl4 = ttk.Label(root, text="الشهر", font=14).place(x=800, y=360)

entry1 = ttk.Entry(root, textvariable=flat, font=14, justify='right')
entry1.place(x=550, y=210)
entry2 = ttk.Entry(root, textvariable=name, font=14, justify='right')
entry2.place(x=550, y=260)
entry3 = ttk.Entry(root, textvariable=money, font=14, justify='right')
entry3.place(x=550, y=310)
cmb1 = ttk.Combobox(root, values=["يناير", "فبراير", "مارس", "ابريل", "مايو",
                    "يونيو", "يوليو", "اغسطس", "سبتمبر", "اكتوبر", "نوفمبر", "ديسمبر"], font=14)
cmb1.place(x=550, y=360)
# tr = ttk.Treeview(root, columns=("flat", "name", "money"), show='headings')
tr = ttk.Treeview(root, columns=("الشقة", "المالك", "المبلغ"), show="headings")
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 14),
                foreground="navy", background="red")
tr.tag_configure('الشقة', background='azure')
tr.heading("الشقة", text="الشقة", anchor="center")
tr.column("الشقة", width=100, anchor="center")
tr.heading("المالك", text="المالك")
tr.column("المالك", width=300, anchor="center")
tr.heading("المبلغ", text="المبلغ")
tr.column("المبلغ", width=100, anchor="center")
tr.place(x=5, y=5, width=500, height=800)


def filltree():
    tr.delete(*tr.get_children())
    cur.execute("SELECT * FROM flats")
    rows = cur.fetchall()
    for row in rows:
        tr.insert("", tk.END, values=row)


def updtdb():
    flat = entry1.get()
    
    if( flat.isnumeric() and flat in ("1", "2", "4")):
       pass
    else:
        messagebox.showerror("خطأ", "يجب ادخال رقم الشقة بشكل صحيح")
        return
    

    name = entry2.get()
    money = entry3.get()
    cur.execute("""UPDATE flats
                    SET NAME = (?), value = (?)
                    WHERE FLAT =(?)""", (name, money, flat,))
    cur.execute("""commit""")
    filltree()


filltree()
btn = tk.Button(root, text="تحديث البيانات", font=14, command=updtdb)
btn.place(x=550, y=400, width=150, height=50)
btn = tk.Button(root, text="طباعة الايصالات", font=14, command=print_invoice)
btn.place(x=720, y=400, width=150, height=50)
root.mainloop()
