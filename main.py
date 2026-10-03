
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Skin Clinic Campaign Analysis",
    description="API for analysing campaign response rates",
    version="1.0"
)

# Load dataset
df = pd.read_csv("skin clinic campaign.csv")

# Create product usage categories
df["Product_Usage"] = pd.cut(
    df["Unique_Products_Purchased"],
    bins=[0, 4, 8, float("inf")],
    labels=["1–4", "5–8", ">8"]
)


def calculate_response_rate(column):

    result = (
        df.groupby(column, observed=False)["Response_to_Campaign"]
        .agg(
            Customers="count",
            Responses=lambda x: (x == "Yes").sum()
        )
        .reset_index()
    )

    result["Response Rate (%)"] = (
        result["Responses"] /
        result["Customers"] * 100
    ).round(2)

    return result


# Home page
@app.get("/")
def home():

    return {
        "message": "Skin Clinic Campaign Analysis API",
        "endpoint": "/campaign-analysis"
    }


# Campaign analysis endpoint
@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():

    gender = calculate_response_rate("Gender")
    age = calculate_response_rate("AgeGroup")
    purchase = calculate_response_rate("Purchase_Last_Quarter")
    product = calculate_response_rate("Product_Usage")

    html = """
    <html>

    <head>
        <title>Campaign Analysis</title>

        <style>

        body {
            font-family: Arial;
            margin: 40px;
        }

        table {
            border-collapse: collapse;
            width: 80%;
            margin-bottom: 40px;
        }

        th, td {
            border: 1px solid black;
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #eeeeee;
        }

        </style>

    </head>

    <body>

    <h1>Skin Clinic Campaign Analysis</h1>

    <h2>1. Gender vs Campaign Response</h2>
    """

    html += gender.to_html(index=False)

    html += """
    <h2>2. Age Group vs Campaign Response</h2>
    """

    html += age.to_html(index=False)

    html += """
    <h2>3. Purchase in Last Quarter vs Campaign Response</h2>
    """

    html += purchase.to_html(index=False)

    html += """
    <h2>4. Product Usage vs Campaign Response</h2>
    """

    html += product.to_html(index=False)

    html += """
    </body>
    </html>
    """

    return html
