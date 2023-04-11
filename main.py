import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PyAstronomy.pyTiming import pyPDM



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Multi-band PDM GUI")
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


        self.result_button = tk.Button(self)  #輸出圖形顯示按鈕
        self.result_button["text"] = "result"
        self.result_button["state"] = "disabled"
        self.result_button["command"] = self.show_result
        self.result_button.pack(side="bottom")



    def select_file(self):  #選擇檔案功能函式
        filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filetypes)
        self.flname=filename
        self.result_label["text"] = self.flname
        
    def calculate_start(self): #計算按鈕函式
        self.calculate_statistics(self.flname)
        self.result_button["state"] = "normal"
        #self.show_scatter(self.flname)

    def calculate_statistics(self,filename):  #運算函式
        df = pd.read_csv(filename)
        filename_split_path = filename.split("/")
        self.outputfigname=filename_split_path[-1][:-4]+".png"
        S= pyPDM.Scanner(minVal=float(self.var_min.get()),maxVal=float(self.var_max.get()),dVal=0.1,mode="period")
        col_list = list(set(df['filter'].tolist()))
        col_list.remove['filter']
        sizef=17
        fig,axs=plt.subplots(3,1,figsize=(8,10))
        fig.subplots_adjust(hspace=0.4)
        f_total=1
        t_total=1
        for data_filter in col_list:
            MJD=np.array( df['MJD'][df['filter']==data_filter].tolist())
            mag=np.array( df['mag'][df['filter']==data_filter].tolist())
            P_filter=pyPDM.PyPDM(MJD,mag)
            f,t =  P_filter.pdmEquiBinCover(10,4,S)
            axs[0].plot(f, t)
            f_total=f
            t_total=t_total*t

        axs[1].plot(f_total,t_total)
        best_period=f_total[t_total== np.max(t_total)]
        self.result_label["text"] = "best period ="+str(best_period)
        for data_filter in col_list:
            MJD=np.array( df['MJD'][df['filter']==data_filter].tolist())
            mag=np.array( df['mag'][df['filter']==data_filter].tolist())
            error=np.array( df['error'][df['filter']==data_filter].tolist())
            phase=np.array( df['MJD'][df['filter']==data_filter].tolist())/best_period - np.array( df['MJD'][df['filter']==data_filter].tolist())//best_period
            axs[2].errorbar(phase,mag,error,fmt='.')
        axs[1].set_xlabel("period",fontsize=sizef)
        axs[0].set_ylabel("Theta",fontsize=sizef)
        axs[1].set_ylabel("Theta",fontsize=sizef)
        axs[2].set_xlabel("Phase",fontsize=sizef)
        axs[2].set_ylabel("Mag",fontsize=sizef)
        axs[2].yaxis_inverted()
        axs[0].set_title(self.outputfigname[:-4],fontsize=sizef)
        plt.savefig(self.outputfigname)


    def show_result(self):  # 結果圖展示功能函式
        result_window = tk.Toplevel(self.master)
        result_window.title("result")
        #scatter_window.geometry("1024x1024")
        result_image = tk.PhotoImage(file=self.outputfigname)
        result_label = tk.Label(result_window, image=result_image)
        result_label.image = result_image
        result_label.pack()


root = tk.Tk()
app = Application(master=root)
app.mainloop()