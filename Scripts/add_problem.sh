curl -X POST http://127.0.0.1:5000/api/add_problem \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN4YyIsImV4cCI6MTczMjE5Njc0OX0.Q2PelgrWKlLBjH1iMZyUgyfK6LcYizZfu_9DXlpvhD4" \
-d '{
  "title": "problem_2",
  "problem_char_id": "multi",
  "description": "multiply 2 nums",
  "input_description": "a and b",
  "output_description": "a+b",
  "sample_input": "2 2",
  "sample_output": "4",
  "difficulty": "easy",
  "time_limit": 1,
  "memory_limit": 128
}'