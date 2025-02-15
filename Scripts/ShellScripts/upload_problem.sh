curl -X POST http://127.0.0.1:5000/api/add_problem \
    -F "file=@problems.zip" \
    -F "json={\"problem_char_id\": \"aPlusB\"}" \
    -H "access-token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRpbSIsImV4cCI6MTczOTc2MDI1N30.v80ldP_S6VdXUv1ghSerUMOfvP4pC-OJELmJ5BPENPw""