'''
This module defines a Flask web application with routes for rendering an index page,
handling form submissions to fetch and save data, and rendering a plot page.
Routes:
    - /: Handles GET and POST requests to render the index page and process form submissions.
    - /plot: Handles GET requests to render the plot page with the generated plot URL.
    - /assets: Handles GET requests to fetch and return the list of available crypto asset symbols.
Functions:
    - index(): Renders the index page and handles form submission to fetch and save data.
    - plot(): Renders the plot page with the generated plot URL.
    - get_assets(): Fetches and returns the list of available crypto asset symbols.
'''

from flask import Flask, render_template, request, redirect, url_for
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
from data_fetcher import fetch_and_save_data
from plot_char import create_plot


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the index page and handle form submission to fetch and save data.
    """
    if request.method == "POST":
        api_key = request.form["api_key"]
        api_secret = request.form["api_secret"]
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        asset = request.form.get("asset")

        # Call the function to fetch and save data
        response = fetch_and_save_data(api_key=api_key, api_secret=api_secret,
                                       start_date=start_date, end_date=end_date, asset=asset)

        if "success" in response:
            return redirect(url_for("plot", asset=asset))
        return render_template("result.html", result=response)

    return render_template("index.html")

@app.route("/plot")
def plot():
    """
    Render the plot page with the generated plot URL.
    """
    asset = request.args.get("asset")
    if not asset:
        return "Asset not specified", 400
    plot_url = create_plot(asset)
    return render_template("plot.html", plot_url=plot_url)

@app.route("/assets", methods=["GET"])
def get_assets():
    """
    Fetch and return the list of available crypto asset
    symbols using user-provided API key and secret.
    """
    api_key = request.args.get("api_key")
    api_secret = request.args.get("api_secret")
    client = TradingClient(api_key, api_secret)
    assets = [asset.symbol for asset in client.get_all_assets()
              if asset.asset_class == AssetClass.CRYPTO]
    return {"symbols": assets}

if __name__ == "__main__":
    app.run(debug=True)
