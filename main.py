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

    def create_widgets(self):  #GUI 元件設置
        self.max_label = tk.Label(self,text="Input max value")  #最大值輸入框
        self.max_label.pack()
        self.var_max = tk.StringVar()
        self.input_max = tk.Entry(self,width=15,textvariable=self.var_max)  
        self.input_max.pack()
        
        self.min_label = tk.Label(self,text="Input min value")  #最小值輸入框
        self.min_label.pack()
        self.var_min = tk.StringVar()
        self.input_min = tk.Entry(self,width=15,textvariable=self.var_min) 
        self.input_min.pack()

        self.space = tk.Label(self,text="")  #中間空行
        self.space.pack()

        self.select_button = tk.Button(self)  #選擇檔案按鈕
        self.select_button["text"] = "File"
        self.select_button["command"] = self.select_file
        self.select_button.pack()

        self.result_label = tk.Label(self, text="")  #結果文字輸出
        self.result_label.pack()

        self.calculate_button = tk.Button(self)  #計算按鈕
        self.calculate_button["text"] = "calculate"
        self.calculate_button["state"] = "normal"
        self.calculate_button["command"] = self.calculate_start
        self.calculate_button.pack()


        self.scatter_button = tk.Button(self)  #輸出圖形顯示按鈕
        self.scatter_button["text"] = "scatter"
        self.scatter_button["state"] = "disabled"
        self.scatter_button["command"] = self.show_scatter
        self.scatter_button.pack(side="bottom")



    def select_file(self):  #選擇檔案功能函式
        filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filetypes)
        self.flname=filename
        self.result_label["text"] = self.flname
        
    def calculate_start(self): #計算按鈕函式
        self.calculate_statistics(self.flname)
        self.scatter_button["state"] = "normal"
        self.show_scatter(self.filename)

    # def calculate_statistics(self,filename):
    #     data = pd.read_csv(filename)
    #     mean = data.mean()
    #     std = data.std()
    #     filename_split_path = filename.split("/")
    #     self.result_label["text"] = filename_split_path[-1][:-4]+'\n'+f"平均值：{mean}\n標準差：{std}"+"\n"+str(self.var_max.get())+"\n"+str(self.var_min.get())

    #     outputfigname=filename_split_path[-1][:-4]+".png"
    #     plt.scatter(data["x"], data["y"])
    #     plt.xlabel("x")
    #     plt.ylabel("y")
    #     plt.title("scatter")
    #     plt.savefig(outputfigname)
    #     self.outputfigname = outputfigname

    def calculate_statistics(self,filename):  #運算函式
        data = pd.read_csv(filename)

    def show_scatter(self):  # 結果圖展示功能函式
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