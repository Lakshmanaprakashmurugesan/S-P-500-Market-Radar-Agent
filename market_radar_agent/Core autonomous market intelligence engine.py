import json
import re
import html
import urllib.request
import boto3

from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# 📡 S&P 500 MARKET RADAR AGENT
# AWS LAMBDA
# NO PACKAGE INSTALLATION
# ============================================================


USER_AGENT = "Mozilla/5.0"

SES_REGION = "us-east-1"

EMAIL_ADDRESS = "lakshkrishmurug@gmail.com"

LOCAL_TIMEZONE = "America/Denver"


# ============================================================
# 🌐 HTTP GET
# ============================================================


def http_get(url):

    request = urllib.request.Request(

        url,

        headers={

            "User-Agent": USER_AGENT,

            "Accept": "application/json,text/html"

        }

    )

    with urllib.request.urlopen(

        request,

        timeout=30

    ) as response:

        return response.read().decode(

            "utf-8",

            errors="ignore"

        )


# ============================================================
# 🕒 LOCAL DATE
# ============================================================


def get_local_report_date():

    return datetime.now(

        ZoneInfo(LOCAL_TIMEZONE)

    ).strftime(

        "%B %d, %Y"

    ).upper()


# ============================================================
# 📊 SAFE FORMATTERS
# ============================================================


def format_price(value):

    if value is None:

        return "N/A"

    try:

        return f"${float(value):,.2f}"

    except Exception:

        return "N/A"


def format_percent(value):

    if value is None:

        return "N/A"

    try:

        return f"{float(value):+.2f}%"

    except Exception:

        return "N/A"


# ============================================================
# 🌐 LOAD S&P 500 UNIVERSE
# ============================================================


def load_sp500():

    print("🌐 LOADING S&P 500 UNIVERSE")

    url = (

        "https://en.wikipedia.org/wiki/"

        "List_of_S%26P_500_companies"

    )

    page = http_get(url)

    tables = re.findall(

        r"<table[^>]*>.*?</table>",

        page,

        re.S | re.I

    )

    for table in tables:

        if "Symbol" not in table:

            continue

        if "Security" not in table:

            continue

        rows = re.findall(

            r"<tr[^>]*>(.*?)</tr>",

            table,

            re.S | re.I

        )

        stocks = []

        for row in rows:

            cells = re.findall(

                r"<td[^>]*>(.*?)</td>",

                row,

                re.S | re.I

            )

            if len(cells) < 2:

                continue

            ticker = re.sub(

                r"<.*?>",

                "",

                cells[0]

            )

            company = re.sub(

                r"<.*?>",

                "",

                cells[1]

            )

            ticker = html.unescape(

                ticker

            ).strip().upper()

            company = html.unescape(

                company

            ).strip()

            ticker = ticker.replace(

                ".",

                "-"

            )

            if ticker and company:

                stocks.append({

                    "Ticker": ticker,

                    "Company": company

                })

        if stocks:

            print(

                f"✅ LOADED {len(stocks)} COMPANIES"

            )

            return stocks

    raise RuntimeError(

        "S&P 500 universe could not be loaded"

    )


# ============================================================
# 📈 GET LAST COMPLETED DAILY MARKET DATA
# ============================================================


