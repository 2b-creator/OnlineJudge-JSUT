#!/bin/bash

# Step 1: Read the content of submit.cpp into a variable
codes=$(cat ./submit.cpp)

# Step 2: Escape the content for JSON (replace newlines and quotes)
codes_escaped=$(echo "$codes" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

# Step 3: Construct the JSON payload
json_payload=$(cat <<EOF
{
  "id": 1,
  "code": "${codes_escaped}",
  "language": "cpp"
}
EOF
)

# Step 4: Send the request using curl
curl -X POST http://127.0.0.1:5000/api/submit \
-H "Content-Type: application/json" \
-H "access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczOTQyOTAwM30.T5UkKB9SFG03TSicAqHT1hs9e6H09uZ6nAu6zujdePI" \
-d '{"id": 1,
  "code": "#include <iostream>\nusing namespace std;\n\nint main(int argc, char const *argv[])\n{\n    int c, d, n;\n    cin >> c >> d >> n;\n    int sums = 0;\n    for (int i = 1; i <= n; i++)\n    {\n        sums += (c * i + d);\n    }\n    cout << sums;\n    return 0;\n}\n",
  "language": "cpp"}'