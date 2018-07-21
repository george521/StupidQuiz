import threading
import time
import random
import tkinter as tk
from tkinter import *
options = "1. Start Quiz","2. LeaderBoard","3. Import new Question","4. Quit Game"

def main():
    #main menu
    while True:
        for i in options:
            print(i)
        x=input()
        if x=="1":
            del plist[:]
            for i in range(0,len(qlist),1):
                plist.append(False)
            d=input("Name: ")
            stquiz(d)
        elif x=="2":
            leaderb()
        elif x=="3":
            qg=input("Give your question:\t")
            ag=input("Give the answer to the question:\t")
            ImportQA(qg,ag)
        elif x=="4":
            exit()
        else:
            print("Invalid choice")
#global variables
plist = []
qlist = []
alist = []
leadboard=[[],[]]
names=[]
points=[]
bonus=["Panflo"]

class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.name = name

    def run(self):
        #Countdown Timer for 1 minute
        t0=time.localtime(time.time()) 
        while True:
            t1=time.localtime(time.time()) 
            if t0.tm_min!=t1.tm_min and t0.tm_sec==t1.tm_sec:
                break
        self.name="thread2"

def stquiz(d):
    score=0
    #initialize threadz
    threadz = myThread("Thread1")
    threadz.start()
    threadz.lock.acquire()
    for k in range (0,5,1):
        rand=Randomizer()
        threadz.name="Thread1"
        print("Question: "+ qlist[rand])
        answer=input("\nWrite your answer: ")
        print("\n")
        #Checking if answer is correct and 1 minute has not passed
        if str(answer)==alist[rand] and str(threadz.getName())=="Thread1":
            score = score + 10
        elif str(answer)==bonus[0]:
            score = score + 10000
        else:
            continue
    threadz.lock.release()
    leadboard[0].append(d)
    leadboard[1].append(score)
    quicksort(leadboard,0,len(leadboard[0])-1)    
    leadboard[0].reverse()
    leadboard[1].reverse()
    saveFile()

    
def leaderb():
    
    #printing the top 10 players or less if not 10
    top=len(leadboard[0])if len(leadboard[0])<=10 else 10
    for i in range(0,top,1):
        print(str(leadboard[0][i])+"\t"+str(leadboard[1][i]))
    print("\n")

def quicksort(a,ls,rs):
    #Simple quicksort for a 2D list
    if ls<rs:
        l=ls
        r=rs
        p=a[1][rs]
        p2=a[0][rs]
        while l<r:
            while l<r and int(a[1][l])<=int(p) :
                l=l+1
            while r>l and int(a[1][r])>=int(p) :
                r=r-1
            if l<r:
                t1=a[1][l]
                t2=a[0][l]
                a[1][l]=a[1][r]
                a[0][l]=a[0][r]
                a[1][r]=t1
                a[0][r]=t2
        a[1][rs]=a[1][l]
        a[0][rs]=a[0][l]
        a[1][l]=p
        a[0][l]=p2
        quicksort(a,ls,l-1)
        quicksort(a,l+1,rs)

#Function for randomizing the questions
def Randomizer():
    while True:
        a=random.randint(0,len(qlist)-1)
        if plist[a]==False:
            plist[a]=True
            return a    

#Function for importing new questions
def ImportQA(question,answer):
    qlist.append(question)
    alist.append(answer)
    try:
        with open("questions_answers.txt","w",encoding="ansi") as f:
            for i in range(0,len(qlist),1):
                f.write(str(qlist[i])+";"+str(alist[i])+";\n")
    except IOError:
        print ("Error: can\'t find file questions_answers.txt")

    
#Saving into LeaderBoard.txt            
def saveFile():
    top=len(leadboard[0])if len(leadboard[0])<=10 else 10
    with open("LeaderBoard.txt","w",encoding="ansi") as f:
        for i in range(0,top,1):
            f.write(str(leadboard[0][i])+"\t")
            f.write(str(leadboard[1][i])+"\n")
    