def get_market_data(ticker, company):

    url = (

        "https://query1.finance.yahoo.com/"

        "v8/finance/chart/"

        + ticker

        + "?range=10d&interval=1d"

    )

    try:

        response = http_get(url)

        data = json.loads(response)

        result = (

            data

            .get("chart", {})

            .get("result", [])

        )

        if not result:

            return None

        chart = result[0]

        timestamps = chart.get(

            "timestamp",

            []

        )

        quote = (

            chart

            .get("indicators", {})

            .get("quote", [])

        )

        if not quote:

            return None

        closes = quote[0].get(

            "close",

            []

        )

        daily_closes = []

        for timestamp, close in zip(

            timestamps,

            closes

        ):

            if close is None:

                continue

            try:

                daily_closes.append({

                    "timestamp": timestamp,

                    "close": float(close)

                })

            except Exception:

                continue

        if len(daily_closes) < 2:

            return None

        latest = daily_closes[-1]

        previous = daily_closes[-2]

        latest_close = latest["close"]

        previous_close = previous["close"]

        if previous_close == 0:

            return None

        change_percent = (

            (

                latest_close

                - previous_close

            )

            / previous_close

        ) * 100

        return {

            "Ticker": ticker,

            "Company": company,

            "Price": latest_close,

            "Previous Close": previous_close,

            "1D Change %": change_percent

        }

    except Exception as error:

        print(

            f"⚠️ {ticker} FAILED: {error}"

        )

        return None


# ============================================================
# 🧠 MARKET RADAR ENGINE
# ============================================================


def run_market_radar():

    print("")

    print(

        "🚀 MARKET RADAR AGENT AWAKENED"

    )

    print("")

    sp500 = load_sp500()

    market_data = []

    for index, stock in enumerate(sp500):

        result = get_market_data(

            stock["Ticker"],

            stock["Company"]

        )

        if result:

            market_data.append(result)

        if (

            (index + 1) % 25 == 0

            or index + 1 == len(sp500)

        ):

            print(

                f"📊 PROCESSED "

                f"{index + 1}/"

                f"{len(sp500)}"

            )

    if not market_data:

        raise RuntimeError(

            "Yahoo Finance returned no market data"

        )

    print("")

    print(

        f"✅ MARKET DATA LOADED: "

        f"{len(market_data)} COMPANIES"

    )

    print("")

    # ========================================================
    # 📈 GAINERS
    # ========================================================

    gainers = sorted(

        market_data,

        key=lambda stock:

        stock.get(

            "1D Change %"

        ) if stock.get(

            "1D Change %"

        ) is not None else -999999,

        reverse=True

    )

    # ========================================================
    # 📉 DECLINERS
    # ========================================================

    decliners = sorted(

        market_data,

        key=lambda stock:

        stock.get(

            "1D Change %"

        ) if stock.get(

            "1D Change %"

        ) is not None else 999999

    )

    strongest_gainer = (

        gainers[0]

        if gainers

        else None

    )

    largest_decliner = (

        decliners[0]

        if decliners

        else None

    )

    # ========================================================
    # ⚠️ VALUE REVIEW RADAR
    # ========================================================

    value_trap_risk = [

        stock

        for stock in market_data

        if (

            stock.get("1D Change %") is not None

            and stock.get("1D Change %") <= -5

        )

    ]

    value_trap_risk = sorted(

        value_trap_risk,

        key=lambda stock:

        stock.get(

            "1D Change %"

        )

    )

    # ========================================================
    # 🧠 AGENT CONCLUSION
    # ========================================================

    conclusion = (

        "The Market Radar Agent analyzed "

        f"{len(market_data)} S&P 500 companies. "

    )

    if strongest_gainer:

        gainer_change = format_percent(

            strongest_gainer["1D Change %"]

        )

        conclusion += (

            f"{strongest_gainer['Ticker']} led the "

            "daily gainers with a "

            f"{gainer_change} move. "

        )

    if largest_decliner:

        decliner_change = format_percent(

            largest_decliner["1D Change %"]

        )

        conclusion += (

            f"{largest_decliner['Ticker']} recorded the "

            "largest daily decline at "

            f"{decliner_change}. "

        )

    if value_trap_risk:

        conclusion += (

            f"{len(value_trap_risk)} companies experienced "

            "sharp daily declines and have been flagged "

            "for additional research."

        )

    else:

        conclusion += (

            "No immediate sharp-decline risk signals "

            "were identified."

        )

    report = {

        "agent": "S&P 500 Market Radar",

        "report_date": get_local_report_date(),

        "companies_analyzed": len(market_data),

        "strongest_daily_gainer": (

            strongest_gainer

        ),

        "largest_daily_decliner": (

            largest_decliner

        ),

        "top_daily_gainers": gainers[:10],

        "top_daily_decliners": decliners[:10],

        "value_trap_risk": value_trap_risk[:10],

        "agent_conclusion": conclusion

    }

    print("")

    print(

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    )

    print(

        "📡 S&P 500 MARKET RADAR"

    )

    print(

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    )

    print("")

    print(

        f"📅 REPORT DATE: "

        f"{report['report_date']}"

    )

    print(

        f"🏢 COMPANIES ANALYZED: "

        f"{len(market_data)}"

    )

    if strongest_gainer:

        gainer_change = format_percent(

            strongest_gainer["1D Change %"]

        )

        print(

            f"📈 STRONGEST GAINER: "

            f"{strongest_gainer['Ticker']} "

            f"{gainer_change}"

        )

    if largest_decliner:

        decliner_change = format_percent(

            largest_decliner["1D Change %"]

        )

        print(

            f"📉 LARGEST DECLINER: "

            f"{largest_decliner['Ticker']} "

            f"{decliner_change}"

        )

    print("")

    print(

        "🤖 MARKET RADAR AGENT COMPLETE"

    )

    return report


