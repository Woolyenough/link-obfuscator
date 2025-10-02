# Link Obfuscator

A simple link shortening/obfuscator web app written in Python 3.12 using Flask. I have this deployed under a subdomain of my domain `link.wooly.wtf`, running behind an Apache HTTP server with a reverse proxy setup.

It features:
- Basic username/password authentication
- MariaDB/MySQL compatibility for persistent storage
- Support for custom URL code generation modes (e.g., `xd` and `lol` - i'm *very* creative, clearly) which is easily extensible

## Running an Instance
You will need:
- A MariaDB/MySQL server
- Python 3.12.x

To configure, copy `.env.TEMPLATE` into `.env`, and modify the values inside it.

Then, run with Python (on Linux, using Bash):
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py  # to setup database
python app.py

# Or, for production deployment:
gunicorn --bind 0.0.0.0:5000 app:app
```
By default, the app runs on port 5000.
<details>
<summary>Want to add it to an Apache HTTP server?</summary>
You can use Apache's ProxyPass to internally relay traffic to it. Here's an example of something close to what I am using:

```
<VirtualHost *:443>
    ServerName link.wooly.wtf

    ProxyPreserveHost On
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
</VirtualHost>
```
</details>
<br>
Now it should be good to go!

## why bad ui? grr! 😤
not my strong suit, sorry :c
