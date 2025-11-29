# agent.py
import os
from typing import List, Dict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import (
    SOCIAL_STRATEGY_SYSTEM,
    SOCIAL_STRATEGY_TEMPLATE,
    CAPTION_SYSTEM,
    CAPTION_TEMPLATE,
    REPURPOSE_SYSTEM,
    REPURPOSE_TEMPLATE,
)

load_dotenv()


class PlanItem(BaseModel):
    post_date: str = Field(..., description="Day 1..Day 30")
    platform: str
    post_type: str
    idea_title: str
    key_points: str
    cta: str
    hashtags: str


class SocialAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in .env")
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def _invoke_chain(self, system_prompt: str, prompt: PromptTemplate, variables: dict):
        system_message = SystemMessage(content=system_prompt)
        human_message = HumanMessage(content=prompt.format(**variables))
        return self.llm.invoke([system_message, human_message])

    def create_30_day_plan(
        self,
        brand_name: str,
        niche: str,
        audience: str,
        tone: str,
        platforms: List[str],
        goal: str,
        constraints: str = "",
    ) -> List[PlanItem]:

        prompt = PromptTemplate(
            template=SOCIAL_STRATEGY_TEMPLATE,
            input_variables=["brand_name", "niche", "audience", "tone",
                             "platforms", "goal", "constraints"]
        )

        resp = self._invoke_chain(
            SOCIAL_STRATEGY_SYSTEM,
            prompt,
            {
                "brand_name": brand_name,
                "niche": niche,
                "audience": audience,
                "tone": tone,
                "platforms": ", ".join(platforms),
                "goal": goal,
                "constraints": constraints or "None",
            },
        )

        text = resp.content.strip()
        items: List[PlanItem] = []
        blocks = text.split("---")

        for block_text in blocks:
            block = {}
            for line in block_text.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.lower().replace(" ", "_").strip()
                    block[key] = value.strip()

            required = ["post_date", "platform", "post_type", "idea_title", "key_points", "cta", "hashtags"]
            if all(key in block for key in required):
                try:
                    items.append(PlanItem(**{k: block[k] for k in required}))
                except Exception:
                    continue

        return items

    def write_caption(
        self,
        platform: str,
        tone: str,
        audience: str,
        title: str,
        key_points: str,
        cta: str,
        hashtags: str,
    ) -> str:

        prompt = PromptTemplate(
            template=CAPTION_TEMPLATE,
            input_variables=["platform", "tone", "audience", "title", "key_points", "cta", "hashtags"],
        )

        resp = self._invoke_chain(
            CAPTION_SYSTEM,
            prompt,
            {
                "platform": platform,
                "tone": tone,
                "audience": audience,
                "title": title,
                "key_points": key_points,
                "cta": cta,
                "hashtags": hashtags,
            }
        )
        return resp.content.strip()

    def repurpose(
        self,
        source_platform: str,
        original_caption: str,
        target_platforms: List[str],
    ) -> Dict[str, str]:

        prompt = PromptTemplate(
            template=REPURPOSE_TEMPLATE,
            input_variables=["source_platform", "original_caption", "target_platforms"],
        )

        resp = self._invoke_chain(
            REPURPOSE_SYSTEM,
            prompt,
            {
                "source_platform": source_platform,
                "original_caption": original_caption,
                "target_platforms": ", ".join(target_platforms),
            }
        )

        text = resp.content.strip()
        outputs: Dict[str, str] = {}
        current = None
        buffer = []

        for line in text.splitlines():
            if line.startswith("[") and "]" in line:
                if current:
                    outputs[current] = "\n".join(buffer).strip()
                current = line.strip("[]:").strip()
                buffer = []
            else:
                buffer.append(line)

        if current and buffer:
            outputs[current] = "\n".join(buffer).strip()

        return outputs
