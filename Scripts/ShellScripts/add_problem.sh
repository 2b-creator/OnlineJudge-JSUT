curl -X POST http://192.168.1.107:8000/api/add_problem \
-H "Content-Type: application/json" -H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjEyMyIsImV4cCI6MTczMjQyNjM0Nn0.5i2VEA_4qJ0TXHj8oikdMhMLSAcXyweXPSlVNq5nsWM" \
-d '{
  "title": "problem_3",
  "problem_char_id": "add",
  "description": "add 2 nums",
  "input_description": "a and b",
  "output_description": "a*b",
  "sample_input": "3 3",
  "sample_output": "9",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'