# ============================================================
# 📧 PREMIUM HTML MARKET EMAIL
# ============================================================


def send_market_email(report):

    print(

        "📧 SENDING PREMIUM MARKET RADAR EMAIL"

    )

    ses = boto3.client(

        "ses",

        region_name=SES_REGION

    )

    gainer = report.get(

        "strongest_daily_gainer"

    )

    decliner = report.get(

        "largest_daily_decliner"

    )

    gainers = report.get(

        "top_daily_gainers",

        []

    )

    decliners = report.get(

        "top_daily_decliners",

        []

    )

    value_traps = report.get(

        "value_trap_risk",

        []

    )

    companies_analyzed = report.get(

        "companies_analyzed",

        0

    )

    report_date = report.get(

        "report_date",

        "N/A"

    )

    conclusion = report.get(

        "agent_conclusion",

        "No conclusion available."

    )

    def esc(value):

        return html.escape(

            str(value)

        )

    def stock_table_row(

        stock,

        rank,

        positive=True

    ):

        ticker = esc(

            stock.get(

                "Ticker",

                "N/A"

            )

        )

        company = esc(

            stock.get(

                "Company",

                "N/A"

            )

        )

        change = format_percent(

            stock.get(

                "1D Change %"

            )

        )

        change_color = (

            "#16a34a"

            if positive

            else "#dc2626"

        )

        return f"""

<tr>

<td style="padding:13px 10px;border-bottom:1px solid #e5e7eb;color:#6b7280;font-weight:700;">

{rank}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #e5e7eb;font-weight:800;color:#111827;">

{ticker}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #e5e7eb;color:#374151;">

{company}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #e5e7eb;text-align:right;font-weight:800;color:{change_color};">

{change}

</td>

</tr>

"""

    gainers_html = ""

    for rank, stock in enumerate(

        gainers[:10],

        1

    ):

        gainers_html += stock_table_row(

            stock,

            rank,

            True

        )

    decliners_html = ""

    for rank, stock in enumerate(

        decliners[:10],

        1

    ):

        decliners_html += stock_table_row(

            stock,

            rank,

            False

        )

    value_html = ""

    for rank, stock in enumerate(

        value_traps[:10],

        1

    ):

        ticker = esc(

            stock.get(

                "Ticker",

                "N/A"

            )

        )

        company = esc(

            stock.get(

                "Company",

                "N/A"

            )

        )

        change = format_percent(

            stock.get(

                "1D Change %"

            )

        )

        value_html += f"""

<tr>

<td style="padding:13px 10px;border-bottom:1px solid #fed7aa;color:#9a3412;font-weight:700;">

{rank}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #fed7aa;font-weight:800;color:#7c2d12;">

{ticker}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #fed7aa;color:#7c2d12;">

{company}

</td>

<td style="padding:13px 10px;border-bottom:1px solid #fed7aa;text-align:right;font-weight:800;color:#dc2626;">

{change}

</td>

</tr>

"""

    if not value_html:

        value_html = """

<tr>

<td colspan="4" style="padding:20px;text-align:center;color:#6b7280;">

No immediate sharp-decline risks identified.

</td>

</tr>

"""

    gainer_ticker = esc(

        gainer.get(

            "Ticker",

            "N/A"

        )

        if gainer

        else "N/A"

    )

    gainer_company = esc(

        gainer.get(

            "Company",

            "N/A"

        )

        if gainer

        else "N/A"

    )

    gainer_price = format_price(

        gainer.get(

            "Price"

        )

        if gainer

        else None

    )

    gainer_change = format_percent(

        gainer.get(

            "1D Change %"

        )

        if gainer

        else None

    )

    decliner_ticker = esc(

        decliner.get(

            "Ticker",

            "N/A"

        )

        if decliner

        else "N/A"

    )

    decliner_company = esc(

        decliner.get(

            "Company",

            "N/A"

        )

        if decliner

        else "N/A"

    )

    decliner_price = format_price(

        decliner.get(

            "Price"

        )

        if decliner

        else None

    )

    decliner_change = format_percent(

        decliner.get(

            "1D Change %"

        )

        if decliner

        else None

    )

    html_body = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>S&P 500 Market Radar</title>

