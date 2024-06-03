from tkinter import *
from tkinter import ttk
import time
import os
import shutil
from hashlib import md5

#Function to read the file and generate hash
def generate_hash(Filename:str)->str:
    block_size = 65536
    Filehash = md5()
    try:
        with open(Filename, 'rb') as File:
            fileblock = File.read(block_size)
            while len(fileblock)>0:
                Filehash.update(fileblock)
                fileblock = File.read(block_size)
            Filehash = Filehash.hexdigest()
        return Filehash
    except:
        return False
    
#Function to add hashvalue,path,date of creation/modification in dictionary 
def add(ddom, key, value)->None:
    ddom[key] = value

#Function to print cleaning summary
def summary(cnt_cleaned,sp_saved):
    count=str(cnt_cleaned)
    sp_saved = sp_saved/1048576
    sp_saved = round(sp_saved, 2)
    space=str(sp_saved)
    Label(frame3,text='-------------- FINISHED CLEANING --------------').pack()
    
    Label(frame,text='%s ' % (count)).place(x=100,y=430)
    Label(frame,text='%s MB' %(space)).place(x=100,y=450)
   

#Function to remove duplicate file 
def clean()->None:
    home_dir=var_home.get()
    File_hashes = []
    Total_bytes_saved = 0
    count_cleaned = 0
    mytext.insert(END,"Cleaning.......\n")
    all_dirs = [path[0] for path in os.walk('.')]
    for path in all_dirs:
        os.chdir(path)
        All_Files =[file for file in os.listdir() if os.path.isfile(file)]
        for file in All_Files:
            filehash = generate_hash(file)
            if not filehash in File_hashes:
                if filehash:                       
                    File_hashes.append(filehash)
                    
                        
            else:
                    
                byte_saved = os.path.getsize(file)
                count_cleaned = count_cleaned + 1
                Total_bytes_saved = Total_bytes_saved + byte_saved
                os.remove(file)
                filename = file.split('/')[-1]
                t=filename+ ".....removed\n"
                mytext.insert(END,t)
        os.chdir(home_dir)

    #Module to display memory utilization summary
    summary(count_cleaned,Total_bytes_saved)

#Function to remove duplicate file by keeping oldest file
def clean_latest()->None:
    home_dir = var_home.get()
    File_hashes = []
    fpath={}
    ddom={}
    Total_bytes_saved = 0
    count_cleaned = 0
    mytext.insert(END,"Cleaning.......\n")
    all_dirs = [path[0] for path in os.walk('.')]
    for path in all_dirs:
        os.chdir(path)
        All_Files =[file for file in os.listdir() if os.path.isfile(file)]
        for file in All_Files:
            filehash = generate_hash(file)
            if not filehash in File_hashes:
                if filehash:                       
                    File_hashes.append(filehash)
                    add(fpath,filehash,os.path.abspath(file))
                    add(ddom,filehash,time.ctime(os.path.getctime(fpath[filehash])))
                    
            else:
                dom=ddom[filehash]
                cdom=time.ctime(os.path.getctime(file))
                ldom=max(dom,cdom)
                if cdom==ldom:
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    t=filename+ ".....removed\n"
                    mytext.insert(END,t)
                elif dom==ldom:
                    temp=file
                    file = fpath[filehash]
                    fpath[filehash]=temp
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    t=filename+ ".....removed\n"
                    mytext.insert(END,t)
        os.chdir(home_dir)

    #Module to display memory utilization summary
    summary(count_cleaned,Total_bytes_saved) 


#Function to delete oldest duplicate files
def clean_old()->None:
    home_dir = var_home.get()
    File_hashes = []
    fpath={}
    ddom={}
    Total_bytes_saved = 0
    count_cleaned = 0
    mytext.insert(END,"Cleaning......\n")
    all_dirs = [path[0] for path in os.walk('.')]
    for path in all_dirs:
        os.chdir(path)
        All_Files =[file for file in os.listdir() if os.path.isfile(file)]
        for file in All_Files:
            filehash = generate_hash(file)
            if not filehash in File_hashes:
                if filehash:                       
                    File_hashes.append(filehash)
                    add(fpath,filehash,os.path.abspath(file))
                    add(ddom,filehash,time.ctime(os.path.getctime(fpath[filehash])))   #print(file)
            else:
                dom=ddom[filehash]
                cdom=time.ctime(os.path.getctime(file))
                odom=min(dom,cdom)
                if cdom==odom:
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    t=filename+ ".....removed\n"
                    mytext.insert(END,t)
                elif dom==odom:
                    temp=file
                    file = fpath[filehash]
                    fpath[filehash]=temp
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    t=filename+ ".....removed\n"
                    mytext.insert(END,t)

        os.chdir(home_dir)
    #Module to display memory utilization summary
    summary(count_cleaned,Total_bytes_saved) 

#function to reset the interface
def resetAll():
    master.destroy()
    os.startfile("gui_dfr.py")


#main 
def main():
    try:
        selected_choice= radio.get()
        if selected_choice == 1:
           time.sleep(3)
           clean_latest()
        elif selected_choice == 2:
           time.sleep(3)
           clean_old()
    except:
        time.sleep(3)
        clean()

#Module for graphical user inetrface using tkinter 
master =Tk()

frame = LabelFrame(master, width=500, height=500)
frame.grid(row=0, column=0, padx=10, pady=5)

l1=Label(master, text ='Duplicate File Remover',font=("Arial 20"), borderwidth=1).place(x=120,y=10)

var_home=StringVar()
l2=Label(frame,text="Enter the directory").place(x=7,y=70)
e1=Entry(frame,width="44",textvariable=var_home).place(x=200,y=70)


l3=Label(frame,text="Keep oldest or latest file").place(x=7,y=90)

radio=IntVar()
r1=Radiobutton(frame, text="Oldest", variable=radio, value=1).place(x=200,y=90)
r2=Radiobutton(frame, text="Latest", variable=radio, value=2).place(x=280,y=90)


b1=Button(frame,text="Start",command=main).place(x=7,y=120,width=40)

clearall = Button(frame, text='Reset', command=resetAll).place(x=50,y=120,width=40)


frame2=LabelFrame(frame)
frame2.place(x=7,y=150)

mycanvas=Canvas(frame2,width=464,height=240,bg="white")
mycanvas.pack(side=LEFT)
yscrollbar= ttk.Scrollbar(frame2,orient="vertical",command=mycanvas.yview)
yscrollbar.pack(side=RIGHT,fill="y")
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

myframe= Frame(mycanvas)
mycanvas.create_window((0,0),window=myframe,anchor="nw")

mytext=Text(myframe)
mytext.pack(fill=BOTH,expand=0)

frame3=Frame(frame, width=464, height=20)
frame3.place(x=7,y=410)

l5=Label(frame,text= "Files Cleaned    " ).place(x=7,y=430)
l6=Label(frame,text= "Memory Saved      ").place(x=7,y=450)

#Defining interface dimensions and other properties
master.geometry("520x520")
master.resizable(False,False)
master.title("Duplicate File Remover")
master.config(bg="skyblue")
master.mainloop()