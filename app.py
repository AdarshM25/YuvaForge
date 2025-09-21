import streamlit as st
import httpx
import pandas as pd
import os


st.set_page_config(page_title="Career Trends", layout="wide")


API_BASE = st.secrets.get("api_base", os.getenv("API_BASE", "http://localhost:8000/api"))


st.title("Career Trends Explorer")
query = st.text_input("Enter a role or skill", "Electrical engineering")
location = st.text_input("Location (country or state)", "India")


if st.button("Get Trends"):
payload = {"query": query, "location": location}
with st.spinner("Querying backend..."):
try:
resp = httpx.post(f"{API_BASE}/career-trends", json=payload, timeout=30.0)
resp.raise_for_status()
data = resp.json()
except Exception as e:
st.error(f"Request failed: {e}")
st.stop()


st.subheader("Top skills")
skills = data.get("top_skills", [])
scores = data.get("confidence_scores", [])
df = pd.DataFrame({"skill": skills, "confidence": scores})
st.dataframe(df)


st.subheader("District heatmap (sample)")
heatmap = data.get("district_heatmap_data", {})
if heatmap:
df2 = pd.DataFrame(list(heatmap.items()), columns=["district", "score"])
st.bar_chart(df2.set_index("district"))


st.success("Done")