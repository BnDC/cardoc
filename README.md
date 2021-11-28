# 원티드x위코드 백엔드 프리온보딩 과제7 :: Cardoc

# 배포 주소 : 3.34.144.69

# 1. Member

#### 김주형 : https://github.com/BnDC

# 2. 과제

- **[필수 포함 사항]**

  - READ.ME

     작성

    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - **서버 구조 및 디자인 패턴에 대한 개략적인 설명**
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅

  - Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

#### 1. 배경 및 공통 요구사항

 😁 **카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.**

- 데이터베이스 환경은 별도로 제공하지 않습니다. **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.
- 단, 결과 제출 시 [README.md](http://README.md) 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.
- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.
- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.
- 200 OK	성공
  400 Bad Request   Parameter가 잘못된 (범위, 값 등)
  401 Unauthorized 인증을 위한 Header가 잘못됨
  500 Internal Server Error 기타 서버 에러

------

#### 2. 사용자 생성 API

🎁 **요구사항**

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

```jsx
/* Request Body 예제 */

 { "id": "candycandy", "password": "ASdfdsf3232@" }
```

------

#### 3. 사용자가 소유한 타이어 정보를 저장하는 API

🎁 **요구사항**

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.
- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다. 즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

```jsx
/* Request Body 예제 */
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

🔍 **상세구현 가이드**

- 자동차 정보 조회 API의 사용은 아래와 같이 5000, 9000부분에 trimId를 넘겨서 조회할 수 있다. **자동차 정보 조회 API 사용 예제 → 📄** https://dev.mycar.cardoc.co.kr/v1/trim/5000 **📄** https://dev.mycar.cardoc.co.kr/v1/trim/9000 📄 https://dev.mycar.cardoc.co.kr/v1/trim/11000 📄 https://dev.mycar.cardoc.co.kr/v1/trim/15000
- 조회된 정보에서 타이어 정보는 spec → driving → frontTire/rearTire 에서 찾을 수 있다.
- 타이어 정보는 205/75R18의 포맷이 정상이다. 205는 타이어 폭을 의미하고 75R은 편평비, 그리고 마지막 18은 휠사이즈로써 {폭}/{편평비}R{18}과 같은 구조이다. 위와 같은 형식의 데이터일 경우만 DB에 항목별로 나누어 서로다른 Column에 저장하도록 한다.

------

#### 4. 사용자가 소유한 타이어 정보 조회 API

🎁 **요구사항**

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.

# 3. Skill & Tools

> **Skill :** [![img](https://camo.githubusercontent.com/0f3eb5f3e4c61d94657f16605ea420a0216673dfb085d100c458ed15be0599d2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f7374796c653d666f722d7468652d6261646765266c6f676f3d507974686f6e266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/0f3eb5f3e4c61d94657f16605ea420a0216673dfb085d100c458ed15be0599d2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f7374796c653d666f722d7468652d6261646765266c6f676f3d507974686f6e266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/c4c1014e1f168ff271282b67ec9059c3cfc16b2a5cba6e0c7c98c3530f47f45c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d3039324532303f7374796c653d666f722d7468652d6261646765266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/c4c1014e1f168ff271282b67ec9059c3cfc16b2a5cba6e0c7c98c3530f47f45c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d3039324532303f7374796c653d666f722d7468652d6261646765266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465)  [![img](https://camo.githubusercontent.com/3b7fc1e7ec40da4600edd856f469a213594a031b9dc594d7ea122bc9ad01cac5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a57542d3233324633453f7374796c653d666f722d7468652d6261646765266c6f676f3d4a5754266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/3b7fc1e7ec40da4600edd856f469a213594a031b9dc594d7ea122bc9ad01cac5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a57542d3233324633453f7374796c653d666f722d7468652d6261646765266c6f676f3d4a5754266c6f676f436f6c6f723d7768697465) ![image](https://camo.githubusercontent.com/9bf3ab62e0f872ed37f7d590e4577137b2dda11ffb0786f9b858cd39c2dc8c7f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f73716c6974652d3039324532303f7374796c653d666f722d7468652d6261646765266c6f676f3d73716c697465266c6f676f436f6c6f723d23303033423537)


> **Depoly :** [![img](https://camo.githubusercontent.com/9ad32f291fa1163a77cd2e919f8378b38bf66fd9de517178bf890e521178f341/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f415753204543322d3233324633453f7374796c653d666f722d7468652d6261646765266c6f676f3d416d617a6f6e20415753266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/9ad32f291fa1163a77cd2e919f8378b38bf66fd9de517178bf890e521178f341/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f415753204543322d3233324633453f7374796c653d666f722d7468652d6261646765266c6f676f3d416d617a6f6e20415753266c6f676f436f6c6f723d7768697465)


> **ETC :** [![img](https://camo.githubusercontent.com/fdb91eb7d32ba58701c8e564694cbe60e706378baefa180dbb96e2c1cfb9ec0f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769742d4630353033323f7374796c653d666f722d7468652d6261646765266c6f676f3d476974266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/fdb91eb7d32ba58701c8e564694cbe60e706378baefa180dbb96e2c1cfb9ec0f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769742d4630353033323f7374796c653d666f722d7468652d6261646765266c6f676f3d476974266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/23a917c56e310800a66c58a03447dd42c0dea2abff415ef9719e3e837c1cff82/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769746875622d3138313731373f7374796c653d666f722d7468652d6261646765266c6f676f3d476974687562266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/23a917c56e310800a66c58a03447dd42c0dea2abff415ef9719e3e837c1cff82/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769746875622d3138313731373f7374796c653d666f722d7468652d6261646765266c6f676f3d476974687562266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/879423585ed087f3c973857c43ba7e7d84f52c993d2c937055726339fbf921d9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f506f73746d616e2d4646364333373f7374796c653d666f722d7468652d6261646765266c6f676f3d506f73746d616e266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/879423585ed087f3c973857c43ba7e7d84f52c993d2c937055726339fbf921d9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f506f73746d616e2d4646364333373f7374796c653d666f722d7468652d6261646765266c6f676f3d506f73746d616e266c6f676f436f6c6f723d7768697465)

------

# 4. 모델링

![image](https://user-images.githubusercontent.com/86050295/143781805-c5c53a06-f2b3-498a-b87d-56c594808306.png)

------

# 5. Postman API 테스트

### API 테스트 : https://www.postman.com/telecoms-participant-79983274/workspace/test

### API 명세서 : https://documenter.getpostman.com/view/17713356/UVJckGK2

### 기본 주소는 배포주소로 되어 있으며, 콜렉션 fork 후 테스트 부탁드립니다.

### Data Reference

유저 정보

id : "user1@naver.com"

id : "user2@naver.com"

id : "user3@naver.com"

id : "user9@naver.com"

password : 'abc1234' (공통)

------

# 6. 구현 사항 상세 설명

### 1. POST /users/signup (회원가입)

#### **body Key list**

```javascript
[
  {
    "id"     : (유저 이메일),
    "password" : (유저 비밀번호)
  }
]
```

400 code 반환

- id가 중복

- body에 올바르지 않은 key값,

- 빈 body

예외에 해당하지 않는경우

입력받은 아이디(이메일)와/과 bcrypt를 이용해 암호한 비밀번호를 database에 저장

회원가입 성공 200 code 반환

### 2. POST /users/signin (로그인)

#### **body Key list**

```javascript
{
  "id": "(유저 이메일)",
  "password": "(유저 비밀번호)"
}

```
400 code를 반환

- id가 존재하지 않을 때,

- body에 올바르지 않은body의 key,

- 요청에 빈 body, 

401 code를 반환
- 존재하지 않은 id(email)
- 올바르지 않은 비밀번호

예외에 해당하지 않는 경우

아이디와 비밀번호를 입력받아 로그인 성공시 jwt token과 200을 반환


### 3. POST /trims (타이어 정보 저장)

#### **body Key list**

```javascript
[
  {
    "id" : (유저 이메일),
    "trimId" : (trim 아이디)
  },
  .
  .
  .
  
  {
    "id" : (유저 이메일),
    "trimId" : (trim 아이디)
  }
]
```

400 code를 반환
- body의 요청 데이터가 없거나, 5쌍을 초과
- cardoc의 api에서 받은 요청이 200이 아닌 경우
- tire 정보가 형식에 맞지 않는 경우
(tire의 형식: {바퀴 폭}{편평비}R{바퀴 크기} ex 225/60R16)

예외에 해당하지 않는 경우

tire와 trim 데이터를 생성 하고 200 code를 반환

### 4. GET /trims (유저의 타이어 정보 조회)
```
#headers에 포함
{ "Authorization" : access_token}
```

로그인 데코레이터를 이용하여, 토큰이 유효하지 않으면 401 code가 반환

로그인한 유저가 소유한 trim의 front/rear tire들의 정보를 조회하고,

성공시 200 code를 반환

------

# 7. UnitTest 결과

![image](https://user-images.githubusercontent.com/86050295/143784920-d8ad1ea4-5ff8-4cc4-9237-17d42c8f57d4.png)

# 8. Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다. 감사합니다.
