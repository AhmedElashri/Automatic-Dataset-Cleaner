import tkinter as tk
from tkinter.filedialog import *
from tkinter import *
import ttkbootstrap as ttk
import numpy as np
import pandas as pd
from os import path

#The file types that the program can read
file_types = [("Compatible Files", "*.csv *.xlsx *.json *.xml"),
              ("CSV", "*.csv"),
              ("Excel", "*.xlsx"),
              ("JSON", "*.json"),
              ("XML", "*.xml")]

directory = None
df = None
file_type_read = None
num_replacement_type = 3
text_replacement_type = 2

def add_to_textbox(textbox, text):
    textbox.config(state=NORMAL)
    textbox.insert(END, text + '\n')
    textbox.config(state=DISABLED)

def clear_textbox(textbox):
    textbox.config(state=NORMAL)
    textbox.delete('1.0', END)
    textbox.config(state=DISABLED)

def open_file():
    global directory, df, file_type_read
    
    #temp make sure that if you opened the file selector and then closed it, it will use the previously selected directory
    directory = askopenfilename(filetypes=file_types)

    if directory != "":
        file_type_read = directory.split('.')[-1]
        match file_type_read:
            case 'csv':
                df = pd.read_csv(directory)
            case 'xlsx':
                df = pd.read_excel(directory)
            case 'json':
                df = pd.read_json(directory)
            case 'xml':
                df = pd.read_xml(directory)
            case '':
                None
            case _:
                tk.messagebox.showwarning("Error", "This file type is not compatible. Please use a CSV, Excel, JSON, or XML file.")
        
        #if a dataset was successfully read
        if df is not None:
            clean_button.config(state=NORMAL)
            clear_textbox(text_box)
            add_to_textbox(text_box, "- Loaded " + directory.split('/')[-1])
    
def reset_file():
    global directory, df, file_type_read
    
    file_type_read = directory.split('.')[-1]
    match file_type_read:
        case 'csv':
            df = pd.read_csv(directory)
        case 'xlsx':
            df = pd.read_excel(directory)
        case 'json':
            df = pd.read_json(directory)
        case 'xml':
            df = pd.read_xml(directory)
        case '':
            None
        case _:
            tk.messagebox.showwarning("Error", "This file type is not compatible. Please use a CSV, Excel, JSON, or XML file.")
    
    #if a dataset was successfully read
    if df is not None:
        clear_textbox(text_box)
        add_to_textbox(text_box, "- Loaded " + directory.split('/')[-1])

def export_dataset():
    global directory, df, file_type_read
    
    name = directory.split('/')[-1].split('.')[0]
    location = path.dirname(directory) + '/'

    new_name = name + " cleaned"

    match file_type_read:
        case 'csv':
            df.to_csv(location + new_name + '.' + file_type_read, index=False)
        case 'xlsx':
            df.to_excel(location + new_name + '.' + file_type_read, index=False)
        case 'json':
            df.to_json(location + new_name + '.' + file_type_read)
        case 'xml':
            df.to_xml(location + new_name + '.' + file_type_read, index=False)
        case '':
            None
        case _:
            tk.messagebox.showwarning("Error", "File could not be exported.")
        
    add_to_textbox(text_box, "- File exported as " + new_name + '.' + file_type_read +".")

def update_columns(dataframe):
    numbies = []
    texties = []
    for column in dataframe.columns:
        if str(dataframe.dtypes[column]) == 'object':
            texties.append(column)
        else:
            numbies.append(column)

    return numbies, texties

def set_num_rep(num):
    global num_replacement_type
    match num:
        case 0:
            num_replacement_type = 0
            menubutton_num_rep.config(text='Missing Numbers are replaced by: Average')
            entry_num_rep.config(state=DISABLED, bootstyle='default')
        case 1:
            num_replacement_type = 1
            menubutton_num_rep.config(text='Missing Numbers are replaced by: Most Common')
            entry_num_rep.config(state=DISABLED, bootstyle='default')
        case 2:
            num_replacement_type = 2
            menubutton_num_rep.config(text='Missing Numbers are replaced by: Specific Value')
            entry_num_rep.config(state=NORMAL, bootstyle='primary')
        case 3:
            num_replacement_type = 3
            menubutton_num_rep.config(text='Missing Numbers are replaced by: Ask for each')
            entry_num_rep.config(state=DISABLED, bootstyle='default')
        case _:
            None

