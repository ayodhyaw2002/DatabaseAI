
import pandas as pd
import plotly.express as px
import plotly
import json

def generate_chart(user_prompt, df):
    """
    Generates a Plotly chart based on user prompt and dataframe.
    Supports: bar, line, pie
    """
    user_prompt = user_prompt.lower()
    try:
        if df.empty:
            return "<p>No data found for the chart.</p>"

        # Try to guess chart type from prompt
        if "bar" in user_prompt:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        elif "line" in user_prompt:
            fig = px.line(df, x=df.columns[0], y=df.columns[1])
        elif "pie" in user_prompt:
            fig = px.pie(df, names=df.columns[0], values=df.columns[1])
        else:
            return "<p>Unsupported chart type. Please use bar, line, or pie.</p>"

        return fig.to_html(full_html=False)
    except Exception as e:
        return f"<p>Error generating chart: {e}</p>"
