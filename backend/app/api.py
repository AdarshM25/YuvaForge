# backend/app/api.py
from fastapi import APIRouter
from .models import TrendRequest, TrendResponse
from .gcp_client import gemini_chat, embedding_genma


router = APIRouter()


@router.post("/career-trends", response_model=TrendResponse)
async def career_trends(req: TrendRequest):
# 1) Use Gemini to fetch a textual analysis of trends
prompt = f"Provide top 10 skills and district-level demand predictions for '{req.query}' in '{req.location or 'India'}'. Return JSON with skills and confidence percentages and district heatmap (example districts)."
gresp = gemini_chat(prompt)
# naive parsing — in production, use function-calling or structured output
text = getattr(gresp, 'text', None) or gresp


# 2) For demo, return dummy structured data (replace with a real parser)
top_skills = ["Skill A", "Skill B", "Skill C"]
scores = [0.87, 0.72, 0.65]
heatmap = {
"Pune": 0.87,
"Mumbai": 0.75,
"Bengaluru": 0.92,
}
return TrendResponse(query=req.query, top_skills=top_skills, confidence_scores=scores, district_heatmap_data=heatmap)