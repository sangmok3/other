import datetime as dt
import fileinput
import pandas as pd
import os

if __name__ == "__main__" : 
    print("Start.") 
    day = dt.datetime.today().strftime("%m%d")

    print(os.getcwd())
    save_path = os.getcwd()

    path = input('파일을 넣어주세요.\n')
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
                
                
    df = pd.read_excel(paths[0],engine = 'openpyxl')
    print('파일 로딩 완료!')

    num = input('쪼갤 숫자를 입력하세요.\n')
    num = int(num)
    d_cnt = int(len(df)/num)
    print('분할을 시작합니다!')
    
    for k in range(0,num-1):
        globals()['df' + str(k)] = df.iloc[k*d_cnt:(k+1)*d_cnt]
        globals()['df' + str(k)].to_excel(save_path+"/"+file_name+"_"+str(k+1)+".xlsx",index=False)
        print("저장경로:"+save_path+"/")
        print(str(k+1)+'번째 파일 생성 완료')

    globals()['df' + str(num-1)] = df.iloc[(num-1)*d_cnt:]
    globals()['df' + str(num-1)].to_excel(save_path+"/"+file_name+"_"+str(num)+".xlsx",index=False)
    print(str(num)+'번째 파일 생성 완료')
    print("파일 생성을 완료했습니다.")
    print("End")