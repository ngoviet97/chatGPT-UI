from tkinter import *
from tkinter import ttk
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
from tkinter import messagebox
import requests
import openai
import re
import random

root = Tk()
root.geometry("1000x700")
import time

def redoFuzz(a,b):
    if len(a)//2 < len(b):
        return fuzz.partial_ratio(a, b)
    elif len(a)//2 > len(b):
        return 0
def gptExecution(prompt, command):
    URL = "https://api.openai.com/v1/chat/completions"

    api_key = ["Your API LIST"]

    execution_text = "Once you have obtained the APK files of your desired application, you can use the ARC Welder tool to run it on Google Chrome, both for Windows and OS X, as well as Linux."

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt + " " + command}],
        "temperature": 0.7,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "max_tokens": 256
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key[random.randint(0,len(api_key)-1)]}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    regex = r"(?<=\"content\":\")(.*?)(?=\"})"
    matches = re.finditer(regex, response.text, re.MULTILINE)
    for text in matches:
        return text.group().strip("\n\n")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def splitString(string):
    splitList = []
    for value in [sent for sent in string.split("\n") if sent.isspace() == False]:
        for val in value.split(". "):
            if val != '' and val.isspace() == False and val.strip().isnumeric() == False:
                splitList.append(val)
    return splitList

def checkDup(string1,string2):
    sen1 = splitString(string1)
    sen2 = [value for value in string2.split("\n") if value != '']
    finalValue = []
    for se1 in sen1:
        for se2 in sen2:
            score = redoFuzz(se1,se2)
            try:
                if score >= 30:
                    for sentence in [value for value in splitString(se2) if value.isspace() != True]:
                        score = redoFuzz(se1, sentence)
                        if score >= 70:
                            finalValue.append([se1, sentence, score])
            except:
                pass
    return finalValue
