# coding = utf-8
import requests
import json
from tkinter import *

tk =Tk()
tk.title('코로나19')
label1 = Label(tk, text='날짜').grid(row=0,column=0)
label2 = Label(tk, text='구분').grid(row=1,column=0)
label3 = Label(tk, text='출력값').grid(row=2,column=0)

entry1 = Entry(tk)
entry2 = Entry(tk)
entry3 = Entry(tk)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)

label4_text = StringVar()
label4_text.set('')
label4 =Label(tk, textvariable=label4_text).grid(row=3, column=1)

label5_text = StringVar()
label5_text.set('')
label5 =Label(tk, textvariable=label5_text).grid(row=4, column=1)

date = entry1.get()
gubun = entry2.get()
item = entry3.get()

def getcovid():
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
    params = {'serviceKey': 'hAwTbwaP+RQ+NtMvgUeSQQRsygJHC4cQRLNyYL4rqCPkKDfH+pkYrGiEME2aO9GekhEM0qqE6Dx+7wU0fmNfOw==',
              'pageNo': '1',
              'numOfRows': '500',
              'apiType': 'json',
              'create_dt': date}

    response = requests.get(url, params=params)
    print(response)
    contents = response.text

    a = []
    start = 0
    printcheck = 0
    for c in contents.split('\n'):
        newc = c.replace('\r', '')
        newc = newc.strip()
        if '<item>' in newc:
            a.append(newc)
            start = 1
        elif '</item>' in newc:
            a.append(newc)
            if a[-2] == '<gubun>' + gubun + '</gubun>':
                b = ''
                if item == '확진자수':
                    b = a[1]
                    b = b.replace('<confCase>', ' ')
                    b = b.replace('</confCase>', ' ')
                elif item == '확진율':
                    b = a[2]
                    b = b.replace('<confCaseRate>', ' ')
                    b = b.replace('</confCaseRate>', ' ')
                elif item == '치명률':
                    b = a[4]
                    b = b.replace('<criticalRate>', ' ')
                    b = b.replace('</criticalRate>', ' ')
                elif item == '사망자수':
                    b = a[5]
                    b = b.replace('<death>', ' ')
                    b = b.replace('</death>', ' ')
                elif item == '사망률':
                    b = a[6]
                    b = b.replace('<deathRate>', ' ')
                    b = b.replace('</deathRate>', ' ')
                print('{}에 {}에 {}은{}'.format(date, gubun, item, b))
                printcheck = 1

                label4_text.set('{}에 {}에 {}은 {}'.format(date, gubun, item, b))
            start = 0
            a = []
        elif start == 1:
            a.append(newc)
    if printcheck == 0:
        print('데이터 오류 발생!')
        label4_text.set('데이터 오류 발생!')
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_12/callCovid12Api'
    params = {'serviceKey': "hAwTbwaP+RQ+NtMvgUeSQQRsygJHC4cQRLNyYL4rqCPkKDfH+pkYrGiEME2aO9GekhEM0qqE6Dx+7wU0fmNfOw==",
              'pageNo': '1',
              'numOfRows': '500',
              'apiType': 'json',
              'std_day': date}
    response = requests.get(url, params=params)
    contents = response.text
    a = []
    start = 0
    for c in contents.split('\n'):
        newc = c.replace('\r', '')
        newc = newc.strip()
        if '<item>' in newc:
            a.append(newc)
            start = 1
        elif '</item>' in newc:
            a.append(newc)
            start = 0
            b = a[2]
            b = b.replace('<socdisLvl>', ' ')
            b = b.replace('</socdisLvl>', ' ')
            print('거리두기 단계는{}'.format(b))
            label5_text.set('거리두기 단계는{}'.format(b))
            printcheck = 1
            a = []
        elif start == 1:
            a.append(newc)
    if printcheck == 0:
        print('데이터 오류 발생!')
        label5_text.set('데이터 오류 발생!')
btn1= Button(tk,text='실행',bg='black',fg='white',command=getcovid).grid(row=6, column=3)

tk.mainloop()
