curl -X POST http://192.168.1.107:8000/api/submit \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczMjcxNTc2Nn0.DDV_i93CELcFStUZUH7bf5nS2evA-fQC8qy3bb0JXfY" \
-d '{
  "id": 7,
  "code": "#include <stdio.h>\nint main(){int a=1,b=2; scanf(\"%d %d\",&a,&b); printf(\"%d\",a+b);}",
  "language": "cpp"
}'