#Reading from LeaderBoard.txt and creating it if it doesn't exist  
def readLeadboard():
    try:
        with open("LeaderBoard.txt","r",encoding="ansi") as f:
            for line in f:
                data=line.split()
                leadboard[0].append(data[0])
                leadboard[1].append(data[1])
    except IOError:
        with open("LeaderBoard.txt","w",encoding="ansi") as f:
            print("Creating LeaderBoard.txt")

#Reading from questions_answers.txt             
def readtxt():
    try:
        with open("questions_answers.txt","r",encoding="ansi") as f:
            for line in f:
                data2=line.split(";")
                if data2==[]:
                    print("Error 1")
                    exit()
                qlist.append(data2[0])
                alist.append(data2[1])
    except IOError:
        print ("Error: can\'t find file questions_answers.txt")


class MainPage:
    def __init__(self,master):
        self.master = master
        self.master.title("Main Menu")
        self.frame =tk.Frame(self.master)
        self.button1 = tk.Button(self.frame,text="Start Game",width = 30, command = self.StartGame_window)
        self.button1.pack()
        self.button2 = tk.Button(self.frame,text="Leaderboard",width = 30, command = self.LeaderBoard_window)
        self.button2.pack()
        self.button3 = tk.Button(self.frame,text="New Question",width = 30, command = self.ImportQuestion_window)
        self.button3.pack()
        self.button4 = tk.Button(self.frame,text="Quit Game",width = 30, command = lambda:self.master.destroy() )
        self.button4.pack()
        self.frame.pack()

    def StartGame_window(self):
        self.StartGame_window = tk.Toplevel(self.master)
        self.app = StartGame(self.StartGame_window)

    def LeaderBoard_window(self):
        self.LeaderBoard_window = tk.Toplevel(self.master)
        self.app = LeaderBoard(self.LeaderBoard_window)

    def ImportQuestion_window(self):
        self.ImportQuestion_window = tk.Toplevel(self.master)
        self.app = ImportQuestion(self.ImportQuestion_window)

class StartGame:
    def __init__(self,master):
        self.master = master
        self.master.title("Start Game")
        self.frame = tk.Frame(self.master)
        v = StringVar()
        self.e3 = tk.Entry(self.master,textvariable=v)
        self.e3.pack()
        v.set("Player Name")
        self.mbutton = tk.Button(self.frame,text = "Go!", width =30 , command = self.master.destroy() )
        self.mbutton.pack()
        self.frame.pack()


class LeaderBoard:
    def __init__(self,master):
        self.master = master
        self.master.title("Leaderboard")
        self.frame = tk.Frame(self.master)
        for i in range(0,len(leadboard[0]),1):
            tk.Label(self.master,text=leadboard[0][i]+"\t"+leadboard[1][i]).pack()
        self.qbutton = tk.Button(self.frame,text = "Back", width =30 , command = lambda:self.master.destroy() ).pack()
        self.frame.pack()

class ImportQuestion:
    def __init__(self,master):
        self.master = master
        self.master.title("New Questions")
        self.frame = tk.Frame(self.master)
        self.label1 = tk.Label(self.master,text="Question: ")
        self.label1.pack()
        self.e1 = tk.Entry(self.master)
        self.e1.pack()
        self.label2 = tk.Label(self.master,text="Answer: ")
        self.label2.pack()
        self.e2 = tk.Entry(self.master)
        self.e2.pack()
        self.qbutton = tk.Button(self.frame,text = "Back", width =30 , command = self.ImportQA2).pack()
        self.frame.pack()

    def ImportQA2(self):
        if self.e1.get()=="" or self.e2.get()=="":
            self.master.destroy()
        else:
            qlist.append(self.e1.get())
            alist.append(self.e2.get())
            try:
                with open("questions_answers.txt","w",encoding="ansi") as f:
                    for i in range(0,len(qlist),1):
                        f.write(str(qlist[i])+";"+str(alist[i])+";\n")
            except IOError:
                print ("Error: can\'t find file questions_answers.txt")
            
            self.master.destroy()

readLeadboard()
readtxt()
    
root =tk.Tk()
app=MainPage(root)
root.mainloop()
