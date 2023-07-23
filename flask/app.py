
import plotly.graph_objects as go

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')

db = client['sailu']


@app.route('/')

def index():

    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])

def form():

    if request.method == 'POST':

        # Save the data to MongoDB

        data = {col: request.form[col] for col in request.form}

        db.form_data.insert_one(data)

        return redirect(url_for('index'))

    return render_template('form.html')


@app.route('/excel', methods=['GET', 'POST'])

def excel_upload():

    if request.method == 'POST':

        # Read the uploaded Excel file and save the data to MongoDB

        file = request.files['file']

        if file.filename.endswith('.xlsx'):

            data_df = pd.read_excel(file)
            data = data_df.to_dict(orient='records')

            db.excel_data.insert_many(data)

            return redirect(url_for('index'))


    return render_template('excel_upload.html')


@app.route('/piechart')

def pie_chart():

    # Fetch data from MongoDB for pie charts

    data = list(db.form_data.find({}, {'_id': 0}))


    # Create a list to store pie chart HTML and max/min values

    pie_charts = []


    # Get all the column names dynamically
    columns = set()

    for item in data:

        columns.update(item.keys())


    # Create a pie chart for each column

    for column in columns:

        column_data = [item[column] for item in data if column in item and item[column] is not None]

        column_counts = pd.Series(column_data).value_counts()

        labels = column_counts.index.tolist()

        values = column_counts.tolist()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        pie_chart_html = fig.to_html(full_html=False)


        # Calculate max and min values for the column

        max_value = max(column_data) if column_data else None

        min_value = min(column_data) if column_data else None


        # Append the pie chart HTML and max/min values to the list

        pie_charts.append((pie_chart_html, max_value, min_value))


    return render_template('pie_chart.html', pie_charts=pie_charts)



@app.route('/dotplot')

def dot_plot_chart():

    # Fetch data from MongoDB for dot plot charts

    data = list(db.form_data.find({}, {'_id': 0}))


    # Create a list to store dot plot chart HTML and max/min values

    dot_plot_charts = []


    # Get all the column names dynamically
    columns = set()

    for item in data:

        columns.update(item.keys())


    # Create a dot plot chart for each column

    for column in columns:

        column_data = [item[column] for item in data if column in item and item[column] is not None]

        fig = go.Figure(data=[go.Scatter(x=column_data, y=[column] * len(column_data), mode='markers')])

        dot_plot_chart_html = fig.to_html(full_html=False)


        # Calculate max and min values for the column

        max_value = max(column_data) if column_data else None

        min_value = min(column_data) if column_data else None


        # Append the dot plot chart HTML and max/min values to the list

        dot_plot_charts.append((dot_plot_chart_html, max_value, min_value))


    return render_template('dot_plot_chart.html', dot_plot_charts=dot_plot_charts)

@app.route('/linegraph')
def line_graph():
    # Fetch data from MongoDB for line graph
    data = list(db.form_data.find({}, {'_id': 0}))

    # Create a list to store line graph HTML and max/min values
    line_graphs = []

    # Get all the column names dynamically
    columns = set()
    for item in data:
        columns.update(item.keys())

    # Create a line graph for each column
    for column in columns:
        column_data = [item[column] for item in data if column in item and item[column] is not None]
        
        # Convert the range object to a list using the list() function
        x_values = list(range(1, len(column_data) + 1))
        
        fig = go.Figure(data=[go.Scatter(x=x_values, y=column_data, mode='lines+markers', name=column)])
        line_graph_html = fig.to_html(full_html=False)

        # Calculate max and min values for the column
        max_value = max(column_data) if column_data else None
        min_value = min(column_data) if column_data else None

        # Append the line graph HTML and max/min values to the list
        line_graphs.append((line_graph_html, max_value, min_value))

    return render_template('line_graph.html', line_graphs=line_graphs)




if __name__ == '__main__':

    app.run(debug=True)

