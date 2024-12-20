
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as BSoup
import win32com.client


def open_Excel(visible=False):
    '''
    엑셀 열기
    - visible <bool> : 엑셀에 작업되는 상황 보이기 (기본값=False)
    - 반환값 <엑셀 객체> : 엑셀 객체 생성해서 반환
    '''
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = visible
    excel.DisplayAlerts = False
    return excel


def close_Excel(excel):
    '''
    엑셀 닫기
    - excel <엑셀 객체> : 열었던 엑셀 객체
    '''
    excel.DisplayAlerts = True
    excel.Quit()


def get_news_dataframe(day):
    url_base = 'https://finance.naver.com'
    url = url_base + f'/news/mainnews.naver?date={day}'
    
    data = []
    page_num = 1
    while True:
        html = requests.get(f'{url}&page={page_num}').text
        soup = BSoup(html, 'html.parser')

        for news in soup.find_all('li', 'block1'):
            subject = news.find('dd', 'articleSubject')
            title = subject.text.strip()
            link = url_base + subject.a['href']
            summary = news.find('dd', 'articleSummary')
            content = summary.contents[0].strip()
            press = summary.find('span', 'press').text
            date = summary.find('span', 'wdate').text
            data.append([title, content, press, date, link])
            # print(link, title, content, press, date, sep='\n')

        page_num += 1
        # 다음 페이지가 없으면 종료
        if soup.select_one('.pgRR') is None:
            break
    return pd.DataFrame(data, columns=['제목', '내용', '언론사', '날짜', 'URL'])


def insert_news_file(filePath, sheet, startRow, startCol, today):
    try:
        df = get_news_dataframe(today)
        result = f'뉴스를 가져왔습니다. ({len(df)}행)'
    except Exception as e:
        result = f'에러 발생: {e}'
        return result
    finally:
        print(result)

    try:
        excel = open_Excel()
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
        result = f'{sheet}가 정상적으로 삽입되었습니다. ({today})'
    except Exception as e:
        result = f'에러 발생: {e}'
    finally:
        close_Excel(excel)
        print(result)
    return result



# 연습예제
if __name__ == '__main__':
    fileFolder = "C:\\Users\\Dexter\\Source\\ALPACO8\\RPA_Example\\21_오늘의_증권시황\\Data\\Output"
    filePath = os.path.join(fileFolder, "Today_Stock_Information_2024-12-20.xlsx")
    insert_news_file(filePath, '주요뉴스', 3, 3, '2024-12-20')