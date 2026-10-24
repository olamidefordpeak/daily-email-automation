{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOPJTI067OFQvnl9TGkfMH3",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/olamidefordpeak/daily-email-automation/blob/main/Exchange_rate_Automated_mail.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "0thF9pFQ1C1A"
      },
      "outputs": [],
      "source": [
        " # An automated mail of the daily exchange rate\n",
        "import requests\n",
        "import resend\n",
        "import os\n",
        "from resend.exceptions import ResendError\n",
        "\n",
        "#url for the exchangerate api\n",
        "exchangerate_api_key = os.environ.get(\"exchangerate_api_key\")\n",
        "\n",
        "url = f\"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/latest/\"\n",
        "Base = \"USD\"\n",
        "\n",
        "url_base = f\"{url}{Base}\"\n",
        "response = requests.get(url_base)\n",
        "\n",
        "from datetime import datetime\n",
        "now = datetime.now()\n",
        "\n",
        "try:\n",
        "  response.raise_for_status()\n",
        "  data = response.json()\n",
        "  execution = data['result']\n",
        "  time = now.strftime(\"%Y-%m-%d %H:%M:%S\")\n",
        "  with open(\"execution_log.txt\", \"a\") as f:\n",
        "    f.write(f\"[{time}] [{execution}] Data retrieved successfully.\\n\")\n",
        "\n",
        "except requests.exceptions.Timeout:\n",
        "  with open(\"execution_log.txt\", \"a\") as f:\n",
        "    f.write(\"Request timed out.\\n\")\n",
        "except requests.exceptions.ConnectionError:\n",
        "  with open(\"execution_log.txt\", \"a\") as f:\n",
        "    f.write(\"Failed to connect to server.\\n\")\n",
        "except requests.exceptions.HTTPError as e:\n",
        "  with open(\"execution_log.txt\", \"a\") as f:\n",
        "    f.write(f\"HTTP error: {e}.\\n\")\n",
        "except requests.exceptions.RequestException as e:\n",
        "  with open(\"execution_log.txt\", \"a\") as f:\n",
        "    f.write(f\"Something else went wrong: {e}.\\n\")\n",
        "\n",
        "# A success or failure audit entry text file\n",
        "with open(\"execution_log.txt\", \"r\") as f:\n",
        "  content = f.read()\n",
        "  print(content)\n",
        "\n",
        "usd_eur = data['conversion_rates']['EUR']\n",
        "usd_gbp = data['conversion_rates']['GBP']\n",
        "usd_ngn = data['conversion_rates']['NGN']\n",
        "source = data['documentation']\n",
        "# Automated email sender Api\n",
        "resend.api_key = os.environ.get(\"RESEND_API_KEY\")\n",
        "\n",
        "body = f\"\"\"\n",
        "<h2>Good morning,</h2>\n",
        "<p>Here are today's exchange rates (base: <strong>USD</strong>):</p>\n",
        "<table border=\"1\" cellpadding=\"8\" cellspacing=\"0\">\n",
        "  <tr><th>Currency</th><th>Rate</th></tr>\n",
        "  <tr><td>1 USD → EUR</td><td>{usd_eur:.4f}</td></tr>\n",
        "  <tr><td>1 USD → GBP</td><td>{usd_gbp:.4f}</td></tr>\n",
        "  <tr><td>1 USD → NGN</td><td>{usd_ngn:,.2f}</td></tr>\n",
        "</table>\n",
        "<p><em>Rates as of {time}. Source: {source}.</em></p>\n",
        "<hr>\n",
        "<p><small>This is an automated message. No reply needed.</small></p>\n",
        "\"\"\"\n",
        "\n",
        "params: resend.Emails.SendParams = {\n",
        "    \"from\": \"Acme <onboarding@resend.dev>\",\n",
        "    \"to\": [\"olamidefordpeak@gmail.com\"],\n",
        "    \"subject\": f\"Daily Exchange Rates —{time}\",\n",
        "    \"html\": body,\n",
        "}\n",
        "\n",
        "try:\n",
        "    email = resend.Emails.send(params)\n",
        "    print(email)\n",
        "except ResendError as error:\n",
        "    print(error)\n"
      ]
    }
  ]
}
