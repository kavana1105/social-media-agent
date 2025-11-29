# advanced_features.py
from typing import List, Dict
import random
from datetime import datetime, timedelta

def get_best_posting_times(platform: str) -> Dict[str, List[str]]:
    """Return optimal posting times based on platform and audience"""
    times = {
        "Instagram": {
            "weekdays": ["9:00 AM", "11:00 AM", "1:00 PM", "7:00 PM"],
            "weekends": ["10:00 AM", "12:00 PM", "5:00 PM"],
            "best_days": ["Wednesday", "Friday"]
        },
        "LinkedIn": {
            "weekdays": ["7:00 AM", "8:00 AM", "12:00 PM", "5:00 PM"],
            "weekends": ["Not recommended"],
            "best_days": ["Tuesday", "Wednesday", "Thursday"]
        },
        "Twitter": {
            "weekdays": ["8:00 AM", "12:00 PM", "3:00 PM", "6:00 PM"],
            "weekends": ["9:00 AM", "11:00 AM", "7:00 PM"],
            "best_days": ["Wednesday", "Friday"]
        }
    }
    return times.get(platform, times["Instagram"])

def generate_ab_variants(original_caption: str, num_variants: int = 2) -> List[Dict[str, str]]:
    """Generate A/B test variants with different hooks and CTAs"""
    variants = []
    
    # Hook variations
    hooks = [
        "🔥 Hot take:",
        "💡 Pro tip:",
        "⚡ Quick question:",
        "🎯 Real talk:",
        "👀 You need to see this:",
        "🚀 Game changer:"
    ]
    
    # CTA variations
    ctas = [
        "Drop a comment below 👇",
        "Save this for later 📌",
        "Share with someone who needs this 💙",
        "DM us to learn more 📩",
        "Click the link in bio 🔗",
        "Tag a friend who needs to see this 👥"
    ]
    
    for i in range(num_variants):
        variant = {
            "version": f"Variant {chr(65+i)}",
            "hook": random.choice(hooks),
            "cta": random.choice(ctas),
            "caption": f"{random.choice(hooks)}\n\n{original_caption}\n\n{random.choice(ctas)}"
        }
        variants.append(variant)
    
    return variants

def analyze_sentiment(text: str) -> Dict[str, any]:
    """Analyze sentiment of the caption"""
    # Simple keyword-based sentiment (can be replaced with ML model)
    positive_words = ['great', 'amazing', 'excellent', 'love', 'best', 'awesome', 'fantastic', 'wonderful', 'success', 'win']
    negative_words = ['bad', 'worst', 'hate', 'terrible', 'awful', 'fail', 'problem', 'issue', 'difficult', 'hard']
    neutral_words = ['update', 'news', 'announcement', 'information', 'learn', 'know', 'understand']
    
    text_lower = text.lower()
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    neu_count = sum(1 for word in neutral_words if word in text_lower)
    
    total = pos_count + neg_count + neu_count
    
    if total == 0:
        return {"sentiment": "Neutral", "score": 0, "confidence": 50}
    
    if pos_count > neg_count:
        sentiment = "Positive"
        score = (pos_count / total) * 100
    elif neg_count > pos_count:
        sentiment = "Negative"
        score = -(neg_count / total) * 100
    else:
        sentiment = "Neutral"
        score = 0
    
    confidence = min(abs(score) + 50, 100)
    
    return {
        "sentiment": sentiment,
        "score": round(score, 1),
        "confidence": round(confidence, 1),
        "positive_words": pos_count,
        "negative_words": neg_count
    }

