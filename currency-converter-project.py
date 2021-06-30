##Real Time Currency Converter using Python

import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

class Converter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.rates = self.data['rates']

    def convert(self, fcurr, tcurr, amt=1):

        if fcurr == "Select" or tcurr == "Select":
            return

        ##Convert fcurr in USD then to tcurr
        famt = self.rates[fcurr] 
        tamt = self.rates[tcurr]
        amt_usd = amt / famt
        amt_final = round(amt_usd * tamt, 4)
        return amt_final

class GUI():
    def __init__(self, currency_converter):

        self.countries_list = list(currency_converter.rates.keys())
        window = Tk()
        window.title("Currency Converter")

        window.geometry("500x400")
        c = "mistyrose"
        window.config(bg=c)


        ##Heading
        heading = Label(window, text="Real Time Currency Converter", bg=c,
                        font=("Arial italics", 15), anchor=CENTER)
        heading.pack()


        ##From Currency Line
        from_currency_label = Label(window, text="Enter the input currency",
                                     bg=c)
        from_currency_label.place(x=95, y=80)

        self.from_currency = StringVar()
        self.from_currency.set("Select")
        from_currency_dropdown = ttk.Combobox(window, values=self.countries_list,
                                               textvariable=self.from_currency,
                                               state="readonly",
                                               justify=tk.CENTER, width=15)
        from_currency_dropdown.place(x=280, y=80)

        from_currency_dropdown.bind("<<ComboboxSelected>>", self.callback)


        ##Output Currency Line
        to_currency = Label(window, text="Enter the output currency", bg=c)
        to_currency.place(x=89, y=130)

        self.to_currency = StringVar()
        self.to_currency.set("Select")
        to_currency_dropdown = ttk.Combobox(window, values=self.countries_list,
                                               textvariable=self.to_currency,
                                               state="readonly",
                                               justify=tk.CENTER, width=15)
        to_currency_dropdown.place(x=280, y=130)

        to_currency_dropdown.bind("<<ComboboxSelected>>", self.callback)
        

        ##Input Amount Line
        self.input_amount = StringVar()
        reg = window.register(self.valid)
        input_amount_label = Label(window, text="Enter the amount to be converted",
                                   bg=c)
        input_amount_label.place(x=30, y=180)

        input_amount_entry = Entry(window, width=16, textvariable=self.input_amount,
                                   validate="key", validatecommand = (reg, '%P'))
        input_amount_entry.place(x=280, y=180)


        ##Output Amount Line
        self.output_amount = StringVar()
        output_amount_label = Label(window, text="Converted Amount", bg=c)
        output_amount_label.place(x=128, y=230)

        output_amount_entry = Entry(window, textvariable=self.output_amount,
                                    width=16, state='readonly')
        output_amount_entry.place(x=280, y=230)


        ##Conversion Rates
        self.conversion = StringVar()
        label = Label(window, textvariable = self.conversion, justify=tk.CENTER,
                      width=30, bg=c, font=("Times", "24", "bold"))
        label.place(x=0, y=280)


    ##Function is called whenever a currency is changed
    def callback(self, event=None):
        from_currency = self.from_currency.get()
        to_currency = self.to_currency.get()
        
        if from_currency == "Select" or to_currency == "Select":
            return

        ##Generate / Update Label
        self.generate_conversion(from_currency, to_currency)

        ##Generate / Update Final Amount
        self.valid(self.input_amount.get())


    ##Function to generate the Conversion Rates Label
    def generate_conversion(self, from_currency, to_currency):
        converter.convert(from_currency, to_currency)
        conversion = "1  "+from_currency+"  =  "+str(converter.convert(from_currency, to_currency))+"  "+to_currency
        self.conversion.set(conversion)


    ##Function is called when we input something in amount
    def valid(self, number):        
        try:
            number = float(number)
        except:
            if number == "":
                return True
            return False

        
        self.output_amount.set(converter.convert(self.from_currency.get(),
                               self.to_currency.get(), number))
        return True

        

        
link_to_api = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = Converter(link_to_api)
obj = GUI(converter)
