# Примеры запросов 

## POST /api/auth/token/

```bash
curl -X POST http://localhost:8000/api/auth/token/ -d username=root -d password=root
```

```bash
TOKEN=<token>
```

## GET /api/polls/

```bash
curl -s http://localhost:8000/api/polls/ -H "Authorization: Token $TOKEN"
```

## GET /api/polls/6/next-question/

```bash
curl -s http://localhost:8000/api/polls/6/next-question/ -H "Authorization: Token $TOKEN"
```

## POST /api/polls/6/choices/

```bash
curl -s -X POST http://localhost:8000/api/polls/6/choices/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"answer": 7, "answer_text": "Хорошо"}'
```

```bash
curl -s -X POST http://localhost:8000/api/polls/6/choices/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"answer": 8, "answer_text": "30"}'
```

```bash
curl -s -X POST http://localhost:8000/api/polls/6/choices/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"answer": 9}'
```

## GET /api/polls/6/stats/

```bash
curl -s http://localhost:8000/api/polls/6/stats/ -H "Authorization: Token $TOKEN"
```


Пользователи отличаются настройками в профиле. Всем авторизованым доступно прохождение опросов, редакторам и админам доступно получение статистики, опросы создаются через интерфейс админки.
