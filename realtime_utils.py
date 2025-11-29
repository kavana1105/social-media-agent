# realtime_utils.py
import re
from typing import Dict, List

def analyze_caption_realtime(caption: str, platform: str) -> Dict[str, any]:
    """Analyze caption and provide real-time suggestions"""
    
    suggestions = []
    warnings = []
    
    # Character limits
    limits = {"Instagram": 2200, "LinkedIn": 3000, "Twitter": 280}
    limit = limits.get(platform, 2200)
    char_count = len(caption)
    
    # Check length
    if char_count > limit:
        warnings.append(f"Caption exceeds {platform} limit of {limit} characters")
    elif char_count > limit * 0.9:
        warnings.append(f"Close to {platform} character limit")
    
    # Hashtag analysis
    hashtags = re.findall(r'#\w+', caption)
    hashtag_count = len(hashtags)
    
    if platform == "Instagram" and hashtag_count > 30:
        warnings.append("Instagram allows max 30 hashtags")
    elif platform == "Twitter" and hashtag_count > 2:
        suggestions.append("Twitter posts perform better with 1-2 hashtags")
    elif platform == "LinkedIn" and hashtag_count > 5:
        suggestions.append("LinkedIn posts work best with 3-5 hashtags")
    elif hashtag_count == 0:
        suggestions.append("Consider adding relevant hashtags for better reach")
    
    # Emoji check
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE)
    
    emojis = emoji_pattern.findall(caption)
    emoji_count = len(emojis)
    
    if emoji_count == 0 and platform == "Instagram":
        suggestions.append("Instagram posts with emojis get 47% more engagement")
    elif emoji_count > 5:
        suggestions.append("Too many emojis might reduce readability")
    
    # CTA check
    cta_keywords = ['link in bio', 'click', 'visit', 'sign up', 'register', 'enroll', 'join', 'learn more', 'dm us', 'comment']
    has_cta = any(keyword in caption.lower() for keyword in cta_keywords)
    
    if not has_cta:
        suggestions.append("Add a clear call-to-action (CTA) to drive engagement")
    
    # Line breaks for readability
    lines = caption.split('\n')
    if len(lines) == 1 and char_count > 200:
        suggestions.append("Break long text into paragraphs for better readability")
    
    # Question check (engagement booster)
    if '?' not in caption:
        suggestions.append("Questions increase engagement - consider adding one")
    
    return {
        "char_count": char_count,
        "word_count": len(caption.split()),
        "hashtag_count": hashtag_count,
        "emoji_count": emoji_count,
        "has_cta": has_cta,
        "suggestions": suggestions,
        "warnings": warnings,
        "engagement_score": calculate_engagement_score(caption, platform)
    }

def calculate_engagement_score(caption: str, platform: str) -> int:
    """Calculate predicted engagement score (0-100)"""
    score = 50  # Base score
    
    # Length optimization
    char_count = len(caption)
    if platform == "Instagram" and 100 <= char_count <= 300:
        score += 10
    elif platform == "LinkedIn" and 150 <= char_count <= 500:
        score += 10
    elif platform == "Twitter" and 100 <= char_count <= 250:
        score += 10
    
    # Hashtags
    hashtag_count = len(re.findall(r'#\w+', caption))
    if 3 <= hashtag_count <= 5:
        score += 10
    
    # Emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    if len(emoji_pattern.findall(caption)) > 0:
        score += 10
    
    # CTA
    cta_keywords = ['link in bio', 'click', 'visit', 'sign up', 'register', 'enroll', 'join', 'learn more', 'dm us', 'comment']
    if any(keyword in caption.lower() for keyword in cta_keywords):
        score += 10
    
    # Question
    if '?' in caption:
        score += 10
    
    return min(score, 100)

def get_trending_hashtags(niche: str) -> List[str]:
    """Return trending hashtags for a niche (mock data - can be replaced with API)"""
    hashtag_db = {
        "edtech": ["#EdTech", "#OnlineLearning", "#SkillDevelopment", "#CareerGrowth", "#FutureOfWork"],
        "fitness": ["#FitnessMotivation", "#HealthyLifestyle", "#WorkoutRoutine", "#FitnessGoals", "#GymLife"],
        "food": ["#FoodPhotography", "#FoodLovers", "#Foodie", "#InstaFood", "#FoodBlogger"],
        "tech": ["#TechNews", "#Innovation", "#AI", "#Programming", "#TechTrends"],
        "business": ["#Entrepreneurship", "#BusinessGrowth", "#StartupLife", "#Leadership", "#Marketing"]
    }
    
    niche_lower = niche.lower()
    for key in hashtag_db:
        if key in niche_lower:
            return hashtag_db[key]
    
    return ["#Growth", "#Success", "#Motivation", "#Innovation", "#Community"]