class GUI():
    def __init__(self):
        root.title("GPT3.5 TURBO - WEBIFY APIs")
    def mainRun(self):
        def analyseValue(mode=None):
            valueInput1 = input1.get("1.0", "end-1c")
            valueInput2 = input2.get("1.0", "end-1c")
            valueInput3 = return1.get("1.0", "end-1c")
            if len(valueInput2) == 0:
                check = checkDup(valueInput1, valueInput3)
                input2.delete("1.0", END)
                input2.insert(INSERT, valueInput3)
            else:
                check = checkDup(valueInput1, valueInput2)

            if mode == "inf":
                response = messagebox.showinfo("ÉT O ÉT", "️🎉Có tổng cộng {} lỗi trong bài!!️🎉".format(len(check)))
            ###DELETE VALUES
            return check

        def sendText():
            input1.insert(INSERT,content1)
            input2.insert(INSERT,content1)

        def deleteLabel():
            input1.delete("1.0", END)
            input2.delete("1.0", END)
            return1.delete("1.0", END)
            return2.delete("1.0", END)
            output1.delete("1.0", END)
            promptValue.delete("1.0", END)
        def copy():
            """Copy current contents of text_entry to clipboard."""
            current = output1.get("1.0", "end-1c")
            root.clipboard_clear()  # Optional.
            root.clipboard_append(str(current))
        def replaceValue():
            valueInput1 = input1.get("1.0", "end-1c")
            valueInput2 = return1.get("1.0", "end-1c")
            valueInput3 = output1.get("1.0", "end-1c")
            input1.delete("1.0", END)
            valueInput1 = valueInput1.replace(valueInput2,valueInput3[0:-1])
            input1.insert(INSERT,valueInput1)
        def applyAll():
            start_time = time.time()

            valueInput1 = input1.get("1.0", "end-1c")
            contentReturn = analyseValue()
            waitList = [value[0] for value in contentReturn]
            for value in waitList:
                returnGPT = gptExecution("rewrite in a different and understandable way:", value)
                valueInput1 = valueInput1.replace(value, returnGPT[0:])
            valueInput1 = valueInput1.replace('\\n', '').replace('\\"', '\"').replace('\."', '').replace('..', '.')

            input1.delete("1.0", END)
            input1.insert(INSERT,valueInput1)

            response = messagebox.showinfo("ÉT O ÉT", "️🎉LỆNH THỰC THI THÀNH CÔNG TRONG {}s🎉".format(round(time.time() - start_time), 0))
        def check_input(e):
            contentReturn = analyseValue()
            return1.delete("1.0", END)
            return2.delete("1.0", END)
            percent.delete("1.0", END)

            return1.insert(INSERT, contentReturn[int(combo_box.get())-1][0])
            return2.insert(INSERT, contentReturn[int(combo_box.get())-1][1])
            percent.insert(INSERT,str(contentReturn[int(combo_box.get())-1][2]) + "%")
        def run_bylanguage():
            start_time = time.time()

            prompt = """give me some ideas to optimize this content for {} and rewrite it to {} people::""".format(languages.get(),languages.get())
            print(prompt)
            if len(languages.get()) == 0:
                response = messagebox.showinfo("ÉT O ÉT", "️🎉VUI LÒNG CHỌN NGÔN NGỮ TRƯỚC KHI DỊCH🎉")
                return response
            else:
                returnGPT = gptExecution(prompt,input1.get("1.0", "end-1c"))
                output1.delete("1.0",END)
                returnGPT = returnGPT.replace('\\n', '\n').replace('\\"','\"')

                output1.insert(INSERT, returnGPT)
                response = messagebox.showinfo("ÉT O ÉT", "️🎉DỊCH SANG NGÔN NGỮ {} TRONG {}s🎉".format(languages.get(),round(time.time() - start_time), 0))

            pass
        def runGPT():
            start_time = time.time()
            output1.delete("1.0", END)
            contentReturn = analyseValue()
            if len(promptValue.get("1.0", "end-1c")) == 0:
                response = messagebox.showinfo("ÉT O ÉT", "️🎉VUI LÒNG NHẬP LỆNH TRƯỚC KHI CHẠY GPT️🎉")
                return response
            else:
                try:
                    returnGPT = gptExecution(str(promptValue.get("1.0", "end-1c")),str(contentReturn[int(combo_box.get())-1][0]))
                except:
                    returnGPT = gptExecution(str(promptValue.get("1.0", "end-1c")),return1.get("1.0", "end-1c"))
                returnGPT = returnGPT.replace('\\n', '\n').replace('\\"','\"')
                output1.insert(INSERT,f'{str(returnGPT)}')

                response = messagebox.showinfo("ÉT O ÉT", "️🎉LỆNH THỰC THI THÀNH CÔNG TRONG {}s🎉".format(round(time.time() -  start_time),0))

                return returnGPT
        clicked = StringVar()
        clicked.set("Select website")
        ##drop = OptionMenu(root,clicked,*option_website(),command=display_selected)
        # drop.place(x=450,y=15)

        #### SCROLL VALUE
        textscroll = Scrollbar(root)
        textscroll.pack(side=RIGHT, fill=Y)

        ######INPUT VALUES
        #welcome = Label(root, text="Welcome To The Guessing Game!", background="black", foreground="white",width=18,height=2)
        #welcome.place(x=50, y=10)
        languages = ttk.Combobox(root, width=15)
        languages.bind('<<ComboboxSelected>>', check_input)
        languages.place(x=50, y=20)
        languages['values'] = ["Vietnam","Japan","Germany","English"]

        input1 = Text(root, width=50, borderwidth=20, height=18, bg="light yellow", yscrollcommand=textscroll.set, undo=True)
        input1.place(x=50, y=90)
        input2 = Text(root, width=50, borderwidth=20, height=18, bg="light yellow", yscrollcommand=textscroll.set, undo=True)
        input2.place(x=50, y=385)
        output1 = Text(root, width=60, borderwidth=20, height=23, bg="light blue", yscrollcommand=textscroll.set, undo=True)
        output1.place(x=480, y=320)

        return1 = Text(root, width=60, borderwidth=20, height=3, bg="light blue", yscrollcommand=textscroll.set, undo=True)
        return1.place(x=480, y=90)

        return2 = Text(root, width=60, borderwidth=20, height=3, bg="light blue", yscrollcommand=textscroll.set, undo=True)
        return2.place(x=480, y=180)

        promptValue = Text(root, width=60, borderwidth=8, height=3, bg="light gray")
        promptValue.place(x=492, y=270)

        percent = Text(root, width=5, borderwidth=8, height=1, bg="light gray")
        percent.place(x=650, y=20)

        ######BUTTONS VALUE
        #button1 = Button(root, text="Copy", padx=15, pady=7, highlightbackground='red', command=lambda: copy(input1))
        #button2 = Button(root, text="Copy", padx=15, pady=7, highlightbackground='red', command=lambda: copy(input2))
        button3 = Button(root, text="Copy", padx=15, pady=7, highlightbackground='red', command=lambda: copy())
        replace = Button(root, text="Replace", padx=15, pady=7, highlightbackground='red', command=lambda: replaceValue())
        applyvalue = Button(root, text="Apply All", padx=15, pady=7, highlightbackground='Blue', command=lambda: applyAll())

        GPTButton = Button(root, text="Run", padx=15, pady=14, highlightbackground='blue', command=lambda: runGPT())
        errorAnalyse = Button(root, text="Analyse", padx=15, pady=14, highlightbackground='yellow', command=lambda: returnBox())
        restartBut = Button(root, text="Restart", padx=15, pady=14, highlightbackground='blue', command=lambda: deleteLabel())
        run_LanguageBut = Button(root, text="Translate", padx=15, pady=14, highlightbackground='blue', command=lambda: run_bylanguage())
        ##delBut1 = Button(root, text="Del", padx=15, pady=7, highlightbackground='red', command=lambda: input1.delete("1.0", END))
        #delBut2 = Button(root, text="Del", padx=15, pady=7, highlightbackground='red', command=lambda: input2.delete("1.0", END))
        delBut3 = Button(root, text="Del", padx=15, pady=7, highlightbackground='red', command=lambda: output1.delete("1.0", END))

        ##delBut1.place(x=140, y=325)
        #delBut2.place(x=140, y=620)
        delBut3.place(x=570, y=620)

        #button1.place(x=60, y=325)
        #button2.place(x=60, y=620)
        button3.place(x=490, y=620)
        replace.place(x=640, y=620)
        applyvalue.place(x=740, y=620)
        GPTButton.place(x=760, y=20)
        errorAnalyse.place(x=360, y=20)
        restartBut.place(x=850, y=20)
        run_LanguageBut.place(x=250, y=20)

        textscroll.config(command=input1.yview)
        textscroll.config(command=input2.yview)

        # var_1 = BooleanVar()
        # checkbox = Checkbutton(root, text='Dets Apps', padx=3, pady=3, highlightbackground='red', variable=var_1, onvalue=True, offvalue=False)
        # checkbox.place(x=50, y=64)

        def returnBox():
            analyseValue(mode="inf")
            combo_box['values'] = list(range(1,len(analyseValue())+1))

        combo_box = ttk.Combobox(root, width=15)
        combo_box.bind('<<ComboboxSelected>>', check_input)
        combo_box.place(x=485, y=25)

        root.mainloop()

if __name__ == "__main__":
    GUI().mainRun()