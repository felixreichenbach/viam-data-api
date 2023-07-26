import asyncio
import functions_framework

from datetime import datetime
from dotenv import load_dotenv
import os
import sys

from viam.rpc.dial import Credentials, DialOptions
from viam.app.client import AppClient
from viam.app.data.client import Filter
from viam.proto.app.data import CaptureInterval

from google.protobuf.timestamp_pb2 import Timestamp

"""
    Credentials are imported through a .env file with the following structure:
    ADDRESS=robot.organisation.viam.cloud
    SECRET=yoursecret
"""
load_dotenv()


@functions_framework.http
def get_data(request):

    # Input data validation
    request_json = request.get_json(silent=True)

    print("// Selected Interval")
    print(f"Start Date: {request_json['date_start']}")
    print(f"End Date: {request_json['date_end']}")

    if request_json and "date_start" in request_json:
        date_start = request_json["date_start"]
    elif request_json and "date_end" in request_json:
        date_end = request_json["date_end"]
    elif request_json and "date_end" in request_json:
        component_name = request_json["component_name"]
    else:
        return "Query filter missing!"

    result = asyncio.run(query(request_json))

    return result


async def query(query_params):
    app: AppClient = await connect()
    date_start = int(
        datetime.timestamp(datetime.fromisoformat(query_params["date_start"]))
    )
    date_end = int(datetime.timestamp(datetime.fromisoformat(query_params["date_end"])))
    component_name = query_params["component_name"]

    if date_start > date_end:
        print("Verify interval! date_start must be before date_end!")
        sys.exit()

    data = await app.data_client.tabular_data_by_filter(
        filter=Filter(
            component_name=component_name,
            interval=CaptureInterval(
                start=Timestamp(seconds=date_start), end=Timestamp(seconds=date_end)
            ),
        )
    )
    app.close()
    return data


async def connect():
    address = os.getenv("ADDRESS")
    creds = Credentials(type="robot-location-secret", payload=os.getenv("SECRET"))
    dial_opts = DialOptions(
        credentials=creds,
        auth_entity=address,
    )
    app: AppClient = await AppClient.create(dial_opts)
    return app