</head>

<body style="margin:0;padding:0;background:#f3f4f6;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f6;">

<tr>

<td align="center" style="padding:30px 12px;">

<table width="680" cellpadding="0" cellspacing="0" style="max-width:680px;width:100%;background:#ffffff;border-radius:18px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">

<tr>

<td style="background:#111827;padding:36px 32px;color:#ffffff;">

<div style="font-size:12px;letter-spacing:2px;color:#9ca3af;font-weight:700;">

AUTONOMOUS MARKET INTELLIGENCE

</div>

<div style="font-size:30px;font-weight:800;margin-top:12px;">

📡 S&P 500 MARKET RADAR

</div>

<div style="font-size:14px;color:#d1d5db;margin-top:10px;">

DAILY MARKET INTELLIGENCE REPORT

</div>

<div style="margin-top:24px;font-size:13px;color:#9ca3af;">

📅 {esc(report_date)}

&nbsp;&nbsp; • &nbsp;&nbsp;

🌐 S&P 500

&nbsp;&nbsp; • &nbsp;&nbsp;

🏢 {companies_analyzed} COMPANIES

</div>

</td>

</tr>

<tr>

<td style="padding:30px 32px 10px;">

<div style="font-size:12px;letter-spacing:1.5px;font-weight:800;color:#6b7280;">

EXECUTIVE MARKET SNAPSHOT

</div>

<div style="font-size:22px;font-weight:800;color:#111827;margin-top:8px;">

Today's Market Radar

</div>

<p style="font-size:15px;line-height:1.7;color:#4b5563;">

The autonomous Market Radar Agent analyzed

<b>{companies_analyzed}</b> S&P 500 companies

and identified daily momentum leaders,

downside movement, and potential risk-review

candidates.

</p>

</td>

</tr>

<tr>

<td style="padding:10px 32px 30px;">

<table width="100%" cellpadding="0" cellspacing="0">

<tr>

<td width="32%" valign="top" style="background:#ecfdf5;border-radius:14px;padding:20px;">

<div style="color:#15803d;font-size:12px;font-weight:800;">

📈 STRONGEST GAINER

</div>

<div style="font-size:24px;font-weight:800;color:#166534;margin-top:12px;">

{gainer_ticker}

</div>

