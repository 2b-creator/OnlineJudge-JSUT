curl -X POST http://127.0.0.1:5000/api/submit \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN4YyIsImV4cCI6MTczMjE5Njc0OX0.Q2PelgrWKlLBjH1iMZyUgyfK6LcYizZfu_9DXlpvhD4" \
-d '{
  "problem_id": "sum",
  "code": "#include <stdio.h>\nint main(){int a=1,b=2; scanf(\"%d %d\",&a,&b); printf(\"%d\",a+b);}",
  "language": "cpp"
}'
