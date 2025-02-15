# 上传题目指南

```
Problems/
├── 1/                                  # 题目目录，请使用自增 int 作为目录名称
│   ├── config.toml                     # 配置文件
│   ├── data_range.md                   # 描述数据范围
│   ├── input_description.md            # 输入描述
│   ├── output_description.md           # 输出描述
│   ├── problem.md                      # 题目正文
│   ├── sample/                         # 样例文件夹，请使用自增 int 作为文件名称
│   │   ├── 1.in
│   │   ├── 1.md                        # 样例解释
│   │   └── 1.out
│   └── test/                           # 测试点文件夹，请使用自增 int 作为文件名称
│       ├── 1.in
│       ├── 1.out
│       ├── 2.in
│       └── 2.out
└── 2/
    ├── config.toml
    ├── data_range.md
    ├── input_description.md
    ├── output_description.md
    ├── problem.md
    ├── sample/
    │   ├── 1.in
    │   ├── 1.md
    │   └── 1.out
    └── test/
        ├── 1.in
        ├── 1.out
        ├── 2.in
        └── 2.out
```

## config.toml

```toml
[problem]
problem_char_id = "APlusBProblem"       # 题目唯一标识符
title = "两数相加"
difficulty = 1                          # 难度

[limit]
time = 2                                # 时间限制(s)
memory = 128                            # 内存限制(mb)

[special]
judge = false                           # 特殊 judge，请提交 checker
score = false                           # 特殊判分，请提交 clac.py
```

