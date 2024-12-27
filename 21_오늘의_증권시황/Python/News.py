# conda install conda-forge::webdriver-manager

import os
import requests
import pandas as pd
import win32com.client
from bs4 import BeautifulSoup as BSoup

def open_excel(visible=False):
    '''
    엑셀 열기
    - visible <bool> : 엑셀에 작업되는 상황 보이기 (기본값=False)
    - 반환값 <엑셀 객체> : 엑셀 객체 생성해서 반환
    '''
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = visible
    excel.DisplayAlerts = False
    return excel


def close_excel(excel):
    '''
    엑셀 닫기
    - excel <엑셀 객체> : 열었던 엑셀 객체
    '''
    excel.DisplayAlerts = True
    excel.Quit()



def convert_url(url):
    '''
    URL에서 article_id와 office_id 추출하여 URL 설정
    url <str> : 변환 대상 url 문자열
    반환값 <str> : 변환된 url
    '''
    params = url.split('?')[-1]
    dic = dict(param.split('=') for param in params.split('&'))
    base_url = 'https://n.news.naver.com/mnews/article'
    return f'{base_url}/{dic["office_id"]}/{dic["article_id"]}'



def get_news_dataframe(day):
    '''
    대상 날짜의 네이버 증권 주요뉴스 추출
    - day <str> : 대상 날짜 (yyyy-MM-dd)
    - 반환값 <DataFrame> : 컬럼명 ('제목', 'URL', '내용', '언론사', '날짜')
    '''
    url_base = 'https://finance.naver.com'
    url = url_base + f'/news/mainnews.naver?date={day}'
    
    data = []
    page_num = 0
    while True:
        page_num += 1
        html = requests.get(f'{url}&page={page_num}').text
        soup = BSoup(html, 'html.parser')

        for news in soup.find_all('li', 'block1'):
            subject = news.find('dd', 'articleSubject')
            title = subject.text.strip()
            link_url = url_base + subject.a['href']
            summary = news.find('dd', 'articleSummary')
            content = summary.contents[0].strip()
            press = summary.find('span', 'press').text
            date = summary.find('span', 'wdate').text
            data.append([title, convert_url(link_url), content, press, date])
            # print(title, link_url, convert_url(link_url), content, press, date, sep='\n')
        
        # 다음 페이지가 없으면 반복 종료
        if soup.select_one('.pgRR') is None:
            break
    return pd.DataFrame(data, columns=['제목', 'URL', '내용', '언론사', '날짜'])



def insert_news_file(filePath, sheet, startRow, startCol, today):
    '''
    대상 날짜의 뉴스 파일 읽어서 엑셀 시트의 임의 위치에 쓰기 실행
    - filePath <str> : 엑셀 파일 경로
    - sheet <int | str> : 대상 파일 시트 (숫자는 시트인덱스로 1부터 시작, 문자는 시트명)
    - startRow <int> : 셀의 시작행
    - startCol <int> : 셀의 시작열
    - today <str> : 오늘 날짜 (yyyy-MM-dd)
    - 반환값 <str> : 처리 결과 문자열
    '''
    try:
        df = get_news_dataframe(today)
        result = f'뉴스를 가져왔습니다. ({len(df)}행)'
    except Exception as e:
        result = f'에러 발생: {e}'
        return result
    finally:
        print(result)

    try:
        excel = open_excel()
        wb = excel.Workbooks.Open(filePath)
        ws = wb.Worksheets(sheet)
        # 제목 삽입
        for c, colTitle in enumerate(df.columns, start=startCol):
            ws.Cells(startRow, c).Value = colTitle
        # 값 삽입
        for r, row in enumerate(df.values, start=startRow+1):
            for c, value in enumerate(row, start=startCol):
                ws.Cells(r, c).Value = value
        wb.Save()
        result = f'{sheet}가 정상적으로 삽입되었습니다. ([{today}] {len(df)}행)'
    except Exception as e:
        result = f'에러 발생: {e}'
    finally:
        close_excel(excel)
        print(result)
    return result



# 연습예제
if __name__ == '__main__':
    # day = '2024-12-22'
    # news_df = get_news_dataframe(day)
    # print(news_df)
    
    fileFolder = "C:\\Users\\Dexter\\Source\\ALPACO8\\RPA_Example\\21_오늘의_증권시황\\Data\\Output"
    filePath = os.path.join(fileFolder, "Today_Stock_Information_2024-12-25.xlsx")
    insert_news_file(filePath, '주요뉴스', 1, 1, '2024-12-25')