def set_text_rep(text):
    global text_replacement_type
    match text:
        case 0:
            text_replacement_type = 0
            menubutton_text_rep.config(text='Missing Strings are replaced by: Most Common')
            entry_text_rep.config(state=DISABLED, bootstyle='default')
        case 1:
            text_replacement_type = 1
            menubutton_text_rep.config(text='Missing Strings are replaced by: Specific Value')
            entry_text_rep.config(state=NORMAL, bootstyle='primary')
        case 2:
            text_replacement_type = 2
            menubutton_text_rep.config(text='Missing Strings are replaced by: Ask for each')
            entry_text_rep.config(state=DISABLED, bootstyle='default')
        case _:
            None

def ask_text_window(col):
    ans = None

    ask_each = ttk.Toplevel()
    ask_each.title("Change Request: " + col)
    ask_each.style.theme_use('yeti')
    ask_each.geometry("400x450")
    ask_each.resizable(width=False, height=False)

    values = []
    for i in df[col].unique().tolist():
        if str(i) != 'nan':
            values.append(i)

    text_value = 'The column "' + col + '" has ' + str(df[col].isna().sum()) + ' Missing Values\nSome values Include: '
    for i in range(min(5,len(values))):
        text_value = text_value + str(values[i])
        if i != (min(5,len(values)) - 1):
            text_value = text_value + ", "
    text_value = text_value + "\nThe total number of unique values is " + str(df[col].nunique())

    ask_label = ttk.Label(ask_each,text=text_value)
    ask_label.pack(side=TOP,pady=5)

    ask_button_area = ttk.Frame(ask_each)
    ask_button_area.pack(side=BOTTOM, padx=10, pady=10, fill=X)
    ask_button_area.columnconfigure((0),weight=1, uniform='a')
    ask_button_area.columnconfigure((1),weight=3, uniform='a')
    ask_button_area.rowconfigure((0,2), weight=5, uniform='a')
    ask_button_area.rowconfigure((1), weight=1, uniform='a')

    def op1():
        nonlocal ans
        ans = str(df[col].value_counts().idxmax())
        ask_each.destroy()

    def op2():
        nonlocal ans
        ans = ask_text_rep.get()
        ask_each.destroy()

    ask_common = ttk.Button(ask_button_area, bootstyle='primary',text='Most Common Value: ' + str(df[col].value_counts().idxmax()), command= op1)
    ask_common.grid(column=0,row=0,columnspan=2, sticky='ew')

    ask_value = ttk.Button(ask_button_area, bootstyle='primary',text='Specific Value',command=op2)
    ask_value.grid(column=0,row=2,columnspan=1, sticky='ew')
    
    ask_text_rep = ttk.Entry(ask_button_area)

    ask_text_rep.grid(row=2,column=1,sticky='ew')

    ask_each.wait_window()
    return ans

def ask_num_window(col):
    ans = None

    ask_each = ttk.Toplevel()
    ask_each.title("Change Request: " + col)
    ask_each.style.theme_use('yeti')
    ask_each.geometry("400x450")
    ask_each.resizable(width=False, height=False)

    values = []
    for i in df[col].unique().tolist():
        if str(i) != 'nan':
            values.append(i)

    text_value = 'The column "' + col + '" has ' + str(df[col].isna().sum()) + ' Missing Values\nSome values Include: '
    for i in range(min(5,len(values))):
        text_value = text_value + str(values[i])
        if i != (min(5,len(values)) - 1):
            text_value = text_value + ", "
    text_value = text_value + "\nThe total number of unique values is " + str(df[col].nunique())

    ask_label = ttk.Label(ask_each,text=text_value)
    ask_label.pack(side=TOP,pady=5)

    ask_button_area = ttk.Frame(ask_each)
    ask_button_area.pack(side=BOTTOM, padx=10, pady=10, fill=X)
    ask_button_area.columnconfigure((0),weight=1, uniform='a')
    ask_button_area.columnconfigure((1),weight=3, uniform='a')
    ask_button_area.rowconfigure((0,2,4), weight=5, uniform='a')
    ask_button_area.rowconfigure((1,3), weight=1, uniform='a')

    def op1():
        nonlocal ans
        ans = str(round(df[col].mean(),2))
        ask_each.destroy()

    def op2():
        nonlocal ans
        ans = str(df[col].value_counts().idxmax())
        ask_each.destroy()

    def op3():
        nonlocal ans
        ans = ask_text_rep.get()
        ask_each.destroy()

    ask_common = ttk.Button(ask_button_area, bootstyle='primary',text='Average: ' + str(round(df[col].mean(), 2)), command= op1)
    ask_common.grid(column=0,row=0,columnspan=2, sticky='ew')

    ask_value = ttk.Button(ask_button_area, bootstyle='primary',text='Most Common: ' + str(df[col].value_counts().idxmax()),command=op2)
    ask_value.grid(column=0,row=2,columnspan=2, sticky='ew')

    ask_value = ttk.Button(ask_button_area, bootstyle='primary',text='Specific Value',command=op3)
    ask_value.grid(column=0,row=4,columnspan=1, sticky='ew')
    
    ask_text_rep = ttk.Entry(ask_button_area)

    ask_text_rep.grid(row=4,column=1,sticky='ew')

    ask_each.wait_window()
    return ans

