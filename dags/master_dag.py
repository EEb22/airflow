import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

default_args = {
    "owner" : "airflow",
    "start_date" : airflow.utils.dates.days_ago(1)
}

with DAG(
    'master_dag', schedule_interval="*/5 * * * *", start_date=datetime(2023,1,1),
        #schedule_interval=timedelta(minutes=3), start_date=datetime(2023,2,27,10,57),
    default_args=default_args, catchup=False
) as dag:

    sensor = ExternalTaskSensor(
        task_id='sensor',
        external_dag_id='slave_dag',
        external_task_id='t1'#,
       # execution_delta=timedelta(minutes=2)
    )

    last_task = EmptyOperator(
        task_id='last_task'
    )

    sensor >> last_task



