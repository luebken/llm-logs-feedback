demo

cat tests/test_llm_logs_feedback.py | llm "are there any major issues with the test?"
pbaste | llm "what does this function do?"


# investigate the database
```sh
sqlite3 /Users/mdl/Library/Application\ Support/io.datasette.llm/logs.db
.mode table
SELECT f.feedback, f.comment, SUBSTR(r.prompt, 1, 50), SUBSTR(r.response, 1, 50) FROM feedback f JOIN responses r ON f.response_id = r.id;
```

# pipe it back to the LLM
```sh
sqlite3 /Users/mdl/Library/Application\ Support/io.datasette.llm/logs.db "SELECT f.feedback, f.comment, r.prompt, r.response FROM feedback f JOIN responses r ON f.response_id = r.id;" | llm "what are some key themes on these responses. keep it brief."
```


