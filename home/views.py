from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from .dash_apps.cosmosdb import retrieve_data_from_cosmosdb
# Create your views here.


def home(requests):

    def scatter(pdf, col):
        x1 = pdf.index
        y1 = pdf[col]

        trace = go.Scatter(
            x=x1,
            y=y1,
        )

        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)]),
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    container_name = "analysis_internal.anomaly_detect"
    filter = {"_dataset_name": "yahoo", "mlflow.project.entryPoint": "batch_yahoo"}
    pdf_anomaly_yahoo = retrieve_data_from_cosmosdb(container_name, filter)
    context = {
        'plot1': scatter(pdf_anomaly_yahoo, "ms_precision_negative")
    }

    return render(requests, 'home/welcome.html', context)
