# 📡 S&P 500 Market Radar Agent

> **An autonomous market intelligence agent that wakes up on a schedule, analyzes the S&P 500, identifies market signals, and generates daily intelligence without requiring a human to manually press Run.**

![AWS](https://img.shields.io/badge/AWS-Cloud%20Native-orange?style=for-the-badge\&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Amazon EventBridge](https://img.shields.io/badge/Amazon-EventBridge-red?style=for-the-badge)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?style=for-the-badge)
![Amazon S3](https://img.shields.io/badge/Amazon-S3-blue?style=for-the-badge)
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

> **The system is designed to wake up, perform useful market intelligence work, and prepare the result for the user.**

---

## 🧠 What the Agent Does

The Market Radar analyzes the S&P 500 across:

* 📈 Daily price momentum
* 📉 Significant daily declines
* 🏆 Market capitalization
* 💰 P/E valuation
* 📊 Revenue growth
* 📈 Earnings growth
* 💵 Free cash flow

The agent generates market intelligence views including:

* **Top 50 companies by market capitalization**
* **Top 50 daily gainers**
* **Top 50 daily decliners**
* **Possible value-review candidates**
* **Value-trap risk screening**

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

## 📂 Repository Structure

```text
sp500-market-radar/
│
├── market_radar_agent.py
│   └── Core autonomous market intelligence engine
│
├── market_radar_output.png
│   └── Example generated market radar output
│
└── README.md
    └── Project documentation
```

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

> ⚠️ A radar signal is a screening signal, not an investment recommendation.

---

## 📁 Generated Outputs

The agent generates structured market intelligence files:

```text
sp500_all_stocks.csv
top_50_market_cap.csv
top_50_daily_gainers.csv
bottom_50_daily_losers.csv
value_opportunities.csv
value_trap_risk.csv
sp500_market_radar_premium.html
```

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

> **The agent wakes up. The agent analyzes. The agent prepares the intelligence.**

This project demonstrates the core concept of an **always-on autonomous agent** applied to market intelligence.

---

## 🛡️ Disclaimer

This project is an automated market screening and intelligence system.

The generated signals are for **research and screening purposes only** and do not constitute financial, investment, or trading advice.

---

## 🤖 S&P 500 MARKET RADAR AGENT

### **AUTONOMOUS MARKET INTELLIGENCE.**

### **BUILT TO WATCH THE MARKET WHILE YOU ARE AWAY.**
