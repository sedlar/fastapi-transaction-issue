This project should demonstrate issue with rollbacking of transaction.

To reproduce the issue execute following commands
```bash
docker-compose build
docker-compose up
curl -X 'POST' \
  'http://localhost:8000/notes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "test note",
  "completed": true
}'
docker exec -it fastapi-transaction-issue_db_1 psql -U postgres -d postgres -c "select * from notes;"
```
***Expected result:***

The `notes` table should not contain any rows since the transaction was rollbacked.

***Actual result:***

The record is stored in the db.
