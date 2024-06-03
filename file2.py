import time
import os
import shutil
from hashlib import md5

class Duplicate:
    def __init__(self):
        self.home_dir = os.getcwd()
        self.File_hashes = []
        self.Cleaned_dirs = []
        self.Total_bytes_saved = 0
        self.block_size = 65536
        self.count_cleaned = 0
        self.ddom= dict()

    def welcome(self)->None:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('|                            WELCOME                                |')
        print('|                              TO                                   |')
        print('|                     DUPLICATE FILE REMOVER                        |')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        time.sleep(3)
        print('\nCleaning .................')

    def generate_hash(self, Filename:str)->str:
        Filehash = md5()
        try:
            with open(Filename, 'rb') as File:
                fileblock = File.read(self.block_size)
                while len(fileblock)>0:
                    Filehash.update(fileblock)
                    fileblock = File.read(self.block_size)
                Filehash = Filehash.hexdigest()
            return Filehash
        except:
            return False
    
    def add(self, key, value)->None:
        self.ddom[key] = value

    def choice(self)->str:
        selected=input("Do you want to keep the 'Oldest' or 'Latest' file : ")
        return selected

    def clean(self)->None:
        all_dirs = [path[0] for path in os.walk('.')]
        for path in all_dirs:
            os.chdir(path)
            All_Files =[file for file in os.listdir() if os.path.isfile(file)]
            for file in All_Files:
                filehash = self.generate_hash(file)
                if not filehash in self.File_hashes:
                    if filehash:                       
                        self.File_hashes.append(filehash)
                        self.add(filehash, file)
                        
                else:
                    dom=time.ctime(os.path.getmtime(self.ddom[filehash]))
                    cdom=time.ctime(os.path.getmtime(file))
                    print(dom,cdom)
                    ldom=max(dom,cdom)
                    if cdom==ldom:
                        byte_saved = os.path.getsize(file)
                        self.count_cleaned+=1
                        self.Total_bytes_saved+=byte_saved
                        os.remove(file)
                        filename = file.split('/')[-1]
                        print(filename,path, '.. cleaned ')
                    elif dom==ldom:
                        file = self.ddom[filehash]
                        byte_saved = os.path.getsize(file)
                        self.count_cleaned+=1
                        self.Total_bytes_saved+=byte_saved
                        os.remove(file)
                        filename = file.split('/')[-1]
                        print(filename,path, '.. cleaned ') 
            os.chdir(self.home_dir)

    def clean_old(self)->None:
        all_dirs = [path[0] for path in os.walk('.')]
        for path in all_dirs:
            os.chdir(path)
            All_Files =[file for file in os.listdir() if os.path.isfile(file)]
            for file in All_Files:
                filehash = self.generate_hash(file)
                if not filehash in self.File_hashes:
                    if filehash:                       
                        self.File_hashes.append(filehash)
                        self.add(filehash, file)
                        #print(file)
                else:
                    dom=time.ctime(os.path.getmtime(self.ddom[filehash]))
                    cdom=time.ctime(os.path.getmtime(file))
                    odom=min(dom,cdom)
                    if cdom==odom:
                        byte_saved = os.path.getsize(file)
                        self.count_cleaned+=1
                        self.Total_bytes_saved+=byte_saved
                        os.remove(file)
                        filename = file.split('/')[-1]
                        print(filename,path, '.. cleaned ')
                    elif dom==odom:
                        file = self.ddom[filehash]
                        byte_saved = os.path.getsize(file)
                        self.count_cleaned+=1
                        self.Total_bytes_saved+=byte_saved
                        os.remove(file)
                        filename = file.split('/')[-1]
                        print(filename,path, '.. cleaned ') 
                    
            os.chdir(self.home_dir)
    
    def cleaning_summary(self)->None:
        mb_saved = self.Total_bytes_saved/1048576
        mb_saved = round(mb_saved, 2)
        print('\n\n------------FINISHED CLEANING ------------')
        print('File cleaned      : ', self.count_cleaned)
        print('Total Space saved : ', mb_saved, 'MB')
        print('-----------------------------------------------')
    
    def main(self)->None:
        self.welcome()
        selected_choice=self.choice().upper()
        if selected_choice == "OLDEST":
            print("You kept oldest files ")
            self.clean()
        elif selected_choice == "LATEST":
            print("You kept latest file")
            self.clean_old()
        self.cleaning_summary()

if __name__ == '__main__':
    App = Duplicate()
    App.main()