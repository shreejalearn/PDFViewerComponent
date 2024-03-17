from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os
from miner import PDFMiner

class PDFViewer:
    def __init__(self, master):
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None    
        
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=0, height=0)
        self.master.iconbitmap(self.master, 'pdf_file_icon.ico')
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)
        
        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)
        
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)
        
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky=(N,S))
        
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky=(W, E))
        
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)

        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)
        
        self.uparrow_icon = PhotoImage(file='uparrow.png')
        self.downarrow_icon = PhotoImage(file='downarrow.png')
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        self.downbutton.grid(row=0, column=3, pady=8)
        
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        self.page_label.grid(row=0, column=4, padx=5)
        
        self.output.bind("<MouseWheel>", self.on_mousewheel)
        self.output.bind("<Button-4>", self.on_mousewheel)
        self.output.bind("<Button-5>", self.on_mousewheel)
        
    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.miner = PDFMiner(self.path)
            data, numPages = self.miner.get_metadata()
            self.current_page = 0
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
                self.master.title(self.name)
    
    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.numPages)
            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)         

    def next_page(self):
        if self.fileisopen:
            if self.current_page < self.numPages - 1:
                self.current_page += 1
                self.display_page()
                            
    def previous_page(self):
        if self.fileisopen:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page()
    
    def on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.output.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            self.output.yview_scroll(-1, "units")

root = Tk()
app = PDFViewer(root)
root.mainloop()
