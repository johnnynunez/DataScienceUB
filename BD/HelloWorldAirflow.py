from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def print_name( params,**context):
    print(context)
    name= context['task_instance'].xcom_pull(task_ids='Py_task_3')
    print(name,params["last_name"])

def pass_name():
    return 'Hello Rohit'

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'Rohit',
    'depends_on_past': False,
    'start_date': datetime(2022, 5, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('Helloworld', default_args=default_args, description="Hello World example", schedule_interval=timedelta(days=1))

# t1, t2, t3 and t4 are examples of tasks created using operators

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello World from Task 1"',
    dag=dag)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello World from Task 2"',
    dag=dag)

t3 = PythonOperator(
    task_id='Py_task_3',
    python_callable=pass_name,
    dag=dag)

t4 = PythonOperator(
    task_id='Py_task_4',
    provide_context=True,
    python_callable=print_name,
    params={'last_name': 'Kumar'},
    dag=dag)

t1>>t2
t1>>t3>>t4