def dataset_cleaning():
    global df
    df_size = len(df.index)

    # - Num/Text Split 
    add_to_textbox(text_box, "- Identifying columns with text and numbers.")
    numbies, texties= update_columns(df)

    # - Duped Data 
    add_to_textbox(text_box, "- Removing duplicate data.")
    df.drop_duplicates(inplace=True)

    # - Missing Value 
    add_to_textbox(text_box, "- Working on missing values.")

    for column in df.columns:
        #if the missing columns are greater than 20% and user picked delete option, delete the column
        if (df[column].isna().sum() > 0.2*df_size) & (var_drop_at_20.get()):
            df.drop(columns=column, inplace=True)
            add_to_textbox(text_box, "Dropping " + column + " as it is missing many too many values.")
        elif df[column].isna().sum() > 0:
            if set([column]).intersection(numbies):
                if num_replacement_type == 0:
                    df.fillna(value = {column:df[column].mean()}, inplace= True)
                elif num_replacement_type == 1:
                    df.fillna(value = {column:int(df[column].value_counts().idxmax())}, inplace= True)
                elif num_replacement_type == 2:
                    df.fillna(value = {column:int(entry_num_rep.get())}, inplace= True)
                else: 
                    new_num = float(ask_num_window(column))
                    df.fillna(value = {column:new_num}, inplace= True)
            else:
                if text_replacement_type == 0:
                    df.fillna(value = {column:str(df[column].value_counts().idxmax())}, inplace= True)
                elif text_replacement_type == 1:
                    df.fillna(value = {column:str(entry_text_rep.get())}, inplace= True)
                else:
                    new_value = ask_text_window(column)
                    df.fillna(value = {column:new_value}, inplace= True)
  
    df.dropna(inplace=True)
    
    numbies, texties= update_columns(df)    

    # - Lowercase Columns
    add_to_textbox(text_box,"- Lowercasing all columns")
    df.columns = list(map(str.lower,df.columns))   

    numbies, texties= update_columns(df)

    # - Lowercase Column Contents
    if (var_lower_contents.get()):
        add_to_textbox(text_box,"   Lowercasing contents")
        for column in texties:
            df[column] = df[column].str.lower()

    # - Possible gender column
    add_to_textbox(text_box, "- Finding common catagorical columns to convert to numbers")
    gendies = list(set(df.columns).intersection(['sex','gender']))
    if gendies != []:
        df[gendies[0]] = list(map(str.lower,df[gendies[0]]))
        add_to_textbox(text_box, "Found \"Gender\" column, converting male and female to 0, and 1 respectively")
        df[gendies[0]].replace(['male', 'man', 'm', 'woman', 'female','f','w'],[0,0,0,1,1,1,1], inplace=True)
    export_button.config(state=NORMAL)

    add_to_textbox(text_box, "====================================")
    add_to_textbox(text_box, "-------------------- Dataset Cleaned -------------------")
    add_to_textbox(text_box, "====================================")


#Creating the tkinter window
window = ttk.Window()
window.title("AuDaC")
window.style.theme_use('yeti')
window.geometry("500x400")
window.resizable(width=False, height=False)

