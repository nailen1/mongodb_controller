# MongoDB Query Execution Plan Analysis

## Query Overview

아래의 aggregation pipeline은 주식 데이터에서 특정 필드들을 추출하고 정렬하는 작업을 수행합니다:

```python
pipeline = [
    {"$match": {"영업일": {"$ne": "합계"}}},  # 영업일이 "합계"가 아닌 문서만 선택
    {"$project": {
        "_id": 0,
        "영업일": 1,
        "종목코드": 1,
        "기준가": 1
    }},  # 필요한 필드만 선택
    {"$sort": {"영업일": 1}}  # 영업일 기준으로 오름차순 정렬
]
```

## Query Execution Plan Analysis

`pymongoexplain` 모듈을 사용하여 쿼리의 실행 계획을 분석할 수 있습니다:

```python
from pymongoexplain import ExplainableCollection

expl = ExplainableCollection(collection).aggregate(pipeline)
```

### 실행 계획 분석 포인트

1. **$match 스테이지**
   - 첫 번째 스테이지에서 "영업일" 필드가 "합계"가 아닌 문서들을 필터링
   - 인덱스가 없다면 전체 컬렉션 스캔(COLLSCAN)이 발생할 수 있음
   - 최적화를 위해 `{"영업일": 1}` 인덱스 생성 고려

2. **$project 스테이지**
   - 필요한 필드만 선택하여 메모리 사용량 최적화
   - `_id` 필드를 제외하여 불필요한 데이터 전송 방지

3. **$sort 스테이지**
   - "영업일" 필드로 정렬 수행
   - 인덱스가 없다면 메모리에서 정렬 작업 수행 (in-memory sort)
   - 대용량 데이터의 경우 정렬에 상당한 메모리 사용
   - 최적화를 위해 `{"영업일": 1}` 인덱스 활용 가능

### 성능 최적화 권장사항

1. **인덱스 생성**
   ```python
   collection.create_index([("영업일", 1)])
   ```
   - $match와 $sort 스테이지 모두에서 활용 가능
   - 정렬 작업의 메모리 사용량 감소
   - 쿼리 실행 속도 향상

2. **프로젝션 최적화**
   - 필요한 필드만 선택하여 메모리 및 네트워크 대역폭 절약
   - 현재 쿼리는 이미 최적화된 프로젝션 사용 중

3. **배치 처리 고려**
   - 대용량 데이터 처리 시 `cursor` 활용
   - 메모리 사용량 제어를 위해 적절한 배치 크기 설정

## 모니터링 및 튜닝

1. **실행 계획 모니터링**
   ```python
   # 실행 계획 확인
   expl = ExplainableCollection(collection).aggregate(pipeline)
   print(expl)
   ```

2. **성능 메트릭 확인**
   - 실행 시간
   - 스캔한 문서 수
   - 반환된 문서 수
   - 사용된 인덱스
   - 메모리 사용량

3. **인덱스 사용 현황**
   ```python
   # 현재 인덱스 확인
   collection.list_indexes()
   ```

## 주의사항

1. 인덱스는 쓰기 작업의 성능에 영향을 미칠 수 있으므로, 실제 사용 패턴을 고려하여 생성
2. 대용량 정렬 작업 시 충분한 메모리 확보 필요
3. 실행 계획은 데이터 분포에 따라 달라질 수 있으므로 주기적인 모니터링 필요
