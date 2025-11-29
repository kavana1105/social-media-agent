# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from agent import SocialAgent, PlanItem
from utils import plan_to_dataframe, save_session
from realtime_utils import analyze_caption_realtime, get_trending_hashtags
from advanced_features import (
    get_best_posting_times,
    generate_ab_variants,
    analyze_sentiment,
    get_competitor_insights,
    generate_content_calendar,
    apply_content_style,
    translate_caption,
    generate_smart_hashtags
)

load_dotenv()

st.set_page_config(page_title="Social Media Agent", page_icon="📣", layout="wide")

# Sidebar - Configuration
st.sidebar.header("⚙️ Configuration")
model = st.sidebar.selectbox("Model", options=["gpt-4o-mini"], index=0)
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.7, 0.1)

st.sidebar.divider()
st.sidebar.header("🚀 Advanced Options")

# Content style presets
content_style = st.sidebar.selectbox(
    "Content Style",
    ["Default", "Viral", "Professional", "Storytelling", "Educational", "Humorous"],
    help="Choose a content style preset"
)

# Posting time optimizer
show_best_times = st.sidebar.checkbox("Show Best Posting Times", value=False)

# A/B Testing
enable_ab_testing = st.sidebar.checkbox("Generate A/B Test Variants", value=False)
if enable_ab_testing:
    num_variants = st.sidebar.slider("Number of variants", 2, 5, 2)

# Competitor analysis
enable_competitor = st.sidebar.checkbox("Competitor Insights", value=False)
if enable_competitor:
    competitor_handle = st.sidebar.text_input("Competitor handle", placeholder="@competitor")

# Content calendar
show_calendar = st.sidebar.checkbox("Show Content Calendar View", value=False)

# Auto-hashtag generator
auto_hashtags = st.sidebar.checkbox("AI Hashtag Generator", value=True)

# Sentiment analysis
show_sentiment = st.sidebar.checkbox("Sentiment Analysis", value=False)

# Multi-language support
enable_translation = st.sidebar.checkbox("Multi-language Support", value=False)
if enable_translation:
    target_language = st.sidebar.selectbox("Translate to", ["Spanish", "French", "German", "Hindi", "Arabic"])

# Save as template
save_template = st.sidebar.checkbox("Save as Template", value=False)

st.title("📣 Social Media Agent")
st.caption("Generate a 30-day plan, write captions, and repurpose across platforms.")

# Brand inputs
with st.form("brand_form"):
    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("Brand name", "Rooman Skills")
        niche = st.text_input("Niche/Industry", "EdTech / Skilling")
        audience = st.text_input("Audience", "Students and early-career professionals in India")
    with col2:
        tone = st.text_input("Tone/Voice", "Encouraging, expert, simple")
        platforms = st.multiselect("Platforms", ["Instagram", "LinkedIn", "Twitter"], default=["Instagram","LinkedIn"])
        goal = st.text_input("Primary goal", "Drive awareness and course sign-ups")
    constraints = st.text_area("Constraints (optional)", "Keep captions under 180 words; respect Indian context.")
    submitted = st.form_submit_button("Generate 30-Day Plan")

agent = None
plan_items = []

