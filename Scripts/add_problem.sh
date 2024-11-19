curl -X POST http://127.0.0.1:5000/api/add_problem \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN4YyIsImV4cCI6MTczMjE5Njc0OX0.Q2PelgrWKlLBjH1iMZyUgyfK6LcYizZfu_9DXlpvhD4" \
-d '{
  "title": "problem_1",
  "problem_char_id": "sum",
  "description": "add 2 nums",
  "input_description": "a and b",
  "output_description": "a+b",
  "sample_input": "1 1",
  "sample_output": "2",
  "difficulty": "easy",
  "time_limit": 1,
  "memory_limit": 128
}'