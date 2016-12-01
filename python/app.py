from tkinter import *
from tkinter import messagebox
import pymysql


class App:

    def __init__(self):
        self.LoginPage()

    def LoginPage(self):
        self.rootWin = Tk()
        self.rootWin.wm_title("CS 4400 Phase 3")

        Label(self.rootWin, text='Username').grid(row=1, column=0, sticky=E)
        Label(self.rootWin, text='Password').grid(row=2, column=0, sticky=E)

        self.eUsername = Entry(self.rootWin)
        self.eUsername.grid(row=1, column=1)

        self.ePassword = Entry(self.rootWin)
        self.ePassword.grid(row=2, column=1)

        register = Button(self.rootWin, text='Register', command=self.Register)
        register.grid(row=3, column=1, sticky=E)

        login = Button(self.rootWin, text='Login', command=self.LoginCheck)
        login.grid(row=3, column=2)

        self.rootWin.mainloop()

    # To create a new window
    # self.rootWin.destroy()
    # self.root = Tk()
    # self.root.wm_title("CS 4400 Phase 3")
    def Register(self):
        self.rootWin.destroy()
        self.root = Tk()
        self.root.wm_title("New Student Registration")

        Label(self.root, text='Username').grid(row=1, column=0, sticky=W)
        Label(self.root, text='Email').grid(row=2, column=0, sticky=W)
        Label(self.root, text='Password').grid(row=3, column=0, sticky=W)
        Label(self.root, text='Confirm Password').grid(
            row=4, column=0, sticky=W)

        self.eUser = Entry(self.root)
        self.eUser.grid(row=1, column=1)

        self.eEmail = Entry(self.root)
        self.eEmail.grid(row=2, column=1)

        self.ePass = Entry(self.root)
        self.ePass.grid(row=3, column=1)

        self.eCPass = Entry(self.root)
        self.eCPass.grid(row=4, column=1)

        # cancel = Button(self.root, text='Cancel', command=self.LoginPage)
        # cancel.grid(row=6, column=1, sticky=E)

        register = Button(self.root, text='Register', command=self.RegisterNew)
        register.grid(row=6, column=2)

        self.root.mainloop()

    def RegisterNew(self):

        self.Connect()

        user = self.eUser.get()
        email = self.eEmail.get()
        password = self.ePass.get()
        cPassword = self.eCPass.get()

        if user == '':
            messagebox.showwarning("Whoops!", "Please enter a username")
            return

        if email == '':
            messagebox.showwarning("Whoops!", "Please enter an Email")
            return

        if password == '' or cPassword == '':
            messagebox.showwarning(
                "Whoops!", "Please fill out the password forms")
            return

        if password != cPassword:
            messagebox.showwarning("Whoops!", "Make sure your passwords match")
            return

        userCheck = "SELECT Username FROM User WHERE Username = %s"
        myUserCheck = self.cursor.execute(userCheck, (user,))

        emailCheck = "SELECT Email FROM User WHERE Email = %s"
        myEmailCheck = self.cursor.execute(emailCheck, (email,))

        if myUserCheck >= 1:
            messagebox.showwarning(
                "Whoops!", "This username is already in use! Please choose another username.")
        elif myEmailCheck >= 1:
            messagebox.showwarning(
                "Whoops!", "This email is already in use! Please choose another email.")
        else:
            sql = 'INSERT INTO User (Username, Password, Email) VALUES (%s, %s, %s)'
            self.cursor.execute(sql, (user, password, email))
            messagebox.showinfo("Congratulations!",
                                "You have successfully registered!")
            self.db.commit()
            self.root.destroy()
            self.LoginPage()

        self.cursor.close()
        self.db.close()

    def LoginCheck(self):
        self.Connect()

        user = self.eUsername.get()
        password = self.ePassword.get()

        userCheck = "SELECT Username, Password FROM User WHERE Username = %s AND Password = %s"
        myUserCheck = self.cursor.execute(userCheck, (user, password))
        if myUserCheck == 1:
            messagebox.showinfo("Hello", "Welcome to The Database")
            getAdmin = "SELECT admin FROM User WHERE Username = %s AND Password = %s"
            self.cursor.execute(getAdmin, (user, password))
            admin = self.cursor.fetchone()[0]
            self.rootWin.destroy()
            if admin == 1:
                self.AdminMainPage()
            else:
                self.MainPage()
        else:
            messagebox.showwarning(
                "Whoops!", "Either your username or password was entered incorrectly")

        self.cursor.close()

    def MainPage(self):
        self.root = Tk()
        self.root.wm_title("Main Page")
        self.cursor = self.db.cursor()

        def addcatrow():
            print("hello")

        # row 1
        mePage = Button(self.root, text='Me', command=self.MePage)
        mePage.grid(row=1, column=0, sticky=W)
        Label(self.root, text='Main Page').grid(row=1, column=1, sticky=W)
        # row 2
        Label(self.root, text='Title').grid(row=2, column=0, sticky=W)
        self.eTitle = Entry(self.root)
        self.eTitle.grid(row=2, column=1)
        Label(self.root, text='Category').grid(row=2, column=2, sticky=W)
        # Categories = self.cursor.execute("SELECT DISTINCT Category FROM Projects, Courses")
        # Categories = self.cursor.fetchall()
        CatVar = StringVar(self.root)
        CatVar.set("Please Select")
        CatDrop = OptionMenu(self.root, CatVar, 'Categories')
        CatDrop.grid(row=2, column=3, padx=1, pady=1)
        AddCat = Button(self.root, text="Add Another Category",
                        fg='blue', relief='flat', command=addcatrow)
        AddCat.grid(row=2, column=4)

        Label(self.root, text='Designation').grid(row=3, column=0, sticky=W)
        Label(self.root, text='Major').grid(row=4, column=0, sticky=W)
        Label(self.root, text='Year').grid(row=5, column=0, sticky=W)
        DesVar = StringVar(self.root)
        DesVar.set("Please Select")
        MaVar = StringVar(self.root)
        MaVar.set("Please Select")
        YearVar = StringVar(self.root)
        YearVar.set("Please Select")
        YearOpt = ["Freshman", "Sophomore", "Junior", "Senior"]
        # Designations = self.cursor.execute("SELECT DISTINCT Designation FROM Projects, Courses")
        # Designations = self.cursor.fetchall()
        # Majors = self.cursor.execute("SELECT DISTINCT Major FROM Projects, Courses")
        # Majors = self.cursor.fetchall()
        DesDrop = OptionMenu(self.root, DesVar, 'Designations')
        DesDrop.grid(row=3, column=1, padx=1, pady=1)

        MajDrop = OptionMenu(self.root, MaVar, 'Majors')
        MajDrop.grid(row=4, column=1, padx=1, pady=1)

        YearDrop = OptionMenu(self.root, YearVar, *YearOpt)
        YearDrop.grid(row=5, column=1, padx=1, pady=1)

        ProjCorBo = StringVar(self.root)
        ProjCorBo.set("Both")
        ProjCorButtonOne = Radiobutton(
            self.root, text="Course", variable=ProjCorBo, value="Course").grid(row=5, column=3)
        ProjCorButtonTwo = Radiobutton(
            self.root, text="Project", variable=ProjCorBo, value="Project").grid(row=5, column=4)
        ProjCorButtonTwo = Radiobutton(
            self.root, text="Both", variable=ProjCorBo, value="Both").grid(row=5, column=5)

        def ApplyFilter():
            print("To do")

        def ResetFilter():
            DesVar.set("Please Select")
            MaVar.set("Please Select")
            YearVar.set("Please Select")
            CatVar.set("Please Select")
            ProjCorBo.set("Both")

        ApplyFil = Button(self.root, text="Apply Filter", command=ApplyFilter)
        ApplyFil.grid(row=6, column=5)
        ResetFil = Button(self.root, text="Reset Filter", command=ResetFilter)
        ResetFil.grid(row=6, column=6)

        self.root.mainloop()

    def MePage(self):
        self.cursor.close()
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Me")
        mePage = Button(self.root, text='Edit Profile',
                        command=self.StudEdPro, width=30, height=4)
        mePage.grid(row=1, column=0, sticky=W + E)
        mePage = Button(self.root, text='View Application',
                        command=self.StuViewApp, width=30, height=4)
        mePage.grid(row=2, column=0, sticky=W + E)
        mePage = Button(self.root, text='Back', command=self.BacktoMainPage,
                        padx=5, pady=5, width=30, height=4)
        mePage.grid(row=3, column=0, sticky=W + E)

    def BacktoMainPage(self):
        self.root.destroy()
        self.MainPage()

    def StudEdPro(self):
        print("to do")

    def StuViewApp(self):
        print("to do")

    # AdminMainPage
    def AdminMainPage(self):
        self.root = Tk()
        self.root.wm_title("Admin Main Page")
        Label(self.root, text='Choose Functionality').grid(row=1, column=1, sticky=W)
        viewApps = Button(self.root, text='View Applications', command=self.ViewAppsPage)
        viewApps.grid(row=2, column=1)
        viewProjReport = Button(self.root, text='View Popular Project Reports', command=self.ViewProjReportPage)
        viewProjReport.grid(row=3, column=1)
        viewAppReport = Button(self.root, text='View Application Report', command=self.ViewAppReportPage)
        viewAppReport.grid(row=4, column=1)
        addProj = Button(self.root, text='Add a Project', command=self.AddProjPage)
        addProj.grid(row=5, column=1)
        addCourse = Button(self.root, text='Add a Course', command=self.AddCoursePage)
        addCourse.grid(row=6, column=1)

        logout = Button(self.root, text='Logout', command=self.Logout)
        logout.grid(row=7, column=2)

        self.root.mainloop()

    # Chris Lung
    def ViewAppsPage(self):
        print('TODO')

    # Chris Lung
    def ViewProjReportPage(self):
        print('TODO')

    # Chris Lung
    def ViewAppReportPage(self):
        print('TODO')

    def AddProjPage(self):

        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Add Project Page")

        Label(self.root, text="Add a Project").grid(row=1, column=1, sticky=W + E)
        # row 2
        Label(self.root, text="Project Name:").grid(row=2, column=0)
        self.projName = Entry(self.root)
        self.projName.grid(row=2, column=1)
        # row 3
        Label(self.root, text="Advisor:").grid(row=3, column=0)
        self.advisorName = Entry(self.root)
        self.advisorName.grid(row=3, column=1)
        # row 4
        Label(self.root, text="Advisor Email:").grid(row=4, column=0)
        self.advisorEmail = Entry(self.root)
        self.advisorEmail.grid(row=4, column=1)
        # row 5
        Label(self.root, text="Description").grid(row=5, column=0)
        self.description = Text(self.root, height=10, width=25)
        self.description.grid(row=5, column=1)
        # row 6
        # change 'Designations' to what Dennis has
        rootVar = StringVar(self.root)
        rootVar.set("Please Select")
        Label(self.root, text="Category").grid(row=6, column=0)
        CatDrop = OptionMenu(self.root, rootVar, 'Designations')
        CatDrop.grid(row=6, column=1, padx=1, pady=1)

        def AddCat(self):
            print('TODO')

        addCat = Button(self.root, text='Add a new Category', command=AddCat)
        addCat.grid(row=6, column=2)
        # row 7
        Label(self.root, text="Designation").grid(row=7, column=0)
        DesDrop = OptionMenu(self.root, rootVar, 'Designations')
        DesDrop.grid(row=7, column=1, padx=1, pady=1)
        # row 8
        Label(self.root, text="Estimated # of Students").grid(row=7, column=0)
        self.description = Entry(self.root)
        self.description.grid(row=7, column=1)
        # row 9
        Label(self.root, text="Major Requirement").grid(row=9, column=0)
        MajDrop = OptionMenu(self.root, rootVar, 'Designations')
        MajDrop.grid(row=9, column=1, padx=1, pady=1)
        # row 10
        Label(self.root, text="Year Requirement").grid(row=10, column=0)
        YearDrop = OptionMenu(self.root, rootVar, 'Designations')
        YearDrop.grid(row=10, column=1, padx=1, pady=1)
        # row 11
        Label(self.root, text="Department Requirement").grid(row=11, column=0)
        DepDrop = OptionMenu(self.root, rootVar, 'Designations')
        DepDrop.grid(row=11, column=1, padx=1, pady=1)
        # row 12
        back = Button(self.root, text='Back', command=self.AdminMainPage)
        back.grid(row=12, column=0)
        submit = Button(self.root, text='Submit', command=self.SubmitProj)
        submit.grid(row=12, column=2)

        self.root.mainloop()

    def AddCoursePage(self):
        print('TODO')

    def Logout(self):
        print('TODO')

    def SubmitProj(self):
        print('TODO')

    def Connect(self):
        try:
            self.db = pymysql.connect(
                host='academic-mysql.cc.gatech.edu',
                user='cs4400_Team_38',
                passwd='PTtMisGK',
                db='cs4400_Team_38'
            )
            self.cursor = self.db.cursor()
        except:
            messagebox.showwarning(
                "Whoops!", "Please check your internet connection")
App()
