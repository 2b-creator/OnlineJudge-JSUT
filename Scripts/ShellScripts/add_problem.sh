curl -X POST http://192.168.1.107:8000/api/add_problem \
-H "Content-Type: application/json" \
-H "access-token: your-access-token" \
-d '{
  "title": "等差数列求和",
  "problem_char_id": "addArithmeticSequence",
  "description": "这是 JSUT-OJ 的公式试机题, 给定一个等差数列 ${a_n}$, 其通项公式为 $a_n=cn+d,(c,d \\in \\mathbb{R},n \\in \\mathbb{Z^+})$, 求该数列的前 $n$ 项和. ",
  "input_description": "输入一行, 包括 $3$ 个整数 $c,d,n$. ",
  "output_description": "输出一个数字 $S$, 是为 ${a_n}$ 的前 $n$ 项的求和结果；输入数据保证输出数据在 $[-2^{31},2^{31}-1]$ 范围内. ",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'
