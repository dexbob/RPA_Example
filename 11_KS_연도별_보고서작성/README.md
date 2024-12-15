## 제목 : KS 연도별 보고서 작성

### 개요 : 웹사이트(ACME) 작업목록 각각의 월간리포트를 병합하여 연간리포트 생성 및 업로드하고 완료상태로 업데이트 한 후 결과 메일 송신

### 내용 : RE프레임워크 사용하여 흐름 제어

1. 초기화 프로세스 - 환경설정객체(Config)생성 및 작업목록 리스트 추출을 위해 비지니스 시작 프로세스(StartProcess) 실행
2. 트랜잭션 데이터 추출 - 작업목록 리스트에서 작업ID 추출, 이전작업에서 시스템에러시 해당 작업ID 재설정
3. 트랜잭션 프로세스 실행 - 해당 트랜잭션 데이터(작업ID)를 이용하여 비지니스 메인 프로세스(MainProcess) 실행 및 실행 상태 변경
4. 종료 프로세스 - 시스템에러 최대개수 초과시 또는 트랜잭션 소진(작업목록 처리완료)시 비지니스 종료 프로세스(EndProcess) 실행

### 상태 : 성공 상태, 비지니스에러 상태, 시스템에러 상태

1. 성공 상태 : 해당 트랜잭션 데이터의 정상 처리 진행
2. 비지니스에러 상태 : 해당 트랜잭션 데이터는 경고 로그 출력하고 미처리 후 다음 트랜잭션으로 진행
3. 시스템에러 상태 : 시스템에러 최대개수 초과하기 전에는 재시도횟수 만큼 해당 트랜잭션 재실행 진행, 최대개수 초과시 프로세스 종료

#### ※ 참고사항

- 기존 RE프레임워크를 수정하되 추가는 있어도 삭제는 하지 않았음 (다른 프로젝트 사용을 위해)
- RE프레임워크의 _InitAllApplications_, _CloseAllApplications_, _KillAllProcesses_ 처리 미사용
- 트랜잭션 마다 화면을 열고 로그인 할 필요가 없어 초기 처리는 _InitTransactionData_ 에서 처리
- 트랜잭션이 소진되어 처리 종료시 이메일 송신이 필요해 종료처리에 추가
- 이후 해당프로젝트만을 위한 RE프레임워크로 수정시 시작과 종료 처리를 _InitAllApplications_, _CloseAllApplications_ 으로 이관할 예정

---

### RE프레임워크(_Robotic Enterprise Framework_)

- _비지니스 트랜잭션 프로세스_ 템플릿 위에 구축
- 자동화 프로젝트 단계에서 _상태 머신_ 레이아웃 사용
- 높은 수준의 로깅, 예외처리 및 복구 기능 제공
- 외부설정을 _Config.xlsx_ 파일 및 Orchestrator 자산(asset)에 유지
- Orchestrator 자산(asset)의 자격증명과 Windows 자격증명 관리자에서 자격증명 가져오기
- 큐 사용시 Orchestrator 대기열에서 트랜잭션 데이터를 가져오고 상태를 다시 업데이트
- 큐 미사용시 추출한 데이터를 데이터테이블에 저장하여 트랜잭션 데이터로 사용
- 시스템 예외 발생시 스크린샷 캡쳐

### Framework 파일 설명 (괄호 내의 내용은 이 프로젝트에 적용한 상황)

1. **초기화 프로세스** (INITIALIZE PROCESS)

   - _InitAllSettings_ : Config.xlsx 파일 및 자산(asset)에서 데이터 로드 (자격증명 처리 추가)
   - _KillAllProcesses_ : 전체 프로세스 강제종료하여 초기화하는 프로세스 (미사용)
   - _InitAllApplications_ : 전체 애플리케이션 초기화 실행 프로세스 (미사용)
   - _InitTransactionData_ : 오케스트레이터의 큐를 미사용시 트랜잭션 데이터 추출 추가 (비지니스 시작 프로세스)

2. **트랜잭션 데이터 추출** (GET TRANSACTION DATA)

   - _GetTransactionData_ : 오케스트레이터의 큐로부터 트랜잭션 추출 (데이터테이블의 데이터로우 추출)

3. **트랜잭션 프로세스 실행** (PROCESS TRANSACTION)

   - _Process_ : 프로세스 추적 및 프로세스 자동화 (비지니스 메인 프로세스)
   - _SetTransactionStatus_ : 오케스트레이터 트랜잭션 상태 업데이트 (성공, 비지니스에러, 시스템에러)
     - _RetryCurrentTransaction_ : 재시도 메커니즘 관리 프로세스
     - _TakeScreenshot_ : 전체 화면 스크린샷 캡처 및 저장 프로세스
     - _CloseAllApplications_ : 전체 애플리케이션 종료 프로세스 (미사용)
     - _KillAllProcesses_ : 전체 프로세스 강제종료하여 초기화하는 프로세스 (미사용)

4. **종료 프로세스** (END PROCESS)
   - _CloseAllApplications_ : 전체 애플리케이션 종료 프로세스 (미사용)
   - _KillAllProcesses_ : 전체 프로세스 강제종료하여 초기화하는 프로세스 (미사용)
