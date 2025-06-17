# Data Analyst Agent

A conversational AI agent that performs data analysis, using open‑source models via the Together AI API.

---

## 🚀 Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
````

* **Get your free API key**

  1. Sign up for a free account at [Together AI](https://together.ai).
  2. In your dashboard, go to **Settings → API Keys** and create a new key ([pypi.org][1], [together.ai][2], [api.together.xyz][3]).
  3. Set it as an environment variable:

```bash
export TOGETHER_API_KEY="YOUR_KEY_HERE"
```

---

## 🗂 Project Directory Structure

```text
.
├── agent.py           # Main agent implementation
├── config.py          # Configuration, including model setup
├── data/              # Sample datasets
├── tests/             # Unit and integration tests
└── README.md          # (You are here)
```

---

## ▶️ How to Run the Agent

1. Ensure `TOGETHER_API_KEY` is set.
2. Optionally adjust `config.py` (e.g., change model or behavior).
3. Run:

```bash
python agent.py
```

This starts an interactive session. Ask questions like “analyze data.csv” and the agent will respond using the model.

---

## ✅ How to Test

Tests are in the `tests/` directory. Run:

```bash
pytest
```

This will execute unit and integration tests to validate functionality.

---

## 🧠 Together API Model Usage

By default, the agent uses an open‑source model (e.g., `meta-llama/Llama‑3.1‑8B‑Instruct`) via Together’s OpenAI‑compatible API. You can switch models easily in `config.py`. Sample usage from documentation:

```python
from together import Together
client = Together()

stream = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[{"role": "user", "content": "Analyze sales trends in Q1"}],
  stream=True,
)
```

([docs.together.ai][4])

---

## 🔄 Workflow Summary

1. **Install dependencies**
2. **Obtain and set** `TOGETHER_API_KEY`
3. **Run** the agent with `python agent.py`
4. **Test** via `pytest`
5. (Optional) Modify model selection in `config.py`

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🛠 Contributing

Contributions welcome! Please open GitHub issues or pull requests for bug fixes, improvements, or discussion.

---

Happy analyzing! 😊
