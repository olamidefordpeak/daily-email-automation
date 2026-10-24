 # An automated mail of the daily exchange rate
import requests
import resend
import os
from resend.exceptions import ResendError
from datetime import datetime

#url for the exchangerate api
exchangerate_api_key = os.environ.get("EXCHANGERATE_API_KEY")

url = f"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/latest/"
Base = "USD"

url_base = f"{url}{Base}"
response = requests.get(url_base)


now = datetime.now()

try:
  response.raise_for_status()
  data = response.json()
  execution = data['result']
  time = now.strftime("%Y-%m-%d %H:%M:%S")
  with open("execution_log.txt", "a") as f:
    f.write(f"[{time}] [{execution}] Data retrieved successfully.\n")

except requests.exceptions.Timeout:
  with open("execution_log.txt", "a") as f:
    f.write("Request timed out.\n")
except requests.exceptions.ConnectionError:
  with open("execution_log.txt", "a") as f:
    f.write("Failed to connect to server.\n")
except requests.exceptions.HTTPError as e:
  with open("execution_log.txt", "a") as f:
    f.write(f"HTTP error: {e}.\n")
except requests.exceptions.RequestException as e:
  with open("execution_log.txt", "a") as f:
    f.write(f"Something else went wrong: {e}.\n")

# A success or failure audit entry text file
with open("execution_log.txt", "r") as f:
  content = f.read()
  print(content)

usd_eur = data['conversion_rates']['EUR']
usd_gbp = data['conversion_rates']['GBP']
usd_ngn = data['conversion_rates']['NGN']
source = data['documentation']
# Automated email sender Api
resend.api_key = os.environ.get("RESEND_API_KEY")

body = f"""
<h2>Good morning,</h2>
<p>Here are today's exchange rates (base: <strong>USD</strong>):</p>
<table border="1" cellpadding="8" cellspacing="0">
  <tr><th>Currency</th><th>Rate</th></tr>
  <tr><td>1 USD → EUR</td><td>{usd_eur:.4f}</td></tr>
  <tr><td>1 USD → GBP</td><td>{usd_gbp:.4f}</td></tr>
  <tr><td>1 USD → NGN</td><td>{usd_ngn:,.2f}</td></tr>
</table>
<p><em>Rates as of {time}. Source: {source}.</em></p>
<hr>
<p><small>This is an automated message. No reply needed.</small></p>
"""

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["olamidefordpeak@gmail.com"],
    "subject": f"Daily Exchange Rates —{time}",
    "html": body,
}

try:
    email = resend.Emails.send(params)
    print(email)
except ResendError as error:
    print(error)
