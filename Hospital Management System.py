import mysql.connector as m
from tkinter import *
from tkinter import messagebox,ttk
from PIL import ImageTk,Image
import datetime

mycon=m.connect(host='localhost',user='root',passwd='MyMySql',database='miniproject')
if mycon.is_connected():
    print('Connected')


cursor=mycon.cursor() #creates cursor
cursor.execute('select * from patient')
data_pat=cursor.fetchall() #holds data in the form of list of tuples
cursor.execute('select * from doctor')
data_doc=cursor.fetchall()
cursor.execute('select * from admin')
data_adm=cursor.fetchall()

#mycon.close()

#holds all data

root=Tk()

img1=Image.open(r'C:\Python mini proj\doc.png')
img2=Image.open(r'C:\Python mini proj\admin.png')
img3=Image.open(r'C:\Python mini proj\patient.png')
img4=Image.open(r'C:\Python mini proj\back.png')
n1_img=img1.resize((100,100))
n2_img=img2.resize((100,100))
n3_img=img3.resize((100,100))
n4_img=img4.resize((60,30))
pic1=ImageTk.PhotoImage(n1_img)
pic2=ImageTk.PhotoImage(n2_img)
pic3=ImageTk.PhotoImage(n3_img)
pic4=ImageTk.PhotoImage(n4_img)

head_label=Label(root,text='Salus Hospitals',font=('Britannic Bold',30,'underline'),background='#8B8B7D',foreground='#F5F5F5')
head_label.pack(padx=20,pady=20)
#Creating parameter buttons
def clear(keep_root,keep_frame=()):
    for widget_root in root.winfo_children():
        if widget_root.winfo_class()== 'Frame':
            for widget_frame in widget_root.winfo_children():
                if widget_frame not in keep_frame:
                    widget_frame.destroy()
        if widget_root not in keep_root:
            widget_root.destroy()
def back(w,x,y,z=()):
    clear(y,z)
    w(x)
    