if submitted:
    try:
        agent = SocialAgent(model=model, temperature=temperature)
        with st.spinner("Creating content plan..."):
            plan_items = agent.create_30_day_plan(
                brand_name=brand_name,
                niche=niche,
                audience=audience,
                tone=tone,
                platforms=platforms,
                goal=goal,
                constraints=constraints,
            )
        if not plan_items:
            st.warning("Plan generated, but parsing was partial. Showing raw text below (use caption writer with manual inputs).")
        else:
            st.success(f"Generated {len(plan_items)} plan items.")
            df = plan_to_dataframe(plan_items)
            st.dataframe(df, use_container_width=True)
            filename = f"{brand_name.replace(' ', '_')}_30_day_plan"
            path = save_session(filename, plan_items)
            st.info(f"Session saved: {path}")
            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"{filename}.csv", mime="text/csv")
            
            # Show content calendar if enabled
            if show_calendar:
                st.markdown("### 📅 Content Calendar")
                calendar = generate_content_calendar(plan_items)
                import pandas as pd
                cal_df = pd.DataFrame(calendar)
                st.dataframe(cal_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

# Caption writer
st.subheader("✍️ Caption writer")
colA, colB = st.columns(2)
with colA:
    platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Twitter"])
    title = st.text_input("Idea title", "Top 3 ways to become job-ready in 60 days")
    key_points = st.text_area("Key points (bulleted or comma-separated)", "Choose one skill; build portfolio; network weekly")
with colB:
    tone2 = st.text_input("Tone/Voice", tone or "Encouraging, expert, simple")
    audience2 = st.text_input("Audience", audience or "Students and early-career professionals in India")
    cta = st.text_input("CTA", "Enroll today and start building your future")
hashtags = st.text_input("Hashtags (comma-separated)", "career,skills,education,jobready,india")
caption_btn = st.button("Generate caption")

if caption_btn:
    try:
        agent = agent or SocialAgent(model=model, temperature=temperature)
        with st.spinner("Writing caption..."):
            caption = agent.write_caption(
                platform=platform,
                tone=tone2,
                audience=audience2,
                title=title,
                key_points=key_points,
                cta=cta,
                hashtags=hashtags,
            )
        
        # Apply content style if selected
        if content_style != "Default":
            caption = apply_content_style(caption, content_style)
        
        # Add AI-generated hashtags if enabled
        if auto_hashtags:
            smart_tags = generate_smart_hashtags(title, niche or "general", platform)
            caption += f"\n\n{' '.join(smart_tags)}"
        
        st.success("Caption generated")
        
        # Real-time AI analysis
        analysis = analyze_caption_realtime(caption, platform)
        
        # Real-time preview with platform-specific formatting
        st.markdown("### 📱 Live Preview & AI Analysis")
        col_preview, col_stats, col_ai = st.columns([2, 1, 1])
        
        with col_preview:
            if platform == "Instagram":
                st.markdown(f"**Instagram Post**")
                st.text_area("Preview", caption, height=200, disabled=True, key="ig_preview")
            elif platform == "LinkedIn":
                st.markdown(f"**LinkedIn Post**")
                st.text_area("Preview", caption, height=200, disabled=True, key="li_preview")
            else:
                st.markdown(f"**Twitter/X Post**")
                st.text_area("Preview", caption, height=200, disabled=True, key="tw_preview")
        
        with col_stats:
            st.markdown("**📊 Stats**")
            limits = {"Instagram": 2200, "LinkedIn": 3000, "Twitter": 280}
            limit = limits[platform]
            
            st.metric("Characters", f"{analysis['char_count']}/{limit}")
            st.metric("Words", analysis['word_count'])
            st.metric("Hashtags", analysis['hashtag_count'])
            st.metric("Emojis", analysis['emoji_count'])
            
            if analysis['char_count'] > limit:
                st.error(f"⚠️ Exceeds {platform} limit!")
            elif analysis['char_count'] > limit * 0.9:
                st.warning(f"⚠️ Close to limit")
            else:
                st.success("✅ Within limit")
        
        with col_ai:
            st.markdown("**🤖 AI Score**")
            score = analysis['engagement_score']
            st.metric("Engagement", f"{score}/100")
            
            if score >= 80:
                st.success("🔥 Excellent!")
            elif score >= 60:
                st.info("👍 Good")
            else:
                st.warning("💡 Can improve")
            
            if analysis['has_cta']:
                st.success("✅ Has CTA")
            else:
                st.warning("❌ No CTA")
        
        # AI Suggestions
        if analysis['warnings']:
            st.error("⚠️ **Warnings:**")
            for warning in analysis['warnings']:
                st.write(f"• {warning}")
        
        if analysis['suggestions']:
            st.info("💡 **AI Suggestions:**")
            for suggestion in analysis['suggestions']:
                st.write(f"• {suggestion}")
        
        # Trending hashtags
        trending = get_trending_hashtags(niche)
        st.success(f"🔥 **Trending in {niche}:** {' '.join(trending)}")
        
        st.code(caption)
        
        # Advanced features
        if show_best_times:
            st.markdown("### ⏰ Best Posting Times")
            times = get_best_posting_times(platform)
            col_time1, col_time2 = st.columns(2)
            with col_time1:
                st.info(f"**Best Days:** {', '.join(times['best_days'])}")
                st.write(f"**Weekdays:** {', '.join(times['weekdays'])}")
            with col_time2:
                st.write(f"**Weekends:** {', '.join(times['weekends'])}")
        
        if show_sentiment:
            st.markdown("### 😊 Sentiment Analysis")
            sentiment = analyze_sentiment(caption)
            col_sent1, col_sent2, col_sent3 = st.columns(3)
            with col_sent1:
                st.metric("Sentiment", sentiment['sentiment'])
            with col_sent2:
                st.metric("Score", f"{sentiment['score']}%")
            with col_sent3:
                st.metric("Confidence", f"{sentiment['confidence']}%")
        
        if enable_ab_testing:
            st.markdown("### 🧪 A/B Test Variants")
            variants = generate_ab_variants(caption, num_variants)
            for variant in variants:
                with st.expander(f"📊 {variant['version']}"):
                    st.code(variant['caption'])
                    st.caption(f"Hook: {variant['hook']} | CTA: {variant['cta']}")
        
        if enable_translation:
            st.markdown(f"### 🌍 Translation ({target_language})")
            translated = translate_caption(caption, target_language)
            st.code(translated)
        
        if enable_competitor and competitor_handle:
            st.markdown("### 🔍 Competitor Insights")
            insights = get_competitor_insights(niche or "General")
            col_comp1, col_comp2 = st.columns(2)
            with col_comp1:
                st.write(f"**Top Content:** {', '.join(insights['top_content_types'])}")
                st.write(f"**Avg Engagement:** {insights['avg_engagement_rate']}")
            with col_comp2:
                st.write(f"**Posting Frequency:** {insights['posting_frequency']}")
                st.write(f"**Trending:** {', '.join(insights['trending_topics'])}")
    except Exception as e:
        st.error(f"Error: {e}")

# Repurpose tool
st.subheader("🔁 Repurpose across platforms")
source_platform = st.selectbox("Source platform", ["Instagram", "LinkedIn", "Twitter"], index=0)
original_caption = st.text_area("Original caption", placeholder="Paste a caption to repurpose...", key="repurpose_input")

# Real-time character count for input
if original_caption:
    input_chars = len(original_caption)
    st.caption(f"📝 Input: {input_chars} characters")

target_platforms = st.multiselect("Target platforms", ["Instagram", "LinkedIn", "Twitter"], default=["LinkedIn","Twitter"])
repurpose_btn = st.button("Repurpose")

if repurpose_btn:
    if not original_caption.strip():
        st.warning("Please paste an original caption.")
    else:
        try:
            agent = agent or SocialAgent(model=model, temperature=temperature)
            with st.spinner("Repurposing..."):
                outputs = agent.repurpose(source_platform, original_caption, target_platforms)
            if not outputs:
                st.warning("No repurposed outputs parsed. Try again with a shorter caption.")
            else:
                for plat, text in outputs.items():
                    st.markdown(f"**{plat} version:**")
                    
                    # Real-time stats for each repurposed version
                    col_text, col_stat = st.columns([3, 1])
                    with col_text:
                        st.code(text)
                    with col_stat:
                        char_count = len(text)
                        limits = {"Instagram": 2200, "LinkedIn": 3000, "Twitter": 280}
                        limit = limits.get(plat, 2200)
                        
                        st.metric("Chars", f"{char_count}/{limit}")
                        if char_count > limit:
                            st.error("⚠️ Over limit")
                        else:
                            st.success("✅ Good")
                
                st.success("Repurposed successfully.")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# Performance Predictor Dashboard
st.subheader("📊 Performance Predictor")
st.caption("Predict how your content will perform before posting")

pred_col1, pred_col2, pred_col3 = st.columns(3)

with pred_col1:
    pred_platform = st.selectbox("Platform for prediction", ["Instagram", "LinkedIn", "Twitter"], key="pred_platform")
    pred_time = st.selectbox("Posting time", ["Morning (6-9 AM)", "Midday (11 AM-2 PM)", "Evening (5-8 PM)", "Night (9 PM-12 AM)"])

with pred_col2:
    pred_content_type = st.selectbox("Content type", ["Educational", "Promotional", "Story", "Behind-the-scenes", "User-generated"])
    pred_has_visual = st.checkbox("Has image/video", value=True)

with pred_col3:
    pred_follower_count = st.number_input("Follower count", min_value=0, value=1000, step=100)
    pred_btn = st.button("Predict Performance")

if pred_btn:
    # Simple prediction algorithm
    base_engagement = 3.5
    
    # Platform multiplier
    platform_mult = {"Instagram": 1.2, "LinkedIn": 0.9, "Twitter": 0.8}
    base_engagement *= platform_mult[pred_platform]
    
    # Time multiplier
    time_mult = {"Morning (6-9 AM)": 1.1, "Midday (11 AM-2 PM)": 1.3, "Evening (5-8 PM)": 1.4, "Night (9 PM-12 AM)": 0.9}
    base_engagement *= time_mult[pred_time]
    
    # Content type multiplier
    content_mult = {"Educational": 1.2, "Promotional": 0.7, "Story": 1.4, "Behind-the-scenes": 1.3, "User-generated": 1.5}
    base_engagement *= content_mult[pred_content_type]
    
    # Visual multiplier
    if pred_has_visual:
        base_engagement *= 1.5
    
    # Calculate metrics
    engagement_rate = round(base_engagement, 2)
    estimated_likes = int(pred_follower_count * (engagement_rate / 100))
    estimated_comments = int(estimated_likes * 0.1)
    estimated_shares = int(estimated_likes * 0.05)
    estimated_reach = int(pred_follower_count * 1.5)
    
    st.markdown("### 🎯 Predicted Performance")
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    
    with metric_col1:
        st.metric("Engagement Rate", f"{engagement_rate}%")
    with metric_col2:
        st.metric("Est. Likes", estimated_likes)
    with metric_col3:
        st.metric("Est. Comments", estimated_comments)
    with metric_col4:
        st.metric("Est. Shares", estimated_shares)
    with metric_col5:
        st.metric("Est. Reach", estimated_reach)
    
    if engagement_rate >= 5:
        st.success("🔥 High engagement potential! Great time to post.")
    elif engagement_rate >= 3:
        st.info("👍 Good engagement expected.")
    else:
        st.warning("💡 Consider posting at a different time or with visual content.")

st.divider()
st.caption("Tip: Keep ideas varied each week: education, stories, BTS, social proof, UGC prompts, offers.")