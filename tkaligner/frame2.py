
        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.0, rely=0.333, relheight=0.332, relwidth=1.0)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(width=125)

        self.c10 = ttk.Label(self.Frame2)
        self.c10.place(relx=0.0, rely=0.0,  relheight=1.0, relwidth=0.05)
        # self.c10.configure(background="#d9d9d9")
        # self.c10.configure(background="#1979a9")
        self.c10.configure(background="#0099cc")
        self.c10.configure(foreground="#000000")
        self.c10.configure(font="TkDefaultFont")
        self.c10.configure(relief="flat")
        self.c10.configure(takefocus="0")
        self.c10.configure(text='''01''')

        self.c11 = ScrolledText(self.Frame2)
        self.c11.place(relx=0.05, rely=0., relheight=1, relwidth=0.45)
        self.c11.configure(background="white")
        self.c11.configure(font=font9)
        self.c11.configure(foreground="black")
        self.c11.configure(highlightbackground="#d9d9d9")
        self.c11.configure(highlightcolor="black")
        # self.c11.configure(highlightcolor="blue")
        self.c11.configure(insertbackground="black")
        self.c11.configure(insertborderwidth="3")
        self.c11.configure(selectbackground="#c4c4c4")
        self.c11.configure(selectforeground="black")
        self.c11.configure(takefocus="0")
        self.c11.configure(width=10)
        self.c11.configure(wrap="none")

        self.c12 = ScrolledText(self.Frame2)
        self.c12.place(relx=0.5, rely=0., relheight=1, relwidth=0.45)
        self.c12.configure(background="white")
        self.c12.configure(font=font9)
        self.c12.configure(foreground="black")
        self.c12.configure(highlightbackground="#d9d9d9")
        self.c12.configure(highlightcolor="black")
        self.c12.configure(insertbackground="black")
        self.c12.configure(insertborderwidth="3")
        self.c12.configure(selectbackground="#c4c4c4")
        self.c12.configure(selectforeground="black")
        self.c12.configure(takefocus="0")
        self.c12.configure(width=10)
        self.c12.configure(wrap="none")

        self.c13 = tk.Text(self.Frame2)
        self.c13.place(relx=0.95, rely=0., relheight=1, relwidth=0.05)
        self.c13.configure(background="white")
        self.c13.configure(font=font9)
        self.c13.configure(foreground="black")
        self.c13.configure(highlightbackground="#d9d9d9")
        self.c13.configure(highlightcolor="black")
        self.c13.configure(insertbackground="black")
        self.c13.configure(selectbackground="#c4c4c4")
        self.c13.configure(selectforeground="black")
        self.c13.configure(takefocus="0")
        self.c13.configure(width=10)
        self.c13.configure(wrap="word")