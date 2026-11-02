# Secure CI Pipeline

A small Flask API with automated security tests and a Jenkins CI pipeline
that runs everything in Docker on every change, and blocks code with
SQL injection vulnerabilities.

## What it does

`GET /users/<username>` looks up a user in a SQLite database and returns
their info as JSON.

| Request | Response |
| --- | --- |
| Existing user | 200 + user data |
| Unknown user | 404 |
| Invalid characters | 400 |

## How the pipeline works

    git push → GitHub → Jenkins → docker build → docker run (pytest) → ✅ / ❌

1. Code is pushed to GitHub.
2. Jenkins (running on an Ubuntu VM) pulls the latest commit.
3. **Build:** builds a Docker image from the Dockerfile.
4. **Test:** runs the pytest suite inside a fresh container.
5. If any test fails, pytest exits non-zero and the build fails.

## Security: defense in depth

- **Input validation (allowlist):** usernames may only contain letters,
  numbers, and underscores. Everything else gets a 400 before the
  database is touched.
- **Parameterized queries:** user input is passed to the database as
  data, never as part of the SQL command.

## Tests

7 pytest tests, including 4 real SQL injection payloads:

- `' OR 1=1 --`
- `john_doe' --`
- `x' UNION SELECT id, username, email FROM users --`
- `admin'; DROP TABLE users; --`

Each injection test checks that the request is rejected **and** that no
user data appears in the response.

## Demo: the pipeline catching a vulnerability

I intentionally replaced the parameterized query with string formatting
and removed input validation. The pipeline caught it:

![Build 5 failed: 5 SQL injection tests caught the vulnerability](docs/images/build-5-red-sqli-caught.png)

After reverting the vulnerable commit, the build passed again:

![Build 6 passed after the fix](docs/images/build-6-green-fixed.png)

## Tech stack

Python, Flask, SQLite, pytest, Docker, Jenkins, Git/GitHub, Ubuntu (VMware)

## Run it locally

    python -m venv venv
    venv\Scripts\activate        # Windows
    pip install -r requirements.txt
    pytest -v                    # run the tests
    python app/main.py           # start the API on http://127.0.0.1:5000

Or with Docker:

    docker build -t secure-ci-pipeline .
    docker run --rm secure-ci-pipeline

## What I learned

See [NOTES.md](NOTES.md) for the bugs I hit and how I fixed them.

## Next steps

- Add a Bandit security scan stage to the pipeline
- Trigger builds automatically on push (webhooks)
- Build an intentionally vulnerable app (XSS, IDOR) with fixes and tests