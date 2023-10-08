import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class MainWindow:
    def __init__(self, window_width = 800, window_height = 400):
        #TODO Abhängig von matplot das seitenverhältnis bestimmne (ich selber, was halt gut
            # aussieht) -> DANACH: resizable machen oder nicht? 
            # -> DANACH: hardcoded width&height ODER screenX/z, screenY/z ??ß
        self.is_unsaved_changes = False #TODO das muss in der io file in save, load geändert werden. So machen, dass ich nicht dieses object als param reinziehen muss! hier wrapper fcts?
        self.__window_width = window_width
        self.__window_height = window_height
    #init main window
        self.__root = tk.Tk()
        self.__root.title("sHealth Heart Rate Plotter")
        #excecute on_close method before closing programm 
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_close)
        #get display size
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        #get center point
        self.center_x = int(screen_width/2 - self.__window_width)
        self.center_y = int(screen_height/2 - self.__window_height)
        #set main window size and position
        self.__root.geometry(f'{self.__window_width}x{self.__window_height}+{self.center_x}+{self.center_y}')
        #make non resizable #TODO check whether I should make it resizable or not!
        self.__root.resizable(False, False)
        #load app icon
        self.__root.iconbitmap('./resources/logo.ico')
    #add top bar
        self.__make_topbar()
    #TODO checkPrevious() 
        #entweder if isPrevious(): autoload() else: make_empty_message()
        #oder die if abfrage in make_autoload, je nachdem wie das funktioniert
            #ttk.Label(root, text='Load a file or import Samsung Health heart ate data to start a new File').pack()#TODO make this text italic #TODO center text & display only if empty File -> #TODO autoload last opened File 
        self.__make_main_area()
        self.__make_side_area()
    '''Idee: Programm erstellt onClose eine (unsichtbare?) Datei in appdata oder so, wo der pfad der zuletzt geöffneten Datei steht 
        und falls möglich nen EXCEPTION flag, wenn das programm alt+f4 'ed wurde.
        Beim start, also hier, wird diese Datei gelesen, und mit dem Pfad das zuletzt geöffnete dokument geladen.
            -> damit könnte man auch im File-Reiter ein "Zuletzt geöffnet->" einbauen, wo dann die letzten 5 dateien stehen (is glaub eher unnötig,
              ausser ich mach beim import die option "Limit timeranges", dass User dann z.b. für jeden Monat ne eigene Datei erstellen kann. KP ob man das brauch,
              aber wäre ne option, wenn das Fileloading ab ner bestimmten Filegröße z.b. 3 Jahre ewig lang daurert... vlt einfach als TODO aufschreiben.)'''

    def __make_topbar(self):#TODO make self. für sachen, die von anderen fcts gecallt werden müssen
        #add menu top bar
        menubar = tk.Menu(master=self.__root)
        self.__root.config(menu=menubar)
        #init submenus
        file_menu = tk.Menu(master=menubar, tearoff=False)
        settings_menu = tk.Menu(master=menubar, tearoff=False)
        help_menu = tk.Menu(master=menubar, tearoff=False)
        #add file_menu entries
        file_menu.add_command(label='New File From Raw Data')
        file_menu.add_command(label='Save File')#TODO save - load df.to_pickle df.read_pickle !? Oder Sqlite?? ->mit extra infos, wie default display, etc. settings. matplot chart realtime generation (solangs nicht 10jahre dauert, da entweder ändern oder während des ladens nen Fenster ...loading...)
            #save file fct beim ersten save einer datei callt save as, sonst save über geg pfad. Über autoload? <-Aufpassen!
        file_menu.add_command(label='Save As')
        file_menu.add_command(label='Load File')
        file_menu.add_command(label='Add Raw Data To This File')
        file_menu.add_command(label='Exit', command=self.__on_close)
        #add settings_menu entries
        settings_menu.add_command(label='...', state='disabled') # TODO
        #add help_menu entries
        help_menu.add_command(label='How to get raw data')
        help_menu.add_command(label='About')
        #add submenus to menubar
        menubar.add_cascade(menu=file_menu, label='File')
        menubar.add_cascade(menu=settings_menu, label='Settings')
        menubar.add_cascade(menu=help_menu, label='Help')

    def __make_main_area(self):#TODO comment every fucking line
        """Init area, where the Graph is based.
        """        
        #TODO remove hardcoded size
        main_area = tk.Frame(master=self.__root, width=600, height=400, bg='white', borderwidth=1, relief=tk.RIDGE) #TODO passt das mit der border?
        main_area.pack(expand=True, fill='both', side='right', anchor='ne')

        #TODO make this into matplot window
        #TODO remove Hardcoded
        #canvas = tk.Canvas(master=main_area, width=500, height=300, bg='blue', borderwidth=1) #TODO passt das mit der border?
        #canvas.pack(anchor=tk.E, padx=20, pady=20)
        self.__init_canvas(master=main_area)

    def __make_side_area(self):#TODO comment every fucking line
        """Init area, where some user input control is located.
        """        
        side_area = tk.Frame(master=self.__root, width=200, height=400, bg='white', borderwidth=1, relief=tk.RIDGE) #TODO passt das mit der border?
        side_area.pack(expand=False, fill='both', side='left', anchor='nw')

    #Create user contol inputs
        #Make combobox for ... TODO comments & ranges!!!
        #TODO rename boxxes and everything!!!
        #TODO add comments manually to points and ranges
        tk.Label(master=side_area, text="Range").pack(anchor='n')
        range_box = ttk.Combobox(master=side_area)
        range_box['state'] = 'readonly'
        range_box['values'] = ('Hour', 'Day (default)', 'Week', 'Month')
        range_box.set('Day (default)')
        range_box.pack(anchor='n')

        tk.Label(master=side_area, text="Timedate").pack(anchor='n')
        timedate_box = ttk.Combobox(master=side_area)
        timedate_box['state'] = 'readonly'
        timedate_box['values'] = ('1.1.23', '1.2.23', '2.2.23')#TODO machs gescheid, dass die werte anhand existierender daten zu laufzeit geladen werden
        timedate_box.set('1.1.23')
        timedate_box.pack(anchor='n')

    def __init_canvas(self, master):
        from data_import import import_data
        import pandas as pd
        #TODO daten als param?
        csv_path = "C:\\Users\\andre\\Documents\\sHealthHrTest\\samsunghealth_99as_20231008153991\\samsunghealth_99as_20231008153991\\"
        csv_filename = "com.samsung.shealth.tracker.heart_rate.20231008153991.csv"
        df = import_data(csv_path, csv_filename)

        # create a figure
        #TODO fix hardcoded 
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(master=master, figure=figure)

        # create the toolbar
        #NavigationToolbar2Tk(figure_canvas, master)
        #TODO is ganz nice, v.a. der zoom, aber kp ob sich das dann mit den smoothed lines, etc. verträgt.

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.plot(df['date_time'], df['heart_rate'])
        
        axes.set_title('Top 5 Programming Languages')
        axes.set_ylabel('HR')
        axes.set_xlabel('time')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def __update_canvas(self): #TODO, wenn überhaupt nötig
        pass

    def __on_close(self):
        result = messagebox.askyesnocancel("Unsaved Changes", "There are unsaved changes. Do you want to save them now?")
        if result is True:
            #save changes
            self.__root.destroy()
        elif result is False:
            #don't save
            self.__root.destroy()
        elif result is None:
            #User clicked Cancel
            pass

    def run(self):
        self.__root.mainloop()

mw = MainWindow()
mw.run()

        
