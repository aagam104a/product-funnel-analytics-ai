import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def funnel_chart(view_users, cart_users, purchase_users):
    fig = go.Figure(go.Funnel(
        y=["View", "Cart", "Purchase"],
        x=[view_users, cart_users, purchase_users]
    ))
    fig.update_layout(
        title="User Funnel",
        margin=dict(l=20, r=20, t=50, b=20),
        height=500
    )
    return fig

def bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        margin=dict(l=20, r=20, t=50, b=20),
        height=500
    )
    return fig

def line_chart(df: pd.DataFrame, x_col: str, y_cols: list, title: str):
    fig = px.line(
        df,
        x=x_col,
        y=y_cols,
        title=title
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=500
    )
    return fig