def get_competitor_insights(niche: str) -> Dict[str, any]:
    """Mock competitor analysis (can be replaced with real API)"""
    insights = {
        "EdTech": {
            "top_content_types": ["Tutorial videos", "Success stories", "Industry tips"],
            "avg_engagement_rate": "4.2%",
            "best_hashtags": ["#EdTech", "#OnlineLearning", "#SkillDevelopment"],
            "posting_frequency": "5-7 posts/week",
            "trending_topics": ["AI in education", "Remote learning", "Career skills"]
        },
        "Fitness": {
            "top_content_types": ["Workout videos", "Transformation posts", "Nutrition tips"],
            "avg_engagement_rate": "6.8%",
            "best_hashtags": ["#FitnessMotivation", "#WorkoutRoutine", "#HealthyLifestyle"],
            "posting_frequency": "7-10 posts/week",
            "trending_topics": ["Home workouts", "Meal prep", "Mental health"]
        }
    }
    
    return insights.get(niche, {
        "top_content_types": ["Educational", "Behind-the-scenes", "User stories"],
        "avg_engagement_rate": "3.5%",
        "best_hashtags": ["#Growth", "#Success", "#Community"],
        "posting_frequency": "4-6 posts/week",
        "trending_topics": ["Innovation", "Sustainability", "Digital transformation"]
    })

def generate_content_calendar(plan_items: List, start_date: datetime = None) -> List[Dict]:
    """Generate a visual content calendar"""
    if not start_date:
        start_date = datetime.now()
    
    calendar = []
    for i, item in enumerate(plan_items):
        post_date = start_date + timedelta(days=i)
        calendar.append({
            "date": post_date.strftime("%Y-%m-%d"),
            "day": post_date.strftime("%A"),
            "platform": item.platform if hasattr(item, 'platform') else "Instagram",
            "title": item.idea_title if hasattr(item, 'idea_title') else f"Post {i+1}",
            "type": item.post_type if hasattr(item, 'post_type') else "Educational"
        })
    
    return calendar

def apply_content_style(caption: str, style: str) -> str:
    """Apply content style modifications"""
    if style == "Viral":
        return f"🔥 STOP SCROLLING! 🔥\n\n{caption}\n\n💥 This is HUGE! Share if you agree! 👇"
    elif style == "Professional":
        return f"Industry Insight:\n\n{caption}\n\nThoughts? Let's discuss in the comments."
    elif style == "Storytelling":
        return f"Here's a story you need to hear...\n\n{caption}\n\nWhat's your story? Share below 👇"
    elif style == "Educational":
        return f"📚 Today's Lesson:\n\n{caption}\n\nWant to learn more? Follow for daily tips!"
    elif style == "Humorous":
        return f"😂 Real talk:\n\n{caption}\n\nTag someone who needs to see this! 😅"
    else:
        return caption

def translate_caption(caption: str, target_language: str) -> str:
    """Mock translation (replace with real translation API)"""
    translations = {
        "Spanish": f"[ES] {caption}\n\n(Traducción automática)",
        "French": f"[FR] {caption}\n\n(Traduction automatique)",
        "German": f"[DE] {caption}\n\n(Automatische Übersetzung)",
        "Hindi": f"[HI] {caption}\n\n(स्वचालित अनुवाद)",
        "Arabic": f"[AR] {caption}\n\n(ترجمة تلقائية)"
    }
    return translations.get(target_language, caption)

def generate_smart_hashtags(title: str, niche: str, platform: str) -> List[str]:
    """AI-powered hashtag generation based on content"""
    # Extract keywords from title
    keywords = title.lower().split()
    
    # Platform-specific hashtag strategies
    if platform == "Instagram":
        count = 15
    elif platform == "LinkedIn":
        count = 5
    else:  # Twitter
        count = 3
    
    # Niche-specific hashtags
    niche_tags = {
        "edtech": ["EdTech", "OnlineLearning", "SkillDevelopment", "CareerGrowth", "Education"],
        "fitness": ["Fitness", "Workout", "HealthyLifestyle", "FitnessMotivation", "GymLife"],
        "tech": ["Tech", "Innovation", "AI", "Programming", "TechNews"],
        "business": ["Business", "Entrepreneurship", "StartupLife", "Leadership", "Marketing"]
    }
    
    base_tags = niche_tags.get(niche.lower(), ["Growth", "Success", "Motivation"])
    
    # Generate hashtags
    hashtags = [f"#{tag}" for tag in base_tags[:count]]
    
    return hashtags