# - Menu Bar
menubar = ttk.Menu(window)
file = ttk.Menu(menubar, tearoff=0)
file.add_command(label="Open File", command=open_file)
file.add_separator()
file.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=file)

#debug = ttk.Menu(menubar, tearoff=0)
#debug.add_command(label="Print Dataframe", command= lambda: print(df))
#debug.add_command(label="Print File Type Read", command= lambda: print(file_type_read))
#menubar.add_cascade(label="Debug", menu=debug)

# - Settings
settings_area = ttk.Frame(window)
settings_area.pack(side=TOP, fill=BOTH,expand=True, padx=10, pady=10)
settings_area.columnconfigure((0,1),weight=1)
settings_area.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

var_lower_contents = ttk.BooleanVar()
check_lower_contents = ttk.Checkbutton(settings_area,bootstyle='round-toggle', text='Lowercase all values', variable=var_lower_contents)
check_lower_contents.grid(row=0,column=0,sticky='w')

var_drop_at_20 = ttk.BooleanVar()
check_drop_at_20 = ttk.Checkbutton(settings_area,bootstyle='round-toggle', text='Drop columns with more than 20% missing values', variable=var_drop_at_20)
check_drop_at_20.grid(row=1,column=0,sticky='w')

menubutton_num_rep = ttk.Menubutton(settings_area, text="Missing Numbers are replaced by: Ask for each")
submenu_num_rep = ttk.Menu(menubutton_num_rep,tearoff=False)
submenu_num_rep.add_command(label='Average', command=lambda: set_num_rep(0))
submenu_num_rep.add_command(label='Most Common', command=lambda: set_num_rep(1))
submenu_num_rep.add_command(label='Specific Value', command=lambda: set_num_rep(2))
submenu_num_rep.add_command(label='Ask for each', command=lambda: set_num_rep(3))
menubutton_num_rep.config(menu=submenu_num_rep)

entry_num_rep = ttk.Entry(settings_area, state=DISABLED )

menubutton_num_rep.grid(row=2,column=0,sticky='ew')
entry_num_rep.grid(row=2,column=1,sticky='e')

menubutton_text_rep = ttk.Menubutton(settings_area, text="Missing Strings are replaced by: Ask for each")
submenu_text_rep = ttk.Menu(menubutton_text_rep,tearoff=False)
submenu_text_rep.add_command(label='Most Common', command=lambda: set_text_rep(0))
submenu_text_rep.add_command(label='Specific Value', command=lambda: set_text_rep(1))
submenu_text_rep.add_command(label='Ask for each', command=lambda: set_text_rep(2))
menubutton_text_rep.config(menu=submenu_text_rep)

entry_text_rep = ttk.Entry(settings_area, state=DISABLED )

menubutton_text_rep.grid(row=3,column=0,sticky='ew')
entry_text_rep.grid(row=3,column=1,sticky='e')

# - Button Area
button_area = ttk.Frame(window,height=20)
button_area.pack(side=BOTTOM, fill=X, padx=10, pady=10)

export_button = ttk.Button(button_area, bootstyle='primary',text='Export Dataset', command=export_dataset, state=DISABLED)
export_button.pack(side=RIGHT, padx=5)

clean_button = ttk.Button(button_area, bootstyle='primary',text='Clean Dataset', command=dataset_cleaning, state=DISABLED)
clean_button.pack(side=RIGHT, padx=5)

load_button = ttk.Button(button_area, bootstyle='primary',text='Load Dataset',command=open_file)
load_button.pack(side=LEFT, padx=5)

reset_button = ttk.Button(button_area, bootstyle='primary',text='Reset Dataset',command=reset_file)
reset_button.pack(side=LEFT, padx=5)


# - Create a Text Area
text_area = ttk.Frame(window,height=220)
text_area.pack(side=BOTTOM, fill=X, padx=10, pady=10)

text_scrollbar = ttk.Scrollbar(text_area, orient=VERTICAL, bootstyle='default')
text_scrollbar.pack(side=RIGHT, fill='y')

text_box= ttk.Text(text_area, state=DISABLED, height= 10, width= 400, yscrollcommand=text_scrollbar.set)
text_box.pack(side=BOTTOM)
text_scrollbar.config(command=text_box.yview)


window.config(menu=menubar)
window.mainloop()