def after_login(user):
    clear((head_label,))
    root.title('Main page')
    frame3=Frame(root,bg='#8B8B7D');frame3.pack()
    welcome_label=Label(frame3,text='Welcome'+' '+password+'            ',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5')
    welcome_label.grid(row=1,column=0)#cannot ue grid in prev line itelf caue it give None type
    logout_bt=Button(frame3,text='Logout',font=('Lucida Bright',10),background='#8B8B7D',foreground='#F5F5F5',command=lambda:back(page,user,(head_label,)))
    logout_bt.grid(row=1,column=20)#cannot ue grid in prev line itelf caue it give None type

    
    if user=='Doctor Login':
        def operation(op_name):
            if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10)
                        P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def id_fn(P_id):
                            pat_id_under_doc="SELECT Patient_ID FROM doctor WHERE Doctor_ID='{}'".format(username) #only patients under the specific doctor
                            cursor.execute(pat_id_under_doc)
                            pat_id=cursor.fetchall() #list of single element(pat id) tuple
                            #print(pat_id)
                            patient_id=[]
                            for i in pat_id:
                                patient_id.append(i[0])
                                
                            if P_id in patient_id:
                                pat_data="SELECT Diagnosis, Treatment FROM doctor WHERE Patient_ID='{}' AND Doctor_ID='{}'".format(P_id,username) 
                                cursor.execute(pat_data)
                                pat_data=cursor.fetchall()
                                #print(pat_data)

                                if (None, None) in pat_data:
                                    clear((head_label,frame3),(welcome_label,logout_bt))                                   
                                    P_diagnosis_label=Label(frame3,text='Enter diagnosis:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                    P_treatment_label=Label(frame3,text='Enter treatment:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                                    P_diagnosis_entry=Entry(frame3,width=30,borderwidth=10);P_diagnosis_entry.grid(row=2,column=1,pady=10,padx=10)
                                    P_treatment_entry=Entry(frame3,width=30,borderwidth=10);P_treatment_entry.grid(row=4,column=1,pady=10,padx=10)
                                    def upd_diagnosis_and_treatment():
                                        diagnosis=P_diagnosis_entry.get()
                                        treatment=P_treatment_entry.get()
                                        #print(diagnosis,treatment)
                                        upd_in_doc="UPDATE doctor SET Diagnosis='{}', Treatment='{}' WHERE Patient_ID='{}' AND Doctor_ID='{}' AND Diagnosis IS NULL AND Treatment IS NULL ".format(diagnosis,treatment,P_id,username,None,None)
                                        upd_in_pat="UPDATE patient SET Diagnosis='{}', Treatment='{}' WHERE Patient_ID='{}' AND Doctor='{}' AND Diagnosis IS NULL AND Treatment IS NULL".format(diagnosis,treatment,P_id,password,None,None)
                                        cursor.execute(upd_in_doc)
                                        cursor.execute(upd_in_pat)
                                        mycon.commit()
                                        messagebox.showinfo("Update", "Update sucessful!!")
                                        ans = messagebox.askyesno("Next", "update for another patient?")
                                        if ans:
                                            operation(op_name)
                                        else:
                                            after_login(user)
                                    enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=upd_diagnosis_and_treatment)
                                    enter_bt.grid(columnspan=20,padx=10,pady=10)
                                    back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt)))
                                    back_bt.grid(columnspan=20,padx=10,pady=10)
                                else:
                                    messagebox.showerror("ID", " Patient does not have an appointment with you. Try again?")
                                    operation(op_name)
                               
                                
                            else:
                                messagebox.showerror("ID", " Patient does not exist under your domain. Try again?")
                                
                                
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(P_id_entry.get()))        
                        enter_bt.grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(after_login,user,(head_label,frame3),(welcome_label,logout_bt)))
                        back_bt.grid(columnspan=20,padx=10,pady=10)


            #if op_name=='show':

        update_pat_bt=Button(frame3,text='Update Patient Prescription',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
        show_pat_bt=Button(frame3,text='Show Patient List',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()

              
    if user=='Admin Login':
        def adm(update_for):
            if update_for=='doc':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        D_id_label=Label(frame3,text='Enter Doctor ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        D_id_entry=Entry(frame3,width=30,borderwidth=10)
                        D_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        
                        def id_fn(D_id):
                            if D_id in list(set(map(lambda i:i[0],data_doc))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                upd_label=Label(frame3,text='What do you want to update?',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                                def upd1(i):
                                    clear((head_label,frame3),(welcome_label,logout_bt))
                                    if i=='name':
                                        D_name_label=Label(frame3,text='Enter new name:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_name_entry=Entry(frame3,width=30,borderwidth=10);D_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_name():
                                            global data_doc,data_pat
                                            new_name='Dr. '+str(D_name_entry.get())
                                            new_email=str(D_name_entry.get())+'@salus.com'
                                            def getoldname(i):
                                                get_old_name="SELECT Name FROM doctor WHERE Doctor_ID='{}'".format(i,)
                                                cursor.execute(get_old_name)
                                                data=cursor.fetchone()
                                                return data[0]
                                            old_name=str(getoldname(D_id))
                                            print(old_name)
                                            cursor.reset() #to reset as otherise it then fetches n-1 not n records
                                            nom_upd1="UPDATE doctor SET Name='{}' WHERE Doctor_ID='{}'".format(new_name,D_id)
                                            cursor.execute(nom_upd1)
                                            nom_upd_inPat="UPDATE patient SET Doctor='{}' WHERE Doctor='{}'".format(new_name,old_name)
                                            cursor.execute(nom_upd_inPat)
                                            email_upd="UPDATE doctor SET E_mail='{}' WHERE Doctor_ID='{}'".format(new_email,D_id)
                                            cursor.execute(email_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_name).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='age':
                                        D_age_label=Label(frame3,text='Enter new age:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_age_entry=Entry(frame3,width=30,borderwidth=10);D_age_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_age():
                                            global data_doc
                                            new_age=D_age_entry.get()
                                            age_upd="UPDATE doctor SET Age='{}' WHERE Doctor_ID='{}'".format(new_age,D_id)
                                            cursor.execute(age_upd)
                                            mycon.commit()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_age).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='Ph':
                                        D_Ph_label=Label(frame3,text='Enter new Ph No.:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_Ph_entry=Entry(frame3,width=30,borderwidth=10);D_Ph_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_ph():
                                            new_Ph=D_Ph_entry.get()
                                            if len(new_Ph)>10:
                                                messagebox.showerror("ID", " Too many digits in ph no.. Try again?")
                                            else:
                                                global data_doc
                                                ph_upd="UPDATE doctor SET Ph_No='{}' WHERE Doctor_ID='{}'".format(new_Ph,D_id)
                                                cursor.execute(ph_upd)
                                                mycon.commit()
                                                cursor.reset()
                                                cursor.execute('select * from doctor')
                                                data_doc=cursor.fetchall()
                                                messagebox.showinfo("Update", "Update sucessful!!")
                                                id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_ph).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                Name_upd=Button(frame3,text='Name',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('name')).grid()
                                Age_upd=Button(frame3,text='Age',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('age')).grid()
                                Ph_upd=Button(frame3,text='Phone No.',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Ph')).grid()
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(operation,'upd',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                            else:
                                messagebox.showerror("ID", " Wrong ID. Try again?")
                            
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(D_id_entry.get())).grid(row=3,column=3)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                   
                    if op_name=='rem':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        D_id_label=Label(frame3,text='Enter Doctor ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        D_id_entry=Entry(frame3,width=30,borderwidth=10)
                        D_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        RD_name_label=Label(frame3,text='Enter Rep. Doctor Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        RD_name_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        RD_age_label=Label(frame3,text='Enter Rep. Doctor Age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                        RD_age_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_age_entry.grid(row=4,column=1,pady=10,padx=10)
                        RD_ph_label=Label(frame3,text='Enter Rep Doctor Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                        RD_ph_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                        def do():
                            global data_doc, data_pat
                            new_name='Dr. '+str(RD_name_entry.get())
                            new_email=str(RD_name_entry.get())+'@salus.com'
                            new_Ph=RD_ph_entry.get()
                            new_age=RD_age_entry.get()
                            D_id=D_id_entry.get()
                            def getoldname(i):
                                get_old_name="SELECT Name FROM doctor WHERE Doctor_ID='{}'".format(i,)
                                cursor.execute(get_old_name)
                                data=cursor.fetchone()
                                return data[0]
                            old_name=str(getoldname(D_id))
                            nom_upd="UPDATE doctor SET Name='{}' WHERE Doctor_ID='{}'".format(new_name,D_id)
                            email_upd="UPDATE doctor SET E_mail='{}' WHERE Doctor_ID='{}'".format(new_email,D_id)
                            ph_upd="UPDATE doctor SET Ph_No='{}' WHERE Doctor_ID='{}'".format(new_Ph,D_id)
                            age_upd="UPDATE doctor SET Age='{}' WHERE Doctor_ID='{}'".format(new_age,D_id)
                            nom_upd_inPat="UPDATE patient SET Doctor='{}' WHERE Doctor='{}'".format(new_name,old_name)
                            cursor.execute(nom_upd_inPat)
                            cursor.execute(age_upd)
                            cursor.execute(ph_upd)
                            cursor.execute(nom_upd)
                            cursor.execute(email_upd)
                            mycon.commit()
                            cursor.reset()
                            cursor.execute('select * from doctor')
                            data_doc=cursor.fetchall()
                            cursor.reset()
                            cursor.execute('select * from patient')
                            data_pat=cursor.fetchall()
                            messagebox.showinfo("Update", "Update sucessful!!")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=do).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                    if op_name=='add':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        ND_id_label=Label(frame3,text='Enter Doctor ID to add:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        ND_id_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        ND_name_label=Label(frame3,text='Enter New Doctor Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        ND_name_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        ND_age_label=Label(frame3,text='Enter New Doctor Age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                        ND_age_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_age_entry.grid(row=4,column=1,pady=10,padx=10)
                        ND_ph_label=Label(frame3,text='Enter New Doctor Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                        ND_ph_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                        ND_dept_label=Label(frame3,text='Enter New Doctor Specl.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=6,column=0,pady=10,padx=10)
                        ND_dept_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_dept_entry.grid(row=6,column=1,pady=10,padx=10)
                        
                        def add():
                            global data_doc
                            new_name='Dr. '+str(ND_name_entry.get())
                            new_email=str(ND_name_entry.get())+'@salus.com'
                            new_Ph=ND_ph_entry.get()
                            new_age=ND_age_entry.get()
                            new_dept=ND_dept_entry.get()
                            D_id=ND_id_entry.get()
                            if D_id not in list(set(map(lambda i:i[0],data_doc))):
                                new_upd="INSERT INTO doctor(Doctor_ID,Name,Age,Specialisation,Ph_No,E_mail)  VALUES('{}','{}','{}','{}','{}','{}')".format(D_id,new_name,new_age,new_dept,new_Ph,new_email)
                                cursor.execute(new_upd)
                                mycon.commit()
                                cursor.reset()
                                cursor.execute('select * from doctor')
                                data_doc=cursor.fetchall()
                                messagebox.showinfo("Update", "Addition of doctor sucessful!!")
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                    #HO
                update_doc=Button(frame3,text='Update Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
                remove_doc=Button(frame3,text='Remove Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem')).grid()
                insert_doc=Button(frame3,text='Add Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add')).grid()
                show_bt=Button(frame3,text='Show Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(after_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                
            if update_for=='pat':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10);P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def id_fn(P_id):
                            global data_pat
                            if P_id in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                upd_label=Label(frame3,text='What do you want to update?',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                                def upd1(i):
                                    clear((head_label,frame3),(welcome_label,logout_bt))
                                    if i=='name':
                                        P_name_label=Label(frame3,text='Enter new name:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_name_entry=Entry(frame3,width=30,borderwidth=10);P_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_name():
                                            global data_doc,data_pat
                                            new_name=str(P_name_entry.get())
                                            nom_upd_in_Pat="UPDATE patient SET Name='{}' WHERE Patient_ID='{}'".format(new_name,P_id)
                                            nom_upd_in_Doc="UPDATE doctor SET Patient_Name='{}' WHERE Patient_ID='{}'".format(new_name,P_id)
                                            cursor.execute(nom_upd_in_Pat)
                                            cursor.execute(nom_upd_in_Doc)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_name).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='age':
                                        P_age_label=Label(frame3,text='Enter new age:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_age_entry=Entry(frame3,width=30,borderwidth=10);P_age_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_age():
                                            global data_pat
                                            new_age=P_age_entry.get()
                                            age_upd="UPDATE patient SET Age={} WHERE Patient_ID='{}'".format(new_age,P_id)
                                            cursor.execute(age_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_age).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='Ph':
                                        P_Ph_label=Label(frame3,text='Enter new Ph No.:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_Ph_entry=Entry(frame3,width=30,borderwidth=10);P_Ph_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_ph():
                                            global data_pat
                                            new_Ph=P_Ph_entry.get()
                                            ph_upd="UPDATE patient SET Ph_No={} WHERE Patient_ID='{}'".format(new_Ph,P_id)
                                            cursor.execute(ph_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_ph).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='Pin':
                                        pin_label=Label(frame3,text='Enter new Pincode:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        pin_entry=Entry(frame3,width=30,borderwidth=10);pin_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_pin():
                                            global data_pat
                                            new_Pin=pin_entry.get()
                                            pin_upd="UPDATE patient SET Pincode={} WHERE Patient_ID='{}'".format(new_Pin,P_id)
                                            cursor.execute(pin_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=change_pin).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='fee':
                                        fee_label=Label(frame3,text='Enter new Fee:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        fee_entry=Entry(frame3,width=30,borderwidth=10);fee_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_fee():
                                            global data_pat
                                            new_fee=int(fee_entry.get())
                                            fee_upd="UPDATE patient SET Fee={} WHERE Patient_ID='{}'".format(new_fee,P_id)
                                            cursor.execute(fee_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_fee).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='stat':
                                        stat_label=Label(frame3,text='Enter new status(In House/Cured):',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        stat_entry=Entry(frame3,width=30,borderwidth=10);stat_entry.grid(row=2,column=1,pady=10,padx=10)
                                        discharge_date=Label(frame3,text='Enter Discharge date (yyyy-mm-dd):',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                                        discharge_date_entry=Entry(frame3,width=30,borderwidth=10);discharge_date_entry.grid(row=3,column=1,pady=10,padx=10)
                                        def change_stat():
                                            global data_pat
                                            new_stat=stat_entry.get();new_discharge=discharge_date_entry.get()
                                            stat_upd_in_Pat="UPDATE patient SET Status='{}' WHERE Patient_ID='{}'".format(new_stat,P_id)
                                            stat_upd_in_Doc="UPDATE doctor SET Patient_Status='{}' WHERE Patient_ID='{}'".format(new_stat,P_id)
                                            discharge_upd="UPDATE patient SET Date_of_discharge='{}' WHERE Patient_ID='{}'".format(new_discharge,P_id)
                                            cursor.execute(stat_upd_in_Doc)
                                            cursor.execute(stat_upd_in_Pat)
                                            cursor.execute(discharge_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_stat).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                        
                                Name_upd=Button(frame3,text='Name',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('name')).grid()
                                Age_upd=Button(frame3,text='Age',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('age')).grid()
                                Ph_upd=Button(frame3,text='Phone No.',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Ph')).grid()
                                Pin_upd=Button(frame3,text='Pincode',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Pin')).grid()
                                fee_upd=Button(frame3,text='Fee',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('fee')).grid()
                                stat_upd=Button(frame3,text='status',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('stat')).grid()
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(operation,'upd',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(P_id_entry.get())).grid(columnspan=20,padx=10,pady=10)        
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                    if op_name=='rem':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10);P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def rem():
                            global data_pat,data_doc
                            P_id=P_id_entry.get()
                            if P_id in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                cursor.reset()
                                rem_pat_in_doc="DELETE FROM doctor WHERE Patient_ID='{}'".format(P_id,)
                                rem_pat_in_pat="DELETE FROM patient WHERE Patient_ID='{}'".format(P_id,)
                                cursor.execute(rem_pat_in_doc)
                                cursor.execute(rem_pat_in_pat)
                                mycon.commit()
                                messagebox.showinfo("Update", "Update sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from patient')
                                data_pat=cursor.fetchall()
                                cursor.reset()
                                cursor.execute('select * from doctor')
                                data_doc=cursor.fetchall()
                                adm('pat')
                            else:
                                messagebox.showerror("ID", " ID does not exist. Enter different one.")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=rem).grid(columnspan=20,padx=10,pady=10)                
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)      

                    if op_name=='add':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter New Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10)
                        P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def add():
                            global data_pat;P_id=P_id_entry.get()
                            if P_id not in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                P_name_label=Label(frame3,text='Enter New Patient name:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                P_name_entry=Entry(frame3,width=30,borderwidth=10);P_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                P_age_label=Label(frame3,text='Enter New Patient age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                                P_age_entry=Entry(frame3,width=30,borderwidth=10);P_age_entry.grid(row=3,column=1,pady=10,padx=10)
                                P_gender_label=Label(frame3,text='Enter New Patient gender:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                                P_gender_entry=Entry(frame3,width=30,borderwidth=10);P_gender_entry.grid(row=4,column=1,pady=10,padx=10)
                                P_ph_label=Label(frame3,text='Enter New Patient Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                                P_ph_entry=Entry(frame3,width=30,borderwidth=10);P_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                                P_doc_label=Label(frame3,text='Enter New Patient Doctor:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=6,column=0,pady=10,padx=10)
                                P_doc_entry=Entry(frame3,width=30,borderwidth=10);P_doc_entry.grid(row=6,column=1,pady=10,padx=10)
                                P_pin_label=Label(frame3,text='Enter New Patient Pincode:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=8,column=0,pady=10,padx=10)
                                P_pin_entry=Entry(frame3,width=30,borderwidth=10);P_pin_entry.grid(row=8,column=1,pady=10,padx=10)
                    
                                def add2():
                                    global data_pat,data_doc #global keyword in prev scope doesnt apply here so changes here are not carried if not global in this defined fxn
                                    P_name=P_name_entry.get();P_age=P_age_entry.get();P_gender=P_gender_entry.get();P_ph=int(P_ph_entry.get());P_doc=P_doc_entry.get();P_pin=int(P_pin_entry.get());
                                    did="select * from doctor where Name='{}'".format(P_doc)
                                    cursor.execute(did)
                                    p=list(cursor.fetchone())
                                    p.pop(6);p.pop(6);p.pop(8);p.pop(6);p.pop(6)# removes pid,pname,status,diagnosis and treat
                                    final=tuple(p)
                                    D_id,D_name,D_age,Sp,Ph,Email=final #unpacking tuple
                                    today=datetime.date.today()
                                    cursor.reset()
                                    add_pat_in_doc="INSERT INTO doctor VALUES('{}','{}',{},'{}',{},'{}','{}','{}',NULL,NULL,'{}')".format(D_id,D_name,D_age,Sp,Ph,Email,P_id,P_name,'In House')
                                    add_pat_in_pat="INSERT INTO patient VALUES('{}','{}',{},'{}',{},'{}',NULL,NULL,NULL,{},'{}','{}',NULL)".format(P_id,P_name,P_age,P_gender,P_ph,D_name,P_pin,'In House',today)
                                    cursor.execute(add_pat_in_doc)
                                    cursor.execute(add_pat_in_pat)
                                    mycon.commit()
                                    messagebox.showinfo("Update", "Update sucessful!!")
                                    cursor.reset()
                                    cursor.execute('select * from patient')
                                    data_pat=cursor.fetchall()
                                    cursor.reset()
                                    cursor.execute('select * from doctor')
                                    data_doc=cursor.fetchall()
                                    adm('pat')
                                    
                                enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add2).grid(columnspan=20,padx=10,pady=10)
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(row=3,column=3)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)        

                update_doc=Button(frame3,text='Update Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
                remove_doc=Button(frame3,text='Remove Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem')).grid()
                insert_doc=Button(frame3,text='Add Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add')).grid()
                show_bt=Button(frame3,text='Show Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(after_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

#completely done DONE for adm adm
            if update_for=='adm':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='rem_admin':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        Adm_id_rem_label=Label(frame3,text='Enter Admin ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        Adm_id_rem_entry=Entry(frame3,width=30,borderwidth=10);Adm_id_rem_entry.grid(row=2,column=1,pady=10,padx=10)
                        def rem():
                            global data_adm
                            A_id=Adm_id_rem_entry.get()
                            if A_id in list(set(map(lambda i:i[0],data_adm))):
                                print(list(set(map(lambda i:i[0],data_adm))))
                                rem_adm="DELETE FROM admin WHERE Ad_Id='{}'".format(A_id,)
                                cursor.execute(rem_adm)
                                mycon.commit()
                                messagebox.showinfo("Update", "Update sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from admin')
                                data_adm=cursor.fetchall()
                                print(list(set(map(lambda i:i[0],data_adm))))
                                adm('adm')
                            else:
                                messagebox.showerror("ID", " ID does not exist. Enter different one.")
                            
                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=rem).grid(row=3,column=3)
                        back3_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'adm',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                    if op_name=='add_admin':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        NA_id_label=Label(frame3,text='Enter Admin ID to add:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        NA_id_entry=Entry(frame3,width=30,borderwidth=10);NA_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        NA_name_label=Label(frame3,text='Enter New Admin Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        NA_name_entry=Entry(frame3,width=30,borderwidth=10);NA_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        def add():
                            global data_adm
                            new_name=str(NA_name_entry.get())
                            new_email=str(NA_name_entry.get())+'@salus.com'
                            A_id=NA_id_entry.get()
                            if A_id not in list(set(map(lambda i:i[0],data_adm))):
                                new_upd="INSERT INTO admin(Ad_Id,Name,Email)  VALUES('{}','{}','{}')".format(A_id,new_name,new_email)
                                cursor.execute(new_upd)
                                mycon.commit()
                                messagebox.showinfo("Update", "Addition of admin sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from admin')
                                data_adm=cursor.fetchall()
                                print(list(set(map(lambda i:i[0],data_adm))))#---> to reflect change, i retrieve data again
                                adm('adm')
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'adm',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                        
                    

                remove_adm=Button(frame3,text='Remove Admin',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem_admin')).grid()
                insert_adm=Button(frame3,text='Add Admin',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add_admin')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(after_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                
                
        update_pat_bt=Button(frame3,text='Patient Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('pat')).grid()
        update_doc_bt=Button(frame3,text='Doctor Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('doc')).grid()
        update_adm_bt=Button(frame3,text='Admin Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('adm')).grid()
            
  #''' if user=='Patient Login':'''  
 
    
def page(user):
    global login
    login=user
    clear((head_label,))
    root.title(login)
    frame2=Frame(root)
    frame2.pack(padx=10,pady=10)
    name_label=Label(frame2,text=login,font=('Lucida Bright',20,'underline'),foreground='#F5F5F5',background='#8B8B7D').grid(columnspan=2,padx=10,pady=10)
    user_label=Label(frame2,text='Username',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D').grid(row=1,column=0,pady=10,padx=10)
    user_entry=Entry(frame2,width=30,borderwidth=10)
    user_entry.grid(row=1,column=1,pady=10,padx=10)
    passd_label=Label(frame2,text='Password',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D').grid(row=2,column=0,pady=10,padx=10)
    passd_entry=Entry(frame2,width=30,borderwidth=10)
    passd_entry.grid(row=2,column=1,pady=10,padx=10)
    back_bt=Button(frame2,image=pic4,background='#8B8B7D',command=lambda:back(home_page,'?',(head_label,))).grid(columnspan=2,padx=10,pady=10)

    #logging in
    def login_fn():
        global username,password
        username=user_entry.get();password=passd_entry.get()
        login_dict={}
        def login_fn2(data):
             for i in data:
                login_dict[i[0]]=i[1]
             if username in login_dict:
                if password==login_dict[username]:
                    messagebox.showinfo("login", "login sucessful!!")
                    after_login(login)
                else:
                    messagebox.showerror("login", " Wrong Password. Try again?")
             else:
                messagebox.showerror("login", "User does not exist. Try again?")
        if login=='Doctor Login':
            login_fn2(data_doc)   
        if login=='Admin Login':
            login_fn2(data_adm)
        if login=='Patient Login':
            login_fn2(data_pat)
            
    login_button=Button(frame2,text='LOGIN',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D',command=login_fn).grid(columnspan=2,padx=10,pady=10)

def home_page(m):
    root.title("Welcome Page")
    root.geometry("400x400")
    root.configure(bg='#8B8B7D')

    frame1=Frame(root)
    frame1.pack(padx=10,pady=10)

    b_doctor=Button(frame1,image=pic1,command=lambda:page('Doctor Login'))
    b_doctor.grid(row=0,column=0,padx=10,pady=10)
    l_doctor=Label(frame1,text='DOCTOR',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_doctor.grid(row=1,column=0,pady=10,padx=10)

    b_admin=Button(frame1,image=pic2,command=lambda:page('Admin Login'))
    b_admin.grid(row=0,column=1,pady=10,padx=10)
    l_admin=Label(frame1,text='ADMIN',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_admin.grid(row=1,column=1,padx=10,pady=10)

    b_patient=Button(frame1,image=pic3,command=lambda:page('Patient Login'))
    b_patient.grid(row=0,column=2,padx=10,pady=10)
    l_patient=Label(frame1,text='PATIENT',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_patient.grid(row=1,column=2,pady=10,padx=10)

home_page('?')
      
    
    
root.mainloop()



import mysql.connector as m
from tkinter import *
from tkinter import messagebox,ttk
from PIL import ImageTk,Image
import datetime

mycon=m.connect(host='localhost',user='root',passwd='MyMySql',database='miniproject')
if mycon.is_connected():
    print('Connected')


cursor=mycon.cursor() #creates cursor
cursor.execute('select * from patient')
data_pat=cursor.fetchall() #holds data in the form of list of tuples
cursor.execute('select * from doctor')
data_doc=cursor.fetchall()
cursor.execute('select * from admin')
data_adm=cursor.fetchall()

#mycon.close()

#holds all data

root=Tk()

img1=Image.open(r'C:\Python mini proj\doc.png')
img2=Image.open(r'C:\Python mini proj\admin.png')
img3=Image.open(r'C:\Python mini proj\patient.png')
img4=Image.open(r'C:\Python mini proj\back.png')
n1_img=img1.resize((100,100))
n2_img=img2.resize((100,100))
n3_img=img3.resize((100,100))
n4_img=img4.resize((60,30))
pic1=ImageTk.PhotoImage(n1_img)
pic2=ImageTk.PhotoImage(n2_img)
pic3=ImageTk.PhotoImage(n3_img)
pic4=ImageTk.PhotoImage(n4_img)

head_label=Label(root,text='Salus Hospitals',font=('Britannic Bold',30,'underline'),background='#8B8B7D',foreground='#F5F5F5')
head_label.pack(padx=20,pady=20)
#Creating parameter buttons
def clear(keep_root,keep_frame=()):
    for widget_root in root.winfo_children():
        if widget_root.winfo_class()== 'Frame':
            for widget_frame in widget_root.winfo_children():
                if widget_frame not in keep_frame:
                    widget_frame.destroy()
        if widget_root not in keep_root:
            widget_root.destroy()
def back(w,x,y,z=()):
    clear(y,z)
    w(x)
    
def apres_login(user):
    clear((head_label,))
    root.title('Main page')
    frame3=Frame(root,bg='#8B8B7D');frame3.pack()
    welcome_label=Label(frame3,text='Welcome'+' '+password+'            ',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5')
    welcome_label.grid(row=1,column=0)#cannot ue grid in prev line itelf caue it give None type
    logout_bt=Button(frame3,text='Logout',font=('Lucida Bright',10),background='#8B8B7D',foreground='#F5F5F5',command=lambda:back(page,user,(head_label,)))
    logout_bt.grid(row=1,column=20)#cannot ue grid in prev line itelf caue it give None type

    
    if user=='Doctor Login':
        def operation(op_name):
            if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10)
                        P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def id_fn(P_id):
                            pat_id_under_doc="SELECT Patient_ID FROM doctor WHERE Doctor_ID='{}'".format(username) #only patients under the specific doctor
                            cursor.execute(pat_id_under_doc)
                            pat_id=cursor.fetchall() #list of single element(pat id) tuple
                            #print(pat_id)
                            patient_id=[]
                            for i in pat_id:
                                patient_id.append(i[0])
                                
                            if P_id in patient_id:
                                pat_data="SELECT Diagnosis, Treatment FROM doctor WHERE Patient_ID='{}' AND Doctor_ID='{}'".format(P_id,username) 
                                cursor.execute(pat_data)
                                pat_data=cursor.fetchall()
                                #print(pat_data)

                                if (None, None) in pat_data:
                                    clear((head_label,frame3),(welcome_label,logout_bt))                                   
                                    P_diagnosis_label=Label(frame3,text='Enter diagnosis:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                    P_treatment_label=Label(frame3,text='Enter diagnosis:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                                    P_diagnosis_entry=Entry(frame3,width=30,borderwidth=10);P_diagnosis_entry.grid(row=2,column=1,pady=10,padx=10)
                                    P_treatment_entry=Entry(frame3,width=30,borderwidth=10);P_treatment_entry.grid(row=4,column=1,pady=10,padx=10)
                                    def upd_diagnosis_and_treatment():
                                        diagnosis=P_diagnosis_entry.get()
                                        treatment=P_treatment_entry.get()
                                        #print(diagnosis,treatment)
                                        upd_in_doc="UPDATE doctor SET Diagnosis='{}', Treatment='{}' WHERE Patient_ID='{}' AND Doctor_ID='{}' AND Diagnosis IS NULL AND Treatment IS NULL ".format(diagnosis,treatment,P_id,username,None,None)
                                        upd_in_pat="UPDATE patient SET Diagnosis='{}', Treatment='{}' WHERE Patient_ID='{}' AND Doctor='{}' AND Diagnosis IS NULL AND Treatment IS NULL".format(diagnosis,treatment,P_id,password,None,None)
                                        cursor.execute(upd_in_doc)
                                        cursor.execute(upd_in_pat)
                                        mycon.commit()
                                        messagebox.showinfo("Update", "Update sucessful!!")
                                        ans = messagebox.askyesno("Next", "update for another patient?")
                                        if ans:
                                            operation(op_name)
                                        else:
                                            after_login(user)
                                    enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=upd_diagnosis_and_treatment)
                                    enter_bt.grid(columnspan=20,padx=10,pady=10)
                                    back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt)))
                                    back_bt.grid(columnspan=20,padx=10,pady=10)
                                else:
                                    messagebox.showerror("ID", " Patient does not have an appointment with you. Try again?")
                                    operation(op_name)
                               
                                
                            else:
                                messagebox.showerror("ID", " Patient does not exist under your domain. Try again?")
                                
                                
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(P_id_entry.get()))        
                        enter_bt.grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(after_login,user,(head_label,frame3),(welcome_label,logout_bt)))
                        back_bt.grid(columnspan=20,padx=10,pady=10)


            #if op_name=='show':

        update_pat_bt=Button(frame3,text='Update Patient Prescription',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
        show_pat_bt=Button(frame3,text='Show Patient List',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()

                 
              
    if user=='Admin Login':
        def adm(update_for):
            if update_for=='doc':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        D_id_label=Label(frame3,text='Enter Doctor ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        D_id_entry=Entry(frame3,width=30,borderwidth=10)
                        D_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        
                        def id_fn(D_id):
                            if D_id in list(set(map(lambda i:i[0],data_doc))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                upd_label=Label(frame3,text='What do you want to update?',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                                def upd1(i):
                                    clear((head_label,frame3),(welcome_label,logout_bt))
                                    if i=='name':
                                        D_name_label=Label(frame3,text='Enter new name:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_name_entry=Entry(frame3,width=30,borderwidth=10);D_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_name():
                                            global data_doc,data_pat
                                            new_name='Dr. '+str(D_name_entry.get())
                                            new_email=str(D_name_entry.get())+'@salus.com'
                                            def getoldname(i):
                                                get_old_name="SELECT Name FROM doctor WHERE Doctor_ID='{}'".format(i,)
                                                cursor.execute(get_old_name)
                                                data=cursor.fetchone()
                                                return data[0]
                                            old_name=str(getoldname(D_id))
                                            print(old_name)
                                            cursor.reset() #to reset as otherise it then fetches n-1 not n records
                                            nom_upd1="UPDATE doctor SET Name='{}' WHERE Doctor_ID='{}'".format(new_name,D_id)
                                            cursor.execute(nom_upd1)
                                            nom_upd_inPat="UPDATE patient SET Doctor='{}' WHERE Doctor='{}'".format(new_name,old_name)
                                            cursor.execute(nom_upd_inPat)
                                            email_upd="UPDATE doctor SET E_mail='{}' WHERE Doctor_ID='{}'".format(new_email,D_id)
                                            cursor.execute(email_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_name).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='age':
                                        D_age_label=Label(frame3,text='Enter new age:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_age_entry=Entry(frame3,width=30,borderwidth=10);D_age_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_age():
                                            global data_doc
                                            new_age=D_age_entry.get()
                                            age_upd="UPDATE doctor SET Age='{}' WHERE Doctor_ID='{}'".format(new_age,D_id)
                                            cursor.execute(age_upd)
                                            mycon.commit()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_age).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='Ph':
                                        D_Ph_label=Label(frame3,text='Enter new Ph No.:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        D_Ph_entry=Entry(frame3,width=30,borderwidth=10);D_Ph_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_ph():
                                            new_Ph=D_Ph_entry.get()
                                            if len(new_Ph)>10:
                                                messagebox.showerror("ID", " Too many digits in ph no.. Try again?")
                                            else:
                                                global data_doc
                                                ph_upd="UPDATE doctor SET Ph_No='{}' WHERE Doctor_ID='{}'".format(new_Ph,D_id)
                                                cursor.execute(ph_upd)
                                                mycon.commit()
                                                cursor.reset()
                                                cursor.execute('select * from doctor')
                                                data_doc=cursor.fetchall()
                                                messagebox.showinfo("Update", "Update sucessful!!")
                                                id_fn(D_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_ph).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,D_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                Name_upd=Button(frame3,text='Name',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('name')).grid()
                                Age_upd=Button(frame3,text='Age',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('age')).grid()
                                Ph_upd=Button(frame3,text='Phone No.',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Ph')).grid()
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(operation,'upd',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                            else:
                                messagebox.showerror("ID", " Wrong ID. Try again?")
                            
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(D_id_entry.get())).grid(row=3,column=3)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                   
                    if op_name=='rem':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        D_id_label=Label(frame3,text='Enter Doctor ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        D_id_entry=Entry(frame3,width=30,borderwidth=10)
                        D_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        RD_name_label=Label(frame3,text='Enter Rep. Doctor Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        RD_name_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        RD_age_label=Label(frame3,text='Enter Rep. Doctor Age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                        RD_age_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_age_entry.grid(row=4,column=1,pady=10,padx=10)
                        RD_ph_label=Label(frame3,text='Enter Rep Doctor Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                        RD_ph_entry=Entry(frame3,width=30,borderwidth=10)
                        RD_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                        def do():
                            global data_doc, data_pat
                            new_name='Dr. '+str(RD_name_entry.get())
                            new_email=str(RD_name_entry.get())+'@salus.com'
                            new_Ph=RD_ph_entry.get()
                            new_age=RD_age_entry.get()
                            D_id=D_id_entry.get()
                            def getoldname(i):
                                get_old_name="SELECT Name FROM doctor WHERE Doctor_ID='{}'".format(i,)
                                cursor.execute(get_old_name)
                                data=cursor.fetchone()
                                return data[0]
                            old_name=str(getoldname(D_id))
                            nom_upd="UPDATE doctor SET Name='{}' WHERE Doctor_ID='{}'".format(new_name,D_id)
                            email_upd="UPDATE doctor SET E_mail='{}' WHERE Doctor_ID='{}'".format(new_email,D_id)
                            ph_upd="UPDATE doctor SET Ph_No='{}' WHERE Doctor_ID='{}'".format(new_Ph,D_id)
                            age_upd="UPDATE doctor SET Age='{}' WHERE Doctor_ID='{}'".format(new_age,D_id)
                            nom_upd_inPat="UPDATE patient SET Doctor='{}' WHERE Doctor='{}'".format(new_name,old_name)
                            cursor.execute(nom_upd_inPat)
                            cursor.execute(age_upd)
                            cursor.execute(ph_upd)
                            cursor.execute(nom_upd)
                            cursor.execute(email_upd)
                            mycon.commit()
                            cursor.reset()
                            cursor.execute('select * from doctor')
                            data_doc=cursor.fetchall()
                            cursor.reset()
                            cursor.execute('select * from patient')
                            data_pat=cursor.fetchall()
                            messagebox.showinfo("Update", "Update sucessful!!")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=do).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                    if op_name=='add':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        ND_id_label=Label(frame3,text='Enter Doctor ID to add:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        ND_id_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        ND_name_label=Label(frame3,text='Enter New Doctor Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        ND_name_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        ND_age_label=Label(frame3,text='Enter New Doctor Age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                        ND_age_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_age_entry.grid(row=4,column=1,pady=10,padx=10)
                        ND_ph_label=Label(frame3,text='Enter New Doctor Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                        ND_ph_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                        ND_dept_label=Label(frame3,text='Enter New Doctor Specl.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=6,column=0,pady=10,padx=10)
                        ND_dept_entry=Entry(frame3,width=30,borderwidth=10)
                        ND_dept_entry.grid(row=6,column=1,pady=10,padx=10)
                        
                        def add():
                            global data_doc
                            new_name='Dr. '+str(ND_name_entry.get())
                            new_email=str(ND_name_entry.get())+'@salus.com'
                            new_Ph=ND_ph_entry.get()
                            new_age=ND_age_entry.get()
                            new_dept=ND_dept_entry.get()
                            D_id=ND_id_entry.get()
                            if D_id not in list(set(map(lambda i:i[0],data_doc))):
                                new_upd="INSERT INTO doctor(Doctor_ID,Name,Age,Specialisation,Ph_No,E_mail)  VALUES('{}','{}','{}','{}','{}','{}')".format(D_id,new_name,new_age,new_dept,new_Ph,new_email)
                                cursor.execute(new_upd)
                                mycon.commit()
                                cursor.reset()
                                cursor.execute('select * from doctor')
                                data_doc=cursor.fetchall()
                                messagebox.showinfo("Update", "Addition of doctor sucessful!!")
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'doc',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                    #HO
                update_doc=Button(frame3,text='Update Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
                remove_doc=Button(frame3,text='Remove Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem')).grid()
                insert_doc=Button(frame3,text='Add Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add')).grid()
                show_bt=Button(frame3,text='Show Doctor Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(apres_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                
            if update_for=='pat':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='upd':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10);P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def id_fn(P_id):
                            global data_pat
                            if P_id in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                upd_label=Label(frame3,text='What do you want to update?',font=('Lucida Bright',30,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                                def upd1(i):
                                    clear((head_label,frame3),(welcome_label,logout_bt))
                                    if i=='name':
                                        P_name_label=Label(frame3,text='Enter new name:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_name_entry=Entry(frame3,width=30,borderwidth=10);P_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_name():
                                            global data_doc,data_pat
                                            new_name=str(P_name_entry.get())
                                            nom_upd_in_Pat="UPDATE patient SET Name='{}' WHERE Patient_ID='{}'".format(new_name,P_id)
                                            nom_upd_in_Doc="UPDATE doctor SET Patient_Name='{}' WHERE Patient_ID='{}'".format(new_name,P_id)
                                            cursor.execute(nom_upd_in_Pat)
                                            cursor.execute(nom_upd_in_Doc)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_name).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                    if i=='age':
                                        P_age_label=Label(frame3,text='Enter new age:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_age_entry=Entry(frame3,width=30,borderwidth=10);P_age_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_age():
                                            global data_pat
                                            new_age=P_age_entry.get()
                                            age_upd="UPDATE patient SET Age={} WHERE Patient_ID='{}'".format(new_age,P_id)
                                            cursor.execute(age_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_age).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='Ph':
                                        P_Ph_label=Label(frame3,text='Enter new Ph No.:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        P_Ph_entry=Entry(frame3,width=30,borderwidth=10);P_Ph_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_ph():
                                            global data_pat
                                            new_Ph=P_Ph_entry.get()
                                            ph_upd="UPDATE patient SET Ph_No={} WHERE Patient_ID='{}'".format(new_Ph,P_id)
                                            cursor.execute(ph_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_ph).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='Pin':
                                        pin_label=Label(frame3,text='Enter new Pincode:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        pin_entry=Entry(frame3,width=30,borderwidth=10);pin_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def change_pin():
                                            global data_pat
                                            new_Pin=pin_entry.get()
                                            pin_upd="UPDATE patient SET Pincode={} WHERE Patient_ID='{}'".format(new_Pin,P_id)
                                            cursor.execute(pin_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=change_pin).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='fee':
                                        fee_label=Label(frame3,text='Enter new Fee:',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        fee_entry=Entry(frame3,width=30,borderwidth=10);fee_entry.grid(row=2,column=1,pady=10,padx=10)
                                        def update_pat_fee():
                                            global data_pat
                                            new_fee=int(fee_entry.get())
                                            fee_upd="UPDATE patient SET Fee={} WHERE Patient_ID='{}'".format(new_fee,P_id)
                                            cursor.execute(fee_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=update_pat_fee).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                    if i=='stat':
                                        stat_label=Label(frame3,text='Enter new status(In House/Cured):',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                        stat_entry=Entry(frame3,width=30,borderwidth=10);stat_entry.grid(row=2,column=1,pady=10,padx=10)
                                        discharge_date=Label(frame3,text='Enter Discharge date (yyyy-mm-dd):',font=('Lucida Bright',30,'italic'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                                        discharge_date_entry=Entry(frame3,width=30,borderwidth=10);discharge_date_entry.grid(row=3,column=1,pady=10,padx=10)
                                        def change_stat():
                                            global data_pat
                                            new_stat=stat_entry.get();new_discharge=discharge_date_entry.get()
                                            stat_upd_in_Pat="UPDATE patient SET Status='{}' WHERE Patient_ID='{}'".format(new_stat,P_id)
                                            stat_upd_in_Doc="UPDATE doctor SET Patient_Status='{}' WHERE Patient_ID='{}'".format(new_stat,P_id)
                                            discharge_upd="UPDATE patient SET Date_of_discharge='{}' WHERE Patient_ID='{}'".format(new_discharge,P_id)
                                            cursor.execute(stat_upd_in_Doc)
                                            cursor.execute(stat_upd_in_Pat)
                                            cursor.execute(discharge_upd)
                                            mycon.commit()
                                            cursor.reset()
                                            cursor.execute('select * from patient')
                                            data_pat=cursor.fetchall()
                                            cursor.reset()
                                            cursor.execute('select * from doctor')
                                            data_doc=cursor.fetchall()
                                            messagebox.showinfo("Update", "Update sucessful!!")
                                            id_fn(P_id)
                                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=change_stat).grid(row=3,column=3)
                                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(id_fn,P_id,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                        
                                        
                                Name_upd=Button(frame3,text='Name',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('name')).grid()
                                Age_upd=Button(frame3,text='Age',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('age')).grid()
                                Ph_upd=Button(frame3,text='Phone No.',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Ph')).grid()
                                Pin_upd=Button(frame3,text='Pincode',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('Pin')).grid()
                                fee_upd=Button(frame3,text='Fee',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('fee')).grid()
                                stat_upd=Button(frame3,text='status',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5',command=lambda:upd1('stat')).grid()
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(operation,'upd',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                                
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=lambda:id_fn(P_id_entry.get())).grid(columnspan=20,padx=10,pady=10)        
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                    if op_name=='rem':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter Patient ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10);P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def rem():
                            global data_pat,data_doc
                            P_id=P_id_entry.get()
                            if P_id in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                cursor.reset()
                                rem_pat_in_doc="DELETE FROM doctor WHERE Patient_ID='{}'".format(P_id,)
                                rem_pat_in_pat="DELETE FROM patient WHERE Patient_ID='{}'".format(P_id,)
                                cursor.execute(rem_pat_in_doc)
                                cursor.execute(rem_pat_in_pat)
                                mycon.commit()
                                messagebox.showinfo("Update", "Update sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from patient')
                                data_pat=cursor.fetchall()
                                cursor.reset()
                                cursor.execute('select * from doctor')
                                data_doc=cursor.fetchall()
                                adm('pat')
                            else:
                                messagebox.showerror("ID", " ID does not exist. Enter different one.")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=rem).grid(columnspan=20,padx=10,pady=10)                
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)      

                    if op_name=='add':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        P_id_label=Label(frame3,text='Enter New Patient ID:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        P_id_entry=Entry(frame3,width=30,borderwidth=10)
                        P_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        def add():
                            global data_pat;P_id=P_id_entry.get()
                            if P_id not in list(set(map(lambda i:i[0],data_pat))):
                                clear((head_label,frame3),(welcome_label,logout_bt))
                                P_name_label=Label(frame3,text='Enter New Patient name:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                                P_name_entry=Entry(frame3,width=30,borderwidth=10);P_name_entry.grid(row=2,column=1,pady=10,padx=10)
                                P_age_label=Label(frame3,text='Enter New Patient age:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                                P_age_entry=Entry(frame3,width=30,borderwidth=10);P_age_entry.grid(row=3,column=1,pady=10,padx=10)
                                P_gender_label=Label(frame3,text='Enter New Patient gender:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=4,column=0,pady=10,padx=10)
                                P_gender_entry=Entry(frame3,width=30,borderwidth=10);P_gender_entry.grid(row=4,column=1,pady=10,padx=10)
                                P_ph_label=Label(frame3,text='Enter New Patient Ph No.:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=5,column=0,pady=10,padx=10)
                                P_ph_entry=Entry(frame3,width=30,borderwidth=10);P_ph_entry.grid(row=5,column=1,pady=10,padx=10)
                                P_doc_label=Label(frame3,text='Enter New Patient Doctor:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=6,column=0,pady=10,padx=10)
                                P_doc_entry=Entry(frame3,width=30,borderwidth=10);P_doc_entry.grid(row=6,column=1,pady=10,padx=10)
                                P_pin_label=Label(frame3,text='Enter New Patient Pincode:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=8,column=0,pady=10,padx=10)
                                P_pin_entry=Entry(frame3,width=30,borderwidth=10);P_pin_entry.grid(row=8,column=1,pady=10,padx=10)
                    
                                def add2():
                                    global data_pat,data_doc #global keyword in prev scope doesnt apply here so changes here are not carried if not global in this defined fxn
                                    P_name=P_name_entry.get();P_age=P_age_entry.get();P_gender=P_gender_entry.get();P_ph=int(P_ph_entry.get());P_doc=P_doc_entry.get();P_pin=int(P_pin_entry.get());
                                    did="select * from doctor where Name='{}'".format(P_doc)
                                    cursor.execute(did)
                                    p=list(cursor.fetchone())
                                    p.pop(6);p.pop(6);p.pop(8)# removes pid,pname,status
                                    final=tuple(p)
                                    D_id,D_name,D_age,Sp,Ph,Email,Diag,Treat=final #unpacking tuple
                                    today=datetime.date.today()
                                    cursor.reset()
                                    pfee="select Fee from patient where Doctor='{}'".format(P_doc)
                                    cursor.execute(pfee)
                                    pfee=cursor.fetchone()
                                    fee=pfee[0];print(fee)
                                    cursor.reset()
                                    add_pat_in_doc="INSERT INTO doctor VALUES('{}','{}',{},'{}',{},'{}','{}','{}','{}','{}','{}')".format(D_id,D_name,D_age,Sp,Ph,Email,P_id,P_name,Diag,Treat,'In House')
                                    add_pat_in_pat="INSERT INTO patient VALUES('{}','{}',{},'{}',{},'{}','{}','{}',{},{},'{}','{}',NULL)".format(P_id,P_name,P_age,P_gender,P_ph,D_name,Diag,Treat,fee,P_pin,'In House',today)
                                    cursor.execute(add_pat_in_doc)
                                    cursor.execute(add_pat_in_pat)
                                    mycon.commit()
                                    messagebox.showinfo("Update", "Update sucessful!!")
                                    cursor.reset()
                                    cursor.execute('select * from patient')
                                    data_pat=cursor.fetchall()
                                    cursor.reset()
                                    cursor.execute('select * from doctor')
                                    data_doc=cursor.fetchall()
                                    adm('pat')
                                    
                                enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add2).grid(columnspan=20,padx=10,pady=10)
                                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(row=3,column=3)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'pat',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)        

                update_doc=Button(frame3,text='Update Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('upd')).grid()
                remove_doc=Button(frame3,text='Remove Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem')).grid()
                insert_doc=Button(frame3,text='Add Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add')).grid()
                show_bt=Button(frame3,text='Show Patient Records',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('show')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(apres_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

#completely done DONE for adm adm
            if update_for=='adm':
                clear((head_label,frame3),(welcome_label,logout_bt))       
                op_label=Label(frame3,text='What do you want to do?',font=('Lucida Bright',20,'underline'),background='#8B8B7D',foreground='#F5F5F5').grid()
                def operation(op_name):
                    if op_name=='rem_admin':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        Adm_id_rem_label=Label(frame3,text='Enter Admin ID to remove:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        Adm_id_rem_entry=Entry(frame3,width=30,borderwidth=10);Adm_id_rem_entry.grid(row=2,column=1,pady=10,padx=10)
                        def rem():
                            global data_adm
                            A_id=Adm_id_rem_entry.get()
                            if A_id in list(set(map(lambda i:i[0],data_adm))):
                                print(list(set(map(lambda i:i[0],data_adm))))
                                rem_adm="DELETE FROM admin WHERE Ad_Id='{}'".format(A_id,)
                                cursor.execute(rem_adm)
                                mycon.commit()
                                messagebox.showinfo("Update", "Update sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from admin')
                                data_adm=cursor.fetchall()
                                print(list(set(map(lambda i:i[0],data_adm))))
                                adm('adm')
                            else:
                                messagebox.showerror("ID", " ID does not exist. Enter different one.")
                            
                        enter_bt1=Button(frame3,text='Enter',background='#8B8B7D',command=rem).grid(row=3,column=3)
                        back3_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'adm',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)

                    if op_name=='add_admin':
                        clear((head_label,frame3),(welcome_label,logout_bt))
                        NA_id_label=Label(frame3,text='Enter Admin ID to add:',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=2,column=0,pady=10,padx=10)
                        NA_id_entry=Entry(frame3,width=30,borderwidth=10);NA_id_entry.grid(row=2,column=1,pady=10,padx=10)
                        NA_name_label=Label(frame3,text='Enter New Admin Name :',font=('Lucida Bright',15,'italic','underline'),background='#8B8B7D',foreground='#F5F5F5').grid(row=3,column=0,pady=10,padx=10)
                        NA_name_entry=Entry(frame3,width=30,borderwidth=10);NA_name_entry.grid(row=3,column=1,pady=10,padx=10)
                        def add():
                            global data_adm
                            new_name=str(NA_name_entry.get())
                            new_email=str(NA_name_entry.get())+'@salus.com'
                            A_id=NA_id_entry.get()
                            if A_id not in list(set(map(lambda i:i[0],data_adm))):
                                new_upd="INSERT INTO admin(Ad_Id,Name,Email)  VALUES('{}','{}','{}')".format(A_id,new_name,new_email)
                                cursor.execute(new_upd)
                                mycon.commit()
                                messagebox.showinfo("Update", "Addition of admin sucessful!!")
                                cursor.reset()
                                cursor.execute('select * from admin')
                                data_adm=cursor.fetchall()
                                print(list(set(map(lambda i:i[0],data_adm))))#---> to reflect change, i retrieve data again
                                adm('adm')
                            else:
                                messagebox.showerror("ID", " ID already exists. Enter different one.")
                        
                        enter_bt=Button(frame3,text='Enter',background='#8B8B7D',command=add).grid(columnspan=20,padx=10,pady=10)
                        back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(adm,'adm',(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                        
                    

                remove_adm=Button(frame3,text='Remove Admin',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('rem_admin')).grid()
                insert_adm=Button(frame3,text='Add Admin',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:operation('add_admin')).grid()
                back_bt=Button(frame3,image=pic4,background='#8B8B7D',command=lambda:back(apres_login,user,(head_label,frame3),(welcome_label,logout_bt))).grid(columnspan=20,padx=10,pady=10)
                
                
        update_pat_bt=Button(frame3,text='Patient Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('pat')).grid()
        update_doc_bt=Button(frame3,text='Doctor Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('doc')).grid()
        update_adm_bt=Button(frame3,text='Admin Info',font=('Lucida Bright',30),background='#8B8B7D',foreground='#F5F5F5',command=lambda:adm('adm')).grid()
            
  #''' if user=='Patient Login':'''  
 
    
def page(user):
    global login
    login=user
    clear((head_label,))
    root.title(login)
    frame2=Frame(root)
    frame2.pack(padx=10,pady=10)
    name_label=Label(frame2,text=login,font=('Lucida Bright',20,'underline'),foreground='#F5F5F5',background='#8B8B7D').grid(columnspan=2,padx=10,pady=10)
    user_label=Label(frame2,text='Username',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D').grid(row=1,column=0,pady=10,padx=10)
    user_entry=Entry(frame2,width=30,borderwidth=10)
    user_entry.grid(row=1,column=1,pady=10,padx=10)
    passd_label=Label(frame2,text='Password',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D').grid(row=2,column=0,pady=10,padx=10)
    passd_entry=Entry(frame2,width=30,borderwidth=10)
    passd_entry.grid(row=2,column=1,pady=10,padx=10)
    back_bt=Button(frame2,image=pic4,background='#8B8B7D',command=lambda:back(home_page,'?',(head_label,))).grid(columnspan=2,padx=10,pady=10)

    #logging in
    def login_fn():
        global username,password
        username=user_entry.get();password=passd_entry.get()
        login_dict={}
        def login_fn2(data):
             for i in data:
                login_dict[i[0]]=i[1]
             if username in login_dict:
                if password==login_dict[username]:
                    messagebox.showinfo("login", "login sucessful!!")
                    apres_login(login)
                else:
                    messagebox.showerror("login", " Wrong Password. Try again?")
             else:
                messagebox.showerror("login", "User does not exist. Try again?")
        if login=='Doctor Login':
            login_fn2(data_doc)   
        if login=='Admin Login':
            login_fn2(data_adm)
        if login=='Patient Login':
            login_fn2(data_pat)
            
    login_button=Button(frame2,text='LOGIN',font=('Lucida Bright',20),foreground='#F5F5F5',background='#8B8B7D',command=login_fn).grid(columnspan=2,padx=10,pady=10)

def home_page(m):
    root.title("Welcome Page")
    root.geometry("400x400")
    root.configure(bg='#8B8B7D')

    frame1=Frame(root)
    frame1.pack(padx=10,pady=10)

    b_doctor=Button(frame1,image=pic1,command=lambda:page('Doctor Login'))
    b_doctor.grid(row=0,column=0,padx=10,pady=10)
    l_doctor=Label(frame1,text='DOCTOR',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_doctor.grid(row=1,column=0,pady=10,padx=10)

    b_admin=Button(frame1,image=pic2,command=lambda:page('Admin Login'))
    b_admin.grid(row=0,column=1,pady=10,padx=10)
    l_admin=Label(frame1,text='ADMIN',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_admin.grid(row=1,column=1,padx=10,pady=10)

    b_patient=Button(frame1,image=pic3,command=lambda:page('Patient Login'))
    b_patient.grid(row=0,column=2,padx=10,pady=10)
    l_patient=Label(frame1,text='PATIENT',font=('Lucida Bright',15),background='#8B8B7D',foreground='#F5F5F5')
    l_patient.grid(row=1,column=2,pady=10,padx=10)

home_page('?')
      
    
    
root.mainloop()



    
