curl -X POST http://192.168.1.107:8000/api/register \
-H "Content-Type: application/json" \
-d '{
  "username": "123",
  "stu_id": "dsax",
  "password_hash_cm": "cmcm",
  "email_cm": "aaaaaa@aaa.com"
}'
