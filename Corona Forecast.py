import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from tkinter import Tk, Label, Entry, Button, StringVar, RIDGE, messagebox, filedialog

def data_collected():
    url = "https://www.worldometers.info/coronavirus/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    tbody = soup.find('tbody')
    abc = tbody.find_all('tr')
    country_notification = cntdata.get().lower()

    if country_notification == "":
        country_notification = "world"

    serial_number, countries, total_cases = [], [], []
    country_cases = None
    for i in abc:
        id = i.find_all('td')
        country = id[1].text.strip().lower()
        total_cases_value = int(id[2].text.strip().replace(',', ""))
        if country == country_notification:
            total_cases1 = total_cases_value
            total_death = id[4].text.strip()
            new_cases = id[3].text.strip()
            new_deaths = id[5].text.strip()
            messagebox.showinfo("Corona Virus Update", f"Total Cases: {total_cases1}\nTotal Deaths: {total_death}\nNew Cases: {new_cases}\nNew Deaths: {new_deaths}")
            country_cases = total_cases_value

        serial_number.append(id[0].text.strip())
        countries.append(id[1].text.strip())
        total_cases.append(total_cases_value)

    df = pd.DataFrame({'Total Cases': total_cases}, index=countries)

    if country_cases is not None:
        forecast_ARIMA(total_cases)

    return df

def forecast_ARIMA(total_cases):
    model = ARIMA(total_cases, order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)

    plt.plot(total_cases)
    plt.plot(np.arange(len(total_cases), len(total_cases)+5), forecast, color='red')
    plt.title('COVID-19 Cases Forecast')
    plt.xlabel('Days')
    plt.ylabel('Total Cases')
    plt.legend(['Actual Cases', 'Forecasted Cases'])
    plt.show()

def downloaddata():
    global path
    df = data_collected()
    if len(flist) != 0:
        path = filedialog.askdirectory()
        for filetype in flist:
            filepath = f"{path}/covid_data.{filetype}"
            if filetype == 'html':
                df.to_html(filepath)
            elif filetype == 'json':
                df.to_json(filepath)
            elif filetype == 'csv':
                df.to_csv(filepath)
        messagebox.showinfo("Download", f"Data downloaded successfully to {path}")
    else:
        messagebox.showwarning("Download", "Please select at least one file format to download.")
    flist.clear()
    Inhtml.configure(state='normal')
    Injson.configure(state='normal')
    Inexcel.configure(state='normal')

def inhtmldownload():
    flist.append('html')
    Inhtml.configure(state='disabled')

def injsondownload():
    flist.append('json')
    Injson.configure(state='disabled')

def inexceldownload():
    flist.append('csv')
    Inexcel.configure(state='disabled')

coro = Tk()
coro.title("Corona Virus Information")
coro.geometry('800x500+200+80')
coro.configure(bg='#046173')
flist = []
path = ''

mainlabel = Label(coro, text="Corona Virus Live Tracker", font=("new roman", 30, "bold"), bg="#05897A", width=33, fg="black", bd=5)
mainlabel.place(x=0, y=0)

label1 = Label(coro, text="Country Name", font=("arial", 20, "bold"), bg="#046173")
label1.place(x=15, y=100)

label2 = Label(coro, text="Download File in ", font=("arial", 20, "bold"), bg="#046173")
label2.place(x=15, y=200)

cntdata = StringVar()
entry1 = Entry(coro, textvariable=cntdata, font=("arial", 20, "bold"), relief=RIDGE, bd=2, width=32)
entry1.place(x=280, y=100)

Inhtml = Button(coro, text="HTML", bg="#2DAE9A", font=("arial", 15, "bold"), relief=RIDGE, activebackground="#05945B", activeforeground="white", bd=5, width=5, command=inhtmldownload)
Inhtml.place(x=300, y=200)

Injson = Button(coro, text="JSON", bg="#2DAE9A", font=("arial", 15, "bold"), relief=RIDGE, activebackground="#05945B", activeforeground="white", bd=5, width=5, command=injsondownload)
Injson.place(x=400, y=200)

Inexcel = Button(coro, text="EXCEL", bg="#2DAE9A", font=("arial", 15, "bold"), relief=RIDGE, activebackground="#05945B", activeforeground="white", bd=5, width=5, command=inexceldownload)
Inexcel.place(x=500, y=200)

Submit = Button(coro, text="Submit", bg="#CB054A", font=("arial", 15, "bold"), relief=RIDGE, activebackground="#7B0519", activeforeground="white", bd=5, width=25, command=downloaddata)
Submit.place(x=250, y=260)

coro.mainloop()
