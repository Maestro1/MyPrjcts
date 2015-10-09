#!/usr/bin/env python3
#Chat client Gui program

#Import necessary modules
from tkinter import *
from threading import Thread
from time import asctime,localtime
from socket import *
from select import select

#Create custom Text widget class that subclasses Frame widget class with methods to update and clear text in the widget
class ScrolledText(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent)
        self.grid(sticky=N+S+E+W)
        self.text=Text(self,*args,**kwargs)
        self.text.configure(wrap=WORD)
        self.scroll=Scrollbar(self,orient="vertical",command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.grid(row=0,column=0,columnspan=4,sticky=N+S+E+W)
        self.scroll.grid(row=0,column=4,sticky=N+S)
        self.text.configure(bg="black",fg="green")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.insert=self.text.insert
        self.delete=self.text.delete
        self.mark_set=self.text.mark_set
        self.get=self.text.get
        self.index=self.text.index
        self.search=self.text.search
        
    def update_text(self,mssg):
        self.mssg=mssg
        self.insert(END,mssg)
    def clear_text(self):
        self.delete("0.0",END)
        
#Class that subclasses Frame class widget
#Used to create the application that holds all the widgets.
#Contains methods to create and initialize widgets,create a connection to the server as well as send and receive data from the server        
class MyApp(Frame):
    #to test for local host
    HOST='127.0.0.1'
    #For networked devices
    #HOST=sock.gethostbyname(sock.gethostname())
    PORT=2457
    BUFSIZ=1024
    sock=socket(AF_INET,SOCK_STREAM)
    writable_list=[sock]
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        parent.title("IRC CHAT CLIENT")
        self.grid(row=0,column=0,sticky=N+S+W+E)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.initUI()
        self.connect()
        self.recv_data()
        
   
    def send_data(self,data):
        self.data=data
        self.hst=self.HOST
        try:
            self.t=localtime()
            self.tym=asctime(self.t)
            fdata="\n[%s]From:%s >>> "%(self.tym,self.hst)+data
            self.scrlldtxt.update_text(fdata)
            fdata=fdata.encode('utf-8')
            self.sock.send(fdata)
        except Exception as e:
            self.scrlldtxt.update_text(e)     
    def initUI(self):
        self.scrlldtxt=ScrolledText(self)
        self.scrlldtxt.grid(row=0,column=0,sticky=N+S+E+W)
        self.labl=Label(self,text="Enter your message")
        self.labl.grid(sticky=N+S+W+E)
        self.msg=Entry(self)
        self.msg.grid(row=2,column=0,sticky=E+W,columnspan=4)
        #Use threads to send data to ensure the graphical user interface does not freeze since sending data could take time due to issues such as slow connection 
        self.send_button=Button(self,text="send",default="active",command=lambda:Thread(target=self.send_data,args=(self.msg.get(),)).start())
        self.send_button.grid(row=3,column=0,sticky=W+E)
        self.quit_button=Button(self,text="quit",command=quit)
        self.quit_button.grid(row=3,column=1,sticky=W+E)
        self.clear_button=Button(self,text="clear",command=self.scrlldtxt.clear_text)
        self.clear_button.grid(row=3,column=2,sticky=W+E)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
       
    def connect(self):
        try:
            self.sock.connect((self.HOST,self.PORT))
            cxn="Connection established successfully to server\n"
            self.scrlldtxt.update_text(cxn)
        except Exception as e:
            #err_mssg="Failed to connect.Error Code:"+str(e[0])+"Error Message: "+str(e[1])
            self.scrlldtxt.update_text(e)
            return
           
    def recv_data(self):
        #select method ensures that the socket is non blocking
        self.readable,self.writable,self.errord=select([],self.writable_list,[],60)
        for s in self.writable:
            rcvd=s.recv(self.BUFSIZ).decode("utf-8")
        self.scrlldtxt.update_text(rcvd)
         




#Creates root window
        
if __name__=="__main__":
    main=Tk()
    main.rowconfigure(0,weight=1)
    main.columnconfigure(0,weight=1)
    
    MyApp(main)
    main.mainloop()
