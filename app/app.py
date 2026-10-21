import os

import pandas as pd
import pyarrow.fs as fs
from flask import Flask

app = Flask(__name__)

s3 = fs.S3FileSystem(endpoint_override=os.environ.get("S3_ENDPOINT"))
BUCKET = os.environ.get("S3_BUCKET", "taxi")


@app.route('/trips/<day>')
def trips(day):
    df = pd.read_parquet(
        f"{BUCKET}/by_day",
        filesystem=s3,
        columns=["total_amount"],
        filters=[("pickup_day", "==", day)],
    )
    return f"{day}: {len(df)} trips, {df['total_amount'].mean():.2f} USD on average"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)