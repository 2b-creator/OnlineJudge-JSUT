curl -X POST http://127.0.0.1:5000/api/add_problem/upload_sample/in \
    -F "file=@need-submit.in" \
    -F "json={\"problem_char_id\": \"multi\"}" \
    -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN4YyIsImV4cCI6MTczMjE5Njc0OX0.Q2PelgrWKlLBjH1iMZyUgyfK6LcYizZfu_9DXlpvhD4"
