'''
This module defines a Flask web application with routes for rendering an index page,
handling form submissions to fetch and save data, and rendering a plot page.
Routes:
    - /: Handles GET and POST requests to render the index page and process form submissions.
    - /plot: Handles GET requests to render the plot page with the generated plot URL.
Functions:
    - index(): Renders the index page and handles form submission to fetch and save data.
    - plot(): Renders the plot page with the generated plot URL.
'''
from flask import Flask, render_template, request, redirect, url_for
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

        # Call the function to fetch and save data
        response = fetch_and_save_data(api_key, api_secret, start_date, end_date)

        if "success" in response:
            return redirect(url_for("plot"))
        return render_template("result.html", result=response)

    return render_template("index.html")

@app.route("/plot")
def plot():
    """
    Render the plot page with the generated plot URL.
    """
    plot_url = create_plot()
    return render_template("plot.html", plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
