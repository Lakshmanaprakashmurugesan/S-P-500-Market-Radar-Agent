# 📡 S&P 500 Market Radar Agent

 **An autonomous market intelligence agent that wakes up on a schedule, analyzes the S&P 500, identifies market signals, and generates daily intelligence without requiring a human to manually press Run.**

![AWS](https://img.shields.io/badge/AWS-Cloud%20Native-orange?style=for-the-badge\&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Amazon EventBridge](https://img.shields.io/badge/Amazon-EventBridge-red?style=for-the-badge)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?style=for-the-badge)
![Amazon SES](https://img.shields.io/badge/Amazon-SES-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Autonomous%20Market%20Radar-success?style=for-the-badge)

---

## 🚀 Overview

The **S&P 500 Market Radar Agent** is an autonomous market intelligence system designed to continuously monitor the S&P 500 and transform raw market data into structured market intelligence.

Instead of requiring a user to open a notebook and manually execute a Python program:

```text
Human → Open Notebook → Press Run → Wait for Analysis
```

the agent is designed around an autonomous workflow:

```text
⏰ Schedule
    ↓
🤖 AWS Lambda Orchestrator
    ↓
📡 Market Data Retrieval
    ↓
📊 S&P 500 Analysis
    ↓
🚩 Market Signal Detection
    ↓
📄 Intelligence Report
```

 **The system is designed to wake up, perform useful market intelligence work, and prepare the result for the user.**

---

## 🧠 What the Agent Does

The Market Radar analyzes the S&P 500 across:

* 📈 Daily price momentum
* 📉 Significant daily price declines
* 🚩 Risk-review candidates
* 📊 Top daily gainers
* 📉 Top daily decliners
* 🧠 Executive market snapshot
* 📄 Automated daily market intelligence report


---

## 🏗️ Autonomous Architecture

```text
Amazon EventBridge
        ↓
AWS Lambda Orchestrator
        ↓
Market Radar Agent
        ↓
Yahoo Finance Market Data
        ↓
S&P 500 Analysis Engine
        ↓
Market Signal Detection
        ↓
CSV + Premium HTML Report
```

The key design principle is **autonomous execution**.

The system does not depend on a human manually pressing **Run** for every analysis cycle.

---

## ⏰ Report Timing & Data Availability

The **S&P 500 Market Radar Agent** is scheduled to run automatically every day at **7:00 AM** using **Amazon EventBridge** to trigger an AWS Lambda function.

### Reporting Methodology

- ⏰ **Execution Time:** 7:00 AM (scheduled via Amazon EventBridge)
- 📊 **Market Data:** Analyzes the **most recently completed U.S. trading session**
- 📄 **Report Generation:** Produces a Daily Market Intelligence Report
- 📧 **Delivery:** Automatically sends the report through Amazon SES
- 🤖 **Operation:** Fully autonomous after deployment with no manual execution required.

  **Note:** The report is generated automatically at **7:00 AM** (via Amazon EventBridge) before the U.S. stock market opens. Therefore, it analyzes data from the **most recently completed U.S. trading session**, rather than intraday market activity.

 The attached **Email Output.pdf** contains a Daily Market Intelligence Report generated automatically on **July 17, 2026, at 7:00 AM**, using market data from the **July 16, 2026 U.S. trading session**.During the analysis window, 24 companies triggered the risk threshold criteria, and the report highlights the top 10 highest-priority signals for focused review.

---

## 📂 Repository Structure

```text
S&P500 MARKET RADAR AGENT/
├── market_radar_agent/
│   └── Core autonomous market intelligence engine.py
├── market_radar_output_screenshot/
│   ├── Amazon EventBridge Active Cron Schedule Screenshot.png
│   ├── Amazon SES Verified Identity Screenshot.png
│   ├── Email Output.pdf
│   ├── Email Snapshot 1 – Daily Market Report.png
│   ├── Email Snapshot 2 – Daily Market Report.png
│   ├── Email Snapshot 3 – Daily Market Report.png
│   └── Email Snapshot 4 – Daily Market Report.png
├── market_radar_output_video/
│   └── Email Output Recording.mp4
└── readme.md
```

---

## 🎬 Demo Video

YouTube Demo: [S&P 500 Market Radar Agent Output Demo](https://youtu.be/Pp42sfW6mNQ)

The video showcases the autonomous market intelligence report generation and Gmail delivery output.

---

## 📊 Market Intelligence Workflow

```text
Market Data
     ↓
S&P 500 Universe
     ↓
Market Capitalization Analysis
     ↓
Daily Gainer / Decliner Analysis
     ↓
Fundamental Screening
     ↓
Value Opportunity Radar
     ↓
Value Trap Risk Screening
     ↓
Market Intelligence Report
```

---

## 🚩 Value Opportunity Radar

The agent identifies companies showing a combination of:

```text
Price Weakness
      +
Revenue Growth
      +
Earnings Growth
      +
Free Cash Flow
      +
Valuation Signals
```

These companies are flagged for **additional value-oriented review**.

 ⚠️ A radar signal is a screening signal, not an investment recommendation.

---

## 📁 Generated Outputs

The agent automatically generates and delivers a structured **Daily Market Intelligence Report** through Amazon SES after each scheduled execution.


The report includes:

* **Executive Market Snapshot** — Overall daily market intelligence summary across the S&P 500.
* **Strongest Gainer** — The company with the largest positive 1-day price movement.
* **Largest Decliner** — The company with the largest negative 1-day price movement.
* **Risk Radar** — Sharp-decline companies flagged for additional research.
* **Top Daily Gainers** — Ranked daily market gainers with ticker, company name, and 1-day percentage change.
* **Top Daily Decliners** — Ranked daily market decliners with ticker, company name, and 1-day percentage change.
* **Value Review Radar** — Companies identified for additional research based on significant daily downside movement.
* **Agent Conclusion** — An autonomous summary of the day's most significant market movements and screening signals.
* **Research Disclaimer** — Clearly distinguishes market screening signals from investment recommendations.


---

## ⚙️ Technology Stack

* **Python** — Market intelligence engine
* **Pandas** — Data processing and analysis
* **Yahoo Finance** — Market data retrieval
* **Amazon EventBridge** — Scheduled execution
* **AWS Lambda** — Agent orchestration
* **HTML / CSS** — Premium report generation

---

## 🌟 Why This Project Matters

Most market scripts wait for a human to start them.

The **S&P 500 Market Radar Agent** is designed around a different model:

 **The agent wakes up. The agent analyzes. The agent prepares the intelligence.**

This project demonstrates the core concept of an **always-on autonomous agent** applied to market intelligence.

---

## 🛡️ Disclaimer

This project is an automated market screening and intelligence system.

The generated signals are for **research and screening purposes only** and do not constitute financial, investment, or trading advice.

---

## 🤖 S&P 500 MARKET RADAR AGENT

### **AUTONOMOUS MARKET INTELLIGENCE.**

### **BUILT TO WATCH THE MARKET WHILE YOU ARE AWAY.**
