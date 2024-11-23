curl -X POST http://192.168.1.107:8000/api/add_problem \
-H "Content-Type: application/json" \
-H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczMjQyNzAzMn0.k3gi3ALt8lPz-OLQcQvP4sRoykedZzAbjm3wPV4He1g" \
-d '{
  "title": "JSUT-OJ 试机题",
  "problem_char_id": "addTwoNum",
  "description": "不要笑！这题见证了 JSUT-OJ 项目的开始，也是作为一个 oier 梦的起点。请你求出输入两个数的和，空格隔开。",
  "input_description": "输入只有一行，包括 $2$ 个整数 $a,b$",
  "output_description": "输出一个数字，是为 $a+b$ 的求和结果",
  "sample_input": "3 3",
  "tag": "测试",
  "sample_output": "6",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'
