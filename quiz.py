import tkinter as tk            
from tkinter import *
import time
import random

#global variables
plist = []
qlist = []
alist = []
leadboard=[[],[]]
names=[]
points=[]
bonus=["Panflo"]

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

troll=0
troll_list=["Good job Stupid","Did you just clicked again?","Really m8?","Aren't you bored of this?","I am certainly not","I hope you don't disappoint me","Keep trying","Better luck next time","Are you mad bro?","Ok I am done","Did you believe me?","OK now I am done","Or so I thought","I am sorry fred","but","all good things come to an end","Your reward for clicking this much","is Panflo"]
#initialize t1,t0        
t1=0.0
t0=0.0


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("StupidQuiz") 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        xaxis =(screen_width/2)-(300/2)
        yaxis = (screen_height/2)-(350/2)
        self.geometry("+%d+%d"%(xaxis,yaxis)) # make the window appear in the center of the screen

 
        # this container contains all the pages
        global container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   
        container.grid_columnconfigure(0,weight=1) 
        self.frames = {} # dictionary to keep the pages
 
        for F in (StartPage, StartGame,LeaderBoard,ImportQuestion): 
            frame = F(container, self) # create the page
            self.frames[F] = frame  
            frame.grid(row=0, column=0, sticky="nsew") 
 
        self.show_frame(StartPage) # setting StartPage as first page

    #showing the named frame
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    #destroying the named frame
    def destroy_frame(self,name):
        
        frame = self.frames[name]
        frame.grid_forget()
        frame.destroy()
    #recreating the named frame
    def add_frame(self,name):
        del plist[:]
        for i in range(0,len(qlist),1):
            plist.append(False)
        frame = name(container,self)
        self.frames[name]=frame
        frame.grid(row=0, column=0, sticky="nsew")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="silver")
        label = tk.Label(self, text="Main Menu",bg="black",fg="violet",font=("Times New Roman",30))
        label.pack(side="top", fill="x", pady=20)

        button1 = tk.Button(self, text="StartGame",bg="black",fg="violet",width = 30,height=3, command=lambda: controller.show_frame(StartGame))
        button2 = tk.Button(self, text="Leaderboard",bg="black",fg="violet", width = 30,height=3,command=lambda: controller.show_frame(LeaderBoard))
        button3 = tk.Button(self, text="New Question",bg="black",fg="violet", width = 30,height=3,command=lambda: controller.show_frame(ImportQuestion))
        button4 = tk.Button(self, text="Quit Game",bg="black",fg="violet",width = 30,height=3, command=lambda: controller.destroy())
        
        button1.pack()
        button2.pack(pady=10)
        button3.pack()
        button4.pack(pady=10)


class StartGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="silver")
        self.name_label = tk.Label(self,text="Player Name",bg='black',width=20,font=("Times New Roman", 20),fg='violet')
        self.name_label.pack(pady=20)
        name_text = tk.StringVar()
        name_text.set("")
        self.Player_name = tk.Entry(self,textvariable=name_text)
        self.Player_name.pack()
        del plist[:]
        for i in range(0,len(qlist),1):
            plist.append(False)
        self.cheatbutton = tk.Button(self,text = "Go!", width =10 ,height=2,fg='violet', bg='black',font=("Times New Roman", 10),  command = lambda:self.gameplay(name_text.get(),controller) )
        self.cheatbutton.pack(pady=20)
        

    def gameplay(self,name_text,controller):
        self.name_label.destroy()
        self.Player_name.destroy()
        if name_text=="":
            name_text="Player"
        self.cheatbutton.configure(text="Click if you are Stupid",width=20,height=1,font=("Times New Roman", 20),command=lambda:self.Cheats(troll))
        self.score=0
        stop_variable = tk.BooleanVar()
        label_text = tk.StringVar()
        entry_text = tk.StringVar()
        t0=time.time()
        rand=Randomizer()
        label_text.set(qlist[rand])
        self.questionlabel = tk.Label(self,textvariable=label_text,bg='black',font=("Times New Roman", 16),fg='violet')
        self.questionlabel.pack()
        entry_text.set("")
        self.answer = tk.Entry(self,textvariable=entry_text)
        self.answer.pack(pady=20)
        #submit checkbutton
        self.fuckingbutton = tk.Checkbutton(self, text="Submit", variable=stop_variable ,onvalue=True, offvalue=False,bg='black',fg='violet',font=("Times New Roman", 14))
        self.fuckingbutton.pack()
        self.fuckingbutton.wait_variable(stop_variable )
        t1=time.time()
        self.fuckingbutton.bind(self.PointsCalculator(rand,t1-t0)) #wait to submit the answer
        for k in range (1,5,1):     
            t0=time.time()
            rand=Randomizer()
            label_text.set(qlist[rand])
            entry_text.set("")
            stop_variable.set(False)
            self.fuckingbutton.wait_variable(stop_variable )
            t1=time.time()
            self.fuckingbutton.bind(self.PointsCalculator(rand,t1-t0))        
            
        leadboard[0].append(name_text)
        leadboard[1].append(self.score)
        quicksort(leadboard,0,len(leadboard[0])-1)    
        leadboard[0].reverse()
        leadboard[1].reverse()
        saveFile()

        controller.destroy_frame(StartGame)
        controller.add_frame(StartGame)
        controller.destroy_frame(LeaderBoard)
        controller.add_frame(LeaderBoard)
        controller.show_frame(StartPage)
              

    def PointsCalculator(self,rand,time):
        #Checking if answer is correct and 1 minute has not passed
        if str(self.answer.get())==alist[rand] and time<60.0:
            self.score = self.score + 10
        elif str(self.answer.get())==bonus[0]:
            self.score = self.score + 10000

    def Cheats(self,troll):
        try:
            self.cheatbutton.configure(width=30,text=troll_list[troll],command=lambda:self.Cheats(troll+1))
        except IndexError:
            self.cheatbutton.configure(width=30,text=troll_list[len(troll_list)-1],command=lambda:self.Cheats(len(troll_list)-1))
        

class LeaderBoard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="silver")
        self.lead_label = tk.Label(self,text="Leaderboard",bg='black',width=20,font=("Times New Roman", 20),fg='violet')
        self.lead_label.pack()
        top=len(leadboard[0])if len(leadboard[0])<=10 else 10
        for i in range(0,top,1):
            self.playerranking=tk.Label(self,text="\n"+str(i+1)+". "+str(leadboard[0][i])+"\t"+str(leadboard[1][i]),fg='black',bg='silver',font=("Times New Romans", 12))
            self.playerranking.pack()
        
        self.returnbutton = tk.Button(self,text = "Back", width =10,font=("Times New Roman", 14) , fg='violet', bg='black',command = lambda:controller.show_frame(StartPage) )
        self.returnbutton.pack(pady=10,side="bottom")


class ImportQuestion(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="silver")
        self.writtenquestion = tk.Label(self,text="Question: ",bg='black',width=15,font=("Times New Roman", 20),fg='violet')
        self.writtenquestion.pack(fill="x",pady=20)
        self.e1 = tk.Entry(self)
        self.e1.pack(padx=20, fill="x")
        self.writtenanswer = tk.Label(self,text="Answer: ",bg='black',width=15,font=("Times New Roman", 20),fg='violet')
        self.writtenanswer.pack(fill="x",pady=20)
        self.e2 = tk.Entry(self)
        self.e2.pack(padx=20, fill="x")
        self.returnbutton2 = tk.Button(self,text = "Back", width =10,font=("Times New Roman", 14) ,bg='black',fg='violet', command = lambda:self.UpdateQuestions(controller))
        self.returnbutton2.pack(pady=10,side="bottom")

    def UpdateQuestions(self,controller):
        if self.e1.get()=="" or self.e2.get()=="":
            controller.destroy_frame(ImportQuestion)
            controller.add_frame(ImportQuestion)
            controller.show_frame(StartPage)
        else:
            qlist.append(self.e1.get())
            alist.append(self.e2.get())
            try:
                with open("questions_answers.txt","w",encoding="ansi") as f:
                    for i in range(0,len(qlist),1):
                        f.write(str(qlist[i])+";"+str(alist[i])+";\n")
            except IOError:
                print ("Error: can\'t find file questions_answers.txt")
            controller.destroy_frame(ImportQuestion)
            controller.add_frame(ImportQuestion)
            controller.show_frame(StartPage)

if __name__ == "__main__":
    readLeadboard()
    readtxt()    
    app = MainWindow()
    app.mainloop()
