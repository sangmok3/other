#!/usr/local/bin/python
# -*- coding:utf-8 -*-

from os import getenv
import pymssql
import pandas as pd
import sys
import os
import datetime as dt
import math

if __name__ == "__main__" : 
    day = dt.datetime.today().strftime("%m%d")
    print(os.getcwd())
    save_path = os.getcwd()

    query = input("쿼리를 입력해주세요. 마지막엔 idx= 이런 식으로 끝내주세요. with(nolock)필수!")
    queryt = query.split(' ')
    print(query)

    f = open(queryt[0], 'r')
    ff = f.readline()
    f.close()

    if ff.find('where') == -1 : 
        querys = ff + ' where ta.account_id in('
    else :
        querys = ff + ' and ta.account_id in('


    path = input("유저IDX파일을 넣어주세요.('.csv')")
    paths = path.split(' ')

    #filename추출
    e = [x[0] for x in enumerate(path) if x[1] in '.'][0]
    s = [x[0] for x in enumerate(path) if x[1] in '/'][-1]
    file_name = path[s+1:e]

    print('기다려주세요.....')

    # save_path를 만들기 위해 path의 '/'를 체크해 마지막 '/'위치 인덱스 +1 까지 짤라서 경로 생성
    cnt = 0
    save_path=[]
    for i in range(len(path)):
        if path[i]== '/':
            cnt += 1
            if cnt == path.count('/'):
                    save_path = path[0:i+1]


    rf = open(paths[0], 'r')
    print('파일 로딩 완료!')
    kk = 0
    data = []

    conn = pymssql.connect(server='DB정보', user='정보', password='비번', database='디비명')
    cursor = conn.cursor()  

    df = pd.read_csv(rf)
    idx_list = df['account_id'].values.tolist()

    k = 0
    k1 = 1000
    #dd = pd.read_csv('./bulk_kkb/user_idx_kko.csv')
    
    for i in range(math.ceil(len(df)/1000)):
        idx = idx_list[k:k1]

        select = querys+"%s"%idx+")"
        selects = select.replace('[','').replace(']','')

        try:
            cursor.execute(selects)
        except pymssql.Error as e:
            print ("SQL Error ")
            conn.rollback() 
            cursor.close()
            conn.close()
            sys.exit(2)

        data = pd.DataFrame(cursor.fetchall())
        data.to_excel(save_path+"/"+file_name+"_"+str(day)+str(k)+".xlsx",index=False)
        #dk = pd.concat([dd,data],axis = 0)
        print(data)
        #dk.to_excel(save_path+"/"+file_name+"_"+str(day)+".xlsx",index=False)
        k += 1000
        k1 += 1000
    cursor.close()
    conn.close()
    rf.close()
    #rf = pd.DataFrame(data) 
    #df.to_excel(save_path+"/"+file_name+"_"+str(day)+".xlsx",index=False)

    print("END")
    #wrf = open('20221221write.xlsx','w', newline='')
    #wr = csv.writer(wrf)
    #wr.writerows(data)
    #wrf.close()
