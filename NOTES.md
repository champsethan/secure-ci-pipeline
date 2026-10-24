# Notes

## Flask app
- What the app does: A small web API. When you visit /user/<name>, it looks that user up in an SQLite database and returns their info as JSON. Unknown users get a 404, and invalid names get a 400.

- Why the SQL uses `?` (parameterized query): Prevents basic SQL injection like a user typing in '` OR 1=1 --'. The database will search for the exact text as a name instead of running it as code.

- Why I validate usernames with an allowlist regex: Before touching the database I only allow letters, numbers, and underscores. Anything else is rejected right away. An allowlist is safer than a blocklist because attackers can find characters you didn't think to block. Together with the '?' makes two layers of defense.

## Bugs I hit
- Files ended up in app/app/ (nested folder). Fixed with Move-Item / Remove-Item.
- An `if` indented 3 spaces swallowed the rest of the function, so valid users returned None (500 error). In Python, indentation defines blocks.
- PowerShell's `>` saved requirements.txt as UTF-16, which Git treated as binary. Fixed with Out-File -Encoding ascii.
- Pytest.ini was empty because it wasn’t saved, so pytest couldn’t find the app module. python -m pytest worked because it adds the current folder to Python’s search path.