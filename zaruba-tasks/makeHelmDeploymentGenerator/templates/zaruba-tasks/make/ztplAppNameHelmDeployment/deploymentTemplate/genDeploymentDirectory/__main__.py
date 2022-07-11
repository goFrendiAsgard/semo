import pulumi
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, LocalChartOpts
import os

app = Chart(
    'gen-deployment-name', 
    config=LocalChartOpts(
        path = './chart',
        namespace = os.getenv('NAMESPACE', 'default'),
        values = {},
        skip_await = True
    )
)

pulumi.export('app', app)
