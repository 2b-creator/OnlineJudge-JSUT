curl -X POST http://192.168.1.107:8000/api/add_problem \
-H "Content-Type: application/json" \
-H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczMjQyNzAzMn0.k3gi3ALt8lPz-OLQcQvP4sRoykedZzAbjm3wPV4He1g" \
-d '{
  "title": "等差数列求和",
  "problem_char_id": "addArithmeticSequence",
  "description": "这是 JSUT-OJ 的公式试机题, 给定一个等差数列 ${a_n}$, 其通项公式为 $a_n=cn+d,(c,d \\in \\mathbb{R},n \\in \\mathbb{Z^+})$, 求该数列的前 $n$ 项和. ",
  "input_description": "输入一行, 包括 $3$ 个整数 $c,d,n$. ",
  "output_description": "输出一个数字 $S$, 是为 ${a_n}$ 的前 $n$ 项的求和结果；输入数据保证输出数据在 $[-2^{31},2^{31}-1]$ 范围内. ",
  "sample_input": "2 1 10",
  "tag": "测试 求和",
  "sample_output": "120",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'