<div style="font-size:13px;color:#166534;margin-top:4px;">

{gainer_company}

</div>

<div style="font-size:20px;font-weight:800;color:#16a34a;margin-top:16px;">

{gainer_change}

</div>

<div style="font-size:12px;color:#15803d;margin-top:5px;">

Price {gainer_price}

</div>

</td>

<td width="2%"></td>

<td width="32%" valign="top" style="background:#fef2f2;border-radius:14px;padding:20px;">

<div style="color:#b91c1c;font-size:12px;font-weight:800;">

📉 LARGEST DECLINER

</div>

<div style="font-size:24px;font-weight:800;color:#991b1b;margin-top:12px;">

{decliner_ticker}

</div>

<div style="font-size:13px;color:#991b1b;margin-top:4px;">

{decliner_company}

</div>

<div style="font-size:20px;font-weight:800;color:#dc2626;margin-top:16px;">

{decliner_change}

</div>

<div style="font-size:12px;color:#b91c1c;margin-top:5px;">

Price {decliner_price}

</div>

</td>

<td width="2%"></td>

<td width="32%" valign="top" style="background:#fff7ed;border-radius:14px;padding:20px;">

<div style="color:#c2410c;font-size:12px;font-weight:800;">

⚠️ RISK RADAR

</div>

<div style="font-size:24px;font-weight:800;color:#9a3412;margin-top:12px;">

{len(value_traps)}

</div>

<div style="font-size:13px;color:#9a3412;margin-top:4px;">

Sharp-decline names

</div>

<div style="font-size:13px;color:#c2410c;margin-top:16px;">

Require additional research

</div>

</td>

</tr>

</table>

</td>

</tr>

<tr>

<td style="padding:0 32px 30px;">

<div style="background:#f9fafb;border-radius:14px;padding:22px;">

<div style="font-size:17px;font-weight:800;color:#111827;margin-bottom:16px;">

📈 TOP DAILY GAINERS

</div>

<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">

<tr style="background:#f3f4f6;color:#6b7280;font-weight:800;">

<td style="padding:10px;">#</td>

<td style="padding:10px;">TICKER</td>

<td style="padding:10px;">COMPANY</td>

<td style="padding:10px;text-align:right;">1D CHANGE</td>

</tr>

{gainers_html}

</table>

</div>

</td>

</tr>

<tr>

<td style="padding:0 32px 30px;">

<div style="background:#f9fafb;border-radius:14px;padding:22px;">

<div style="font-size:17px;font-weight:800;color:#111827;margin-bottom:16px;">

📉 TOP DAILY DECLINERS

</div>

<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">

<tr style="background:#f3f4f6;color:#6b7280;font-weight:800;">

<td style="padding:10px;">#</td>

<td style="padding:10px;">TICKER</td>

<td style="padding:10px;">COMPANY</td>

<td style="padding:10px;text-align:right;">1D CHANGE</td>

</tr>

{decliners_html}

</table>

</div>

</td>

</tr>

<tr>

<td style="padding:0 32px 30px;">

<div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:14px;padding:22px;">

<div style="font-size:17px;font-weight:800;color:#9a3412;margin-bottom:8px;">

🚩 VALUE REVIEW RADAR

</div>

<div style="font-size:13px;color:#9a3412;margin-bottom:18px;">

Sharp daily declines have been flagged for additional research.

</div>

<table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">

<tr style="background:#ffedd5;color:#9a3412;font-weight:800;">

<td style="padding:10px;">#</td>

<td style="padding:10px;">TICKER</td>

<td style="padding:10px;">COMPANY</td>

<td style="padding:10px;text-align:right;">1D CHANGE</td>

</tr>

{value_html}

</table>

</div>

</td>

</tr>

<tr>

<td style="padding:0 32px 30px;">

<div style="background:#111827;border-radius:14px;padding:26px;color:#ffffff;">

<div style="font-size:12px;letter-spacing:1.5px;color:#9ca3af;font-weight:800;">

