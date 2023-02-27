from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime
from random import randint


def display_variable():
    my_var = Variable.get("my_var")
    print("variable: ", my_var)
    return my_var


def _training_model():
    return randint(1,10)


def _choose_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_c'
    ])
    best_accuracy = max(accuracies)
    if best_accuracy > 8:
        return 'accurate'
    return 'inaccurate'


with DAG("first_dag", start_date=datetime(2023, 1, 1),schedule_interval="@daily", catchup=False) as dag:

    display_variable = PythonOperator(
        task_id='display_variable',
        python_callable=display_variable
    )

    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model
    )

    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_C",
        python_callable=_training_model
    )

    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model
    )

    accurate = BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate = BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

    display_variable >> [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]


