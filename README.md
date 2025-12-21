# 🐦 AI Tweet Generator (Markov Chain)

A lightweight, interactive web application that generates "fake" tweets based on specific topics (Tech, Business, Physics, etc.) using a **Markov Chain** algorithm. This project demonstrates how probability and data structures can be used to simulate human language without using heavy Large Language Models (LLMs).

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Lightweight-orange)

## ✨ Features

* **Multi-Topic Support:** Generates content for 6 distinct categories:
    * 💻 Tech
    * 💼 Business
    * 🧠 Philosophy
    * ⚛️ Physics
    * 🌌 Astronomy
    * 🌍 Geopolitics
* **Markov Chain Logic:** Uses a dictionary-based probability chain to construct sentences word-by-word.
* **Glassmorphism UI:** A modern, frosted-glass interface with animated backgrounds and smooth transitions.
* **Instant Generation:** Uses Asynchronous JavaScript (Fetch API) to generate new tweets without reloading the page.
* **Optimized Performance:** Pre-loads all topic models at startup for O(1) generation speed.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3 (Flexbox, CSS Variables, Glassmorphism), JavaScript
* **Algorithm:** Markov Chain (Probability-based text generation)

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/techmanvd/Tweet-Generator-using-ML.git](https://github.com/techmanvd/Tweet-Generator-using-ML.git)
cd Tweet-Generator-using-ML