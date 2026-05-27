#  DataSense - AI Data Analyst ⚡

A sleek, modern Streamlit application that leverages Google Gemini 3.5 Flash to automatically analyze CSV datasets. Upload your data and let the AI generate Python EDA code and synthesize executive-level statistical insights — in seconds.

---

## Features

| | |
|---|---|
| **Automated EDA Generation** | Instantly writes executable Python code using Pandas, Matplotlib, and Seaborn tailored to your specific dataset. |
| **Executive AI Insights** | Synthesizes raw statistics into a readable analytical brief covering key patterns, data health, correlations, and modeling recommendations. |
| **Modern Dark SaaS UI** | Custom typography (Inter & Fira Code), interactive metric cards, and a premium dark-mode aesthetic. |
| **Privacy-Focused** | Data is processed locally in-memory. API keys are loaded via environment variables and are never logged or stored. |

---

## Tech Stack

- **Framework** — [Streamlit](https://streamlit.io)
- **AI Engine** — [Google Gemini API](https://ai.google.dev/) (`gemini-3.5-flash`)
- **Data Layer** — [Pandas](https://pandas.pydata.org/)
- **Environment** — [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- A free Gemini API key — get one at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install streamlit pandas google-genai python-dotenv
```

> If a `requirements.txt` is present: `pip install -r requirements.txt`

### 4. Configure your API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_actual_api_key_here
```

> **Never commit this file.** It's already in `.gitignore`.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## How to Use

1. **Upload data** — drag and drop a `.csv` file into the sidebar dropzone.
2. **Review metrics** — row count, column count, numeric features, and null columns appear instantly in the metric cards.
3. **Start analysis** — click **"Start Exploration ⚡"**.
4. **View code** — expand the **"View Generated Python Engine"** dropdown to see and copy the exact EDA code Gemini wrote for your dataset.
5. **Read insights** — the **"Exploratory Insights"** section below summarizes data health, patterns, correlations, and modeling recommendations.

---

## Project Structure

```
ai-data-analyst/
├── app.py              # Main Streamlit application
├── .env                # API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Contributing

Contributions, bug reports, and feature requests are welcome. Check the [issues page](https://github.com/yourusername/ai-data-analyst/issues) to get started.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).
