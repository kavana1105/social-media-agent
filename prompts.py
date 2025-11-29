# prompts.py
from textwrap import dedent

SOCIAL_STRATEGY_SYSTEM = dedent("""
You are a social media strategist for small brands in India.
You produce clear, structured, actionable plans tailored to brand voice and audience.
Be concise but specific. Avoid generic fluff. Include hooks, CTAs, and platform best practices.
""")

SOCIAL_STRATEGY_TEMPLATE = dedent("""
Brand: {brand_name}
Niche/Industry: {niche}
Audience: {audience}
Tone/Voice: {tone}
Platforms: {platforms}
Goal: {goal}
Constraints: {constraints}

Task:
Create a 30-day content plan. Keep ideas varied: education, storytelling, behind-the-scenes, social proof, UGC prompts, offers.
Align with Indian audience context where relevant.

IMPORTANT: Return EXACTLY in this format for each post (one post per block, separated by blank line):

---
Post Date: Day 1
Platform: Instagram
Post Type: Carousel
Idea Title: 5 Skills That Will Make You Job-Ready in 2024
Key Points: Focus on in-demand skills, Build portfolio projects, Network actively
CTA: Enroll in our skill-building course today
Hashtags: #CareerGrowth #SkillDevelopment #EdTech #JobReady #India
---

Repeat this exact format for all 30 days. Use "Post Date:", "Platform:", "Post Type:", "Idea Title:", "Key Points:", "CTA:", "Hashtags:" as exact labels.
""")

CAPTION_SYSTEM = dedent("""
You write high-performing social captions with strong hooks, skimmable structure, and clear CTAs.
You tailor style to the specified platform, tone, and audience.
Include 5-10 relevant hashtags when helpful.
""")

CAPTION_TEMPLATE = dedent("""
Platform: {platform}
Tone: {tone}
Audience: {audience}

Post Idea:
Title: {title}
Key Points: {key_points}
CTA: {cta}
Hashtags: {hashtags}

Write a single caption under 180 words with:
- a compelling hook in first line,
- short paragraphs or bullets,
- a clear CTA,
- platform-appropriate emojis sparingly (optional),
- include provided hashtags at the end when appropriate.
Return only the caption text.
""")

REPURPOSE_SYSTEM = dedent("""
You repurpose content across platforms while preserving core message and brand voice.
Optimize for each platform's format and norms without bloating the text.
""")

REPURPOSE_TEMPLATE = dedent("""
Original Caption (Source Platform: {source_platform}):
{original_caption}

Target Platforms: {target_platforms}

Task:
Create optimized versions for each target platform:
- Keep message consistent.
- Adapt length, hooks, hashtags, and CTA for each platform.
- Use list formatting only if it improves readability.

Return in the structure:
[Platform]:
<caption>
""")