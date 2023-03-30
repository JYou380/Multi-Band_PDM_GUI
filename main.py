import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1024x1024") # 設定UI介面大小為512x512像素
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.max_label = tk.Label(self,text="Input max value")
        self.max_label.pack()
        self.var_max = tk.StringVar()
        self.input_max = tk.Entry(self,width=15,textvariable=self.var_max)  
        self.input_max.pack()
        
        self.min_label = tk.Label(self,text="Input min value")
        self.min_label.pack()
        self.var_min = tk.StringVar()
        self.input_min = tk.Entry(self,width=15,textvariable=self.var_min) 
        self.input_min.pack()

        self.space = tk.Label(self,text="")
        self.space.pack()

        self.select_button = tk.Button(self)
        self.select_button["text"] = "File"
        self.select_button["command"] = self.select_file
        self.select_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()




        self.scatter_button = tk.Button(self)
        self.scatter_button["text"] = "scatter"
        self.scatter_button["state"] = "disabled"
        self.scatter_button["command"] = self.show_scatter
        self.scatter_button.pack(side="bottom")



    def select_file(self):
        filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.calculate_statistics(filename)
            self.scatter_button["state"] = "normal"
            self.show_scatter(filename)
    
    # def max_value_input(self):
    #     max_value = self.var_max.get()
    
    # def min_value_input(self):
    #     min_value = self.var_max.get()

    def calculate_statistics(self, filename):
        data = pd.read_csv(filename)
        mean = data.mean()
        std = data.std()
        filename_split_path = filename.split("/")
        self.result_label["text"] = filename_split_path[-1][:-4]+'\n'+f"平均值：{mean}\n標準差：{std}"+"\n"+str(self.var_max.get())+"\n"+str(self.var_min.get())

        outputfigname=filename_split_path[-1][:-4]+".png"
        plt.scatter(data["x"], data["y"])
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("scatter")
        plt.savefig(outputfigname)
        self.outputfigname = outputfigname

    def show_scatter(self):
        scatter_window = tk.Toplevel(self.master)
        scatter_window.title("scatter")
        #scatter_window.geometry("1024x1024")
        scatter_image = tk.PhotoImage(file=self.outputfigname)
        scatter_label = tk.Label(scatter_window, image=scatter_image)
        scatter_label.image = scatter_image
        scatter_label.pack()


root = tk.Tk()
app = Application(master=root)
app.mainloop()