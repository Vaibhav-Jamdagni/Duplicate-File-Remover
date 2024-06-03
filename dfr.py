import time
import os
from hashlib import md5


#Welcome Message
def welcome()->None:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('|                                                                   |')
    print('|                            WELCOME                                |')
    print('|                              TO                                   |')
    print('|                     DUPLICATE FILE REMOVER                        |')
    print('|                                                                   |')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
    time.sleep(3)


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

#Function to take user's choice to keep old or latest duplicate file 
def choice()->str:
    selected=input("Do you want to keep the 'Oldest' or 'Latest' file : ")
    return selected

#Function to remove duplicate file 
def clean()->None:
    home_dir = os.getcwd()
    File_hashes = []
    Total_bytes_saved = 0
    count_cleaned = 0
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
                print(filename,path, '....... removed ')
                
        os.chdir(home_dir)

    #Module to display memory utilization summary
    mb_saved = Total_bytes_saved/1048576
    mb_saved = round(mb_saved, 2)
    print('\n\n------------FINISHED CLEANING ------------')
    print('|                                             |')
    print('|  File cleaned      :  ', count_cleaned)
    print('|                                             |')
    print('|  Total Space saved :  ', mb_saved, 'MB')
    print('|                                             |')
    print('---------------------------------------------- ') 

#Function to delete latest duplicate file
def clean_latest()->None:
    home_dir = os.getcwd()
    File_hashes = []
    fpath={}
    ddom={}
    Total_bytes_saved = 0
    count_cleaned = 0
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
                    print(filename,path, '....... removed ')
                elif dom==ldom:
                    temp=file
                    file = fpath[filehash]
                    fpath[filehash]=temp
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    print(filename,path, '....... removed ') 
        os.chdir(home_dir)

    #Module to display memory utilization summary
    mb_saved = Total_bytes_saved/1048576
    mb_saved = round(mb_saved, 2)
    print('\n\n------------FINISHED CLEANING ------------')
    print('|                                             |')
    print('|  File cleaned      :  ', count_cleaned)
    print('|                                             |')
    print('|  Total Space saved :  ', mb_saved, 'MB')
    print('|                                             |')
    print('---------------------------------------------- ') 


#Function to delete oldest duplicate files
def clean_old()->None:
    home_dir = os.getcwd()
    File_hashes = []
    fpath={}
    ddom={}
    Total_bytes_saved = 0
    count_cleaned = 0
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
                    print(filename,path, '....... removed ')
                elif dom==odom:
                    temp=file
                    file = fpath[filehash]
                    fpath[filehash]=temp
                    byte_saved = os.path.getsize(file)
                    count_cleaned = count_cleaned + 1
                    Total_bytes_saved = Total_bytes_saved + byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    print(filename,path, '....... removed ') 
                    
        os.chdir(home_dir)
    #Module to display memory utilization summary
    mb_saved = Total_bytes_saved/1048576
    mb_saved = round(mb_saved, 2)
    print('\n\n------------FINISHED CLEANING ------------')
    print('|                                             |')
    print('|  File cleaned      :  ', count_cleaned)
    print('|                                             |')
    print('|  Total Space saved :  ', mb_saved, 'MB')
    print('|                                             |')
    print('---------------------------------------------- ') 

    
#Defining program entry point
def main()->None:
    welcome()
    try:
        selected_choice= choice().upper()
        if selected_choice == "OLDEST":
            print("You kept oldest files ")
            time.sleep(3)
            print('\nCleaning .................')
            clean_latest()
        elif selected_choice == "LATEST":
            print("You kept latest file")
            time.sleep(3)
            print('\nCleaning .................')
            clean_old()
    except:
        time.sleep(3)
        print('\nCleaning .................')
        clean()

    

#Calling main
main()