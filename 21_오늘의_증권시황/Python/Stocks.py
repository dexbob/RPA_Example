try:
    import os
    import win32com.client
    print('모듈이 성공적으로 로드되었습니다.')
except ImportError as e:
    print(f'에러 발생: {e}')


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


def insert_image_one(filePath, sheet, cell, imagePath, width, height):
    '''
    대상 엑셀 파일내 시트의 입력된 셀에 이미지 사이즈를 조정하여 삽입 실행 
    - filePath <str> : 엑셀 파일 경로
    - sheet <int | str> : 대상 파일 시트 (숫자는 시트인덱스, 문자는 시트명)
    - cell <str> : 셀 위치 문자열 (예: 'A1')
    - imagePath <str> : 이미지 파일 경로
    - width <int> : 너비
    - height <int> : 높이
    - 반환값 <str> : 처리 결과 문자열
    '''
    print(filePath)
    print(imagePath)
    try:
        excel = open_Excel()
        wb = excel.Workbooks.Open(filePath)
        ws = wb.Worksheets(sheet)
        cell = ws.Range(cell)
        ws.Shapes.AddPicture(Filename=imagePath, 
            LinkToFile=False, SaveWithDocument=True, 
            Left=cell.Left, Top=cell.Top, 
            Width=width, Height=height)
        wb.Save()
        result = f'이미지가 정상적으로 삽입되었습니다. ({cell})'
    except Exception as e:
        result = f'에러 발생: {e}'
    finally:
        close_Excel(excel)
    return result


def insert_image_all_path(filePath, sheet, cellArr, imagePathArr, width, height):
    '''
    대상 엑셀 파일내 시트의 입력된 셀들에 모든 이미지 사이즈를 조정하여 전부 삽입 실행 
    - filePath <str> : 엑셀 파일 경로
    - sheet <int | str> : 대상 파일 시트 (숫자는 시트인덱스로 1부터 시작, 문자는 시트명)
    - cellArr <list(str)> : 셀 위치 문자열 배열 (예: ['A1', 'C5'])
    - imagePathArr <list(str)> : 이미지 파일 경로 문자열 배열 (예: ['folder\img1.png', 'folder\img2.png'])
    - width <int> : 너비
    - height <int> : 높이
    - 반환값 <str> : 처리 결과 문자열
    '''
    print(filePath)
    result = filePath
    try:
        excel = open_Excel()
        wb = excel.Workbooks.Open(filePath)
        ws = wb.Worksheets(sheet)
        for i in range(len(cellArr)):
            print(imagePathArr[i])
            result += imagePathArr[i] + '\r\n'
            cell = ws.Range(cellArr[i])
            ws.Shapes.AddPicture(Filename=imagePathArr[i], 
                LinkToFile=False, SaveWithDocument=True, 
                Left=cell.Left+1, Top=cell.Top+1, 
                Width=width, Height=height)
        wb.Save()
        result = '이미지가 정상적으로 삽입되었습니다.'
    except Exception as e:
        result = f'에러 발생: {e}'
    finally:
        close_Excel(excel)
    return result


def insert_image_all_file(filePath, sheet, cellArr, imageFolder, imageFileArr, width, height):
    '''
    대상 엑셀 파일내 시트의 입력된 셀들에 모든 이미지 사이즈를 조정하여 전부 삽입 실행 
    (이미지 폴더 경로를 이미지 파일 배열과 결합하여 각각의 이미지 파일 경로 생성)  
    - filePath <str> : 엑셀 파일 경로
    - sheet <int | str> : 대상 파일 시트 (숫자는 시트인덱스로 1부터 시작, 문자는 시트명)
    - cellArr <list(str)> : 셀 위치 문자열 배열 (예: ['A1', 'C5'])
    - imageFolder <str> : 전체 이미지 파일이 존재하는 폴더 경로
    - imagePathArr <list(str)> : 이미지 파일 경로 문자열 배열 (예: ['folder\img1.png', 'folder\img2.png'])
    - width <int> : 너비
    - height <int> : 높이
    - 반환값 <str> : 처리 결과 문자열
    '''
    imagePathArr = [os.path.join(imageFolder, name) for name in imageFileArr]
    return insert_image_all_path(filePath, sheet, cellArr, imagePathArr, width, height)



# 연습예제
if __name__ == '__main__':
    print('<<< TEST >>>')
    fileFolder = 'C:\\Users\\Dexter\\Source\\ALPACO8\\RPA_Example\\21_오늘의_증권시황\\Data\\Output'
    filePath = os.path.join(fileFolder, 'Today_Stock_Information_2024-12-19.xlsx')
    imageFolder = 'C:\\Users\\Dexter\\Source\\ALPACO8\\RPA_Example\\21_오늘의_증권시황'
    imageFileArr = ['Data\\Temp\\다우.png', 'Data\\Temp\\나스닥.png', 'Data\\Temp\\S&P.png']
    cellArr = ['B11', 'E11', 'H11']
    result = insert_image_all_file(filePath, 1, cellArr, imageFolder, imageFileArr, 115, 95)
    print(result)