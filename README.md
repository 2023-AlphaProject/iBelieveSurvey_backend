# IBelieveSurvey

## Commands

### 빌드

```shell
docker-compose up -d --build
```

### 로그 보기

```shell
## 전체
docker-compose logs -f

## webapp 로그 보기
docker-compose logs -f django
```

### 슈퍼 유저 생성

```shell
docker-compose run --rm django python manage.py createsuperuser
```

### 마이그레이션 생성

```shell
docker-compose run --rm django python manage.py makemigrations
```


### ERD
![image](https://user-images.githubusercontent.com/90228925/225353284-aad095b4-1880-4473-829f-29816290857c.png)
