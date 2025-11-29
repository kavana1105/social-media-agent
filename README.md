# 📣 Social Media Agent

An AI-powered social media content planning and generation tool built with Streamlit and OpenAI GPT-4.

## 🚀 Features

- **30-Day Content Plan Generator** - Create a complete month of content ideas
- **AI Caption Writer** - Generate platform-optimized captions with real-time analysis
- **Content Repurposer** - Adapt content across Instagram, LinkedIn, and Twitter
- **Performance Predictor** - Estimate engagement before posting
- **Real-time AI Analysis** - Get instant feedback on engagement potential
- **Advanced Options**:
  - Content style presets (Viral, Professional, Storytelling, etc.)
  - Best posting times optimizer
  - A/B testing variants generator
  - Sentiment analysis
  - Competitor insights
  - Multi-language support
  - Smart hashtag generator
  - Content calendar view

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/social-media-agent.git
cd social-media-agent
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🛠️ Tech Stack

- **Streamlit** - Web interface
- **LangChain** - LLM orchestration
- **OpenAI GPT-4** - Content generation
- **Pandas** - Data handling
- **Python 3.8+**

## 📝 How to Use

1. **Configure Settings** - Choose your AI model and creativity level in the sidebar
2. **Generate 30-Day Plan** - Fill in your brand details and click "Generate 30-Day Plan"
3. **Write Captions** - Use the caption writer with real-time AI feedback
4. **Repurpose Content** - Adapt existing content for different platforms
5. **Predict Performance** - Estimate how your content will perform before posting

## 🔒 Environment Variables

Create a `.env` file with:
- `OPENAI_API_KEY` - Your OpenAI API key

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 👤 Author

Built with ❤️ using AI assistance