🧠 AGENT CONCLUSION

</div>

<div style="font-size:15px;line-height:1.8;margin-top:14px;color:#f9fafb;">

{esc(conclusion)}

</div>

</div>

</td>

</tr>

<tr>

<td style="padding:0 32px 30px;">

<div style="background:#f9fafb;border-radius:12px;padding:18px;font-size:12px;line-height:1.7;color:#6b7280;">

⚠️ <b>IMPORTANT:</b>

This Market Radar identifies screening signals

for additional research only.

A risk-review signal is

<b>not an investment recommendation</b>.

Additional analysis is required before making

any investment decision.

</div>

</td>

</tr>

<tr>

<td style="background:#f3f4f6;padding:25px 32px;text-align:center;">

<div style="font-size:14px;font-weight:800;color:#111827;">

🤖 S&P 500 MARKET RADAR AGENT

</div>

<div style="font-size:12px;color:#6b7280;margin-top:6px;">

AUTONOMOUS DAILY MARKET INTELLIGENCE

</div>

<div style="font-size:11px;color:#9ca3af;margin-top:12px;">

AWS Lambda • Amazon SES • Yahoo Finance

</div>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>

"""

    plain_text = f"""

📡 S&P 500 MARKET RADAR

DAILY MARKET INTELLIGENCE REPORT

REPORT DATE: {report_date}

COMPANIES ANALYZED: {companies_analyzed}

STRONGEST DAILY GAINER:

{gainer_ticker} - {gainer_company}

Price: {gainer_price}

Change: {gainer_change}

LARGEST DAILY DECLINER:

{decliner_ticker} - {decliner_company}

Price: {decliner_price}

Change: {decliner_change}

VALUE REVIEW RADAR:

{len(value_traps)} sharp-decline names flagged.

AGENT CONCLUSION:

{conclusion}

IMPORTANT:

This is a screening signal only and not an investment recommendation.

"""

    response = ses.send_email(

        Source=EMAIL_ADDRESS,

        Destination={

            "ToAddresses": [

                EMAIL_ADDRESS

            ]

        },

        Message={

            "Subject": {

                "Data": (

                    "📡 S&P 500 Market Radar | "

                    "Daily Intelligence"

                ),

                "Charset": "UTF-8"

            },

            "Body": {

                "Text": {

                    "Data": plain_text,

                    "Charset": "UTF-8"

                },

                "Html": {

                    "Data": html_body,

                    "Charset": "UTF-8"

                }

            }

        }

    )

    print("")

    print(

        "✅ PREMIUM MARKET RADAR EMAIL SENT"

    )

    print(

        f"📨 SES MESSAGE ID: "

        f"{response['MessageId']}"

    )

    return response["MessageId"]


# ============================================================
# 🚀 AWS LAMBDA HANDLER
# ============================================================


def lambda_handler(event, context):

    print(

        "⏰ EVENTBRIDGE ACTIVATED MARKET RADAR"

    )

    print(

        f"🕒 LOCAL TIMEZONE: "

        f"{LOCAL_TIMEZONE}"

    )

    print(

        f"📅 LOCAL REPORT DATE: "

        f"{get_local_report_date()}"

    )

    try:

        report = run_market_radar()

        message_id = send_market_email(

            report

        )

        print("")

        print(

            "🎉 AUTONOMOUS AGENT RUN COMPLETE"

        )

        return {

            "statusCode": 200,

            "body": json.dumps({

                "status": "SUCCESS",

                "agent": (

                    "S&P 500 Market Radar"

                ),

                "email_sent": True,

                "ses_message_id": message_id,

                "report": report

            }, default=str)

        }

    except Exception as error:

        print(

            f"❌ AGENT FAILED: {error}"

        )

        return {

            "statusCode": 500,

            "body": json.dumps({

                "status": "FAILED",

                "error": str(error)

            })

        }
