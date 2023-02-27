import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner" : "airflow",
    "start_date" : airflow.utils.dates.days_ago(1)
}

with DAG(
    'slave_dag', schedule_interval="*/5 * * * *", start_date=datetime(2023,1,1),
    #schedule_interval=timedelta(minutes=3), start_date=datetime(2023,2,27,10,52),
    default_args=default_args, catchup=False
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 'test'"
    )

    t1