from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json
import pandas as pd

# Initialize the Cosmos client
endpoint = "https://csmodelquality.documents.azure.com:443/"
key = {'masterKey': 'bBuBXUgMHPAaXhj31AI4W6gbGmZZm1MRg3agB4pschnTxbX7beg3b0i4PNyJ8C5WZtl7fp2t7QpKaOKWBCnnqw=='}
client = CosmosClient(endpoint, key)


def jsonlize(data):
    return json.dumps(data) if (isinstance(data, dict) or isinstance(data, list)) else data


def retrieve_data_from_cosmosdb(container_name, filter=None, database_name="powerbi"):
    database_id = client.get_database_client(database_name)
    container_id = database_id.get_container_client(container_name)

    pdf = pd.DataFrame()
    for each in container_id.read_all_items():
        if filter and any(filter[key]!=each[key] for key in filter.keys()):
            continue
        each_json = {key: [jsonlize(value)] for key, value in each.items()}
        row = pd.DataFrame.from_dict(each_json)
        if pdf.empty:
            pdf = row.copy()
        else:
            pdf = pd.concat([pdf, row], axis=0, ignore_index=True)

    if not pdf.empty:
        pdf.set_index('timestamp', inplace=True)
    return pdf


if __name__ == "__main__":
    container_name = "analysis_internal.anomaly_detect"
    filter = {"_dataset_name": "yahoo", "mlflow.project.entryPoint": "batch_yahoo"}
    pdf_anomaly_yahoo = retrieve_data_from_cosmosdb(container_name, filter)
    pd.set_option('display.max_columns', None)
    print(pdf_anomaly_yahoo.head())