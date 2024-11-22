curl -X POST http://192.168.1.107:8000/api/add_problem \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczMjQyNzAzMn0.k3gi3ALt8lPz-OLQcQvP4sRoykedZzAbjm3wPV4He1g" \
-d '{
  "title": "problem_2",
  "problem_char_id": "multi",
  "description": "multiply 2 nums",
  "input_description": "a and b",
  "output_description": "a*b",
  "sample_input": "3 3",
  "tag": "test",
  "sample_output": "9",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'