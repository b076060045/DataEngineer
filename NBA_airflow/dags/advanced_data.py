from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import paramiko

# === 定義要連線的參數 ===
SSH_HOST = "dbt"  # 你的 dbt container 名稱或 IP
SSH_PORT = 22
SSH_USER = "root"
SSH_PASSWORD = "jason871226"
SSH_WORKDIR = "/dbt/NBA"  # 這裡填你要指定的目錄，比如 /dbt/NBA


# === 定義 ssh 執行任務的方法 ===
def ssh_execute_command(**kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD
    )

    # 在指定目錄下執行指令，比如 ls -l
    command = f"cd {SSH_WORKDIR} && poetry run dbt run"
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode()
    error = stderr.read().decode()

    if output:
        print("Command Output:")
        print(output)
    if error:
        print("Command Error:")
        print(error)

    ssh.close()


# === 建立 DAG ===
with DAG(
    dag_id="ssh_execute_task",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ssh", "remote"],
) as dag:

    ssh_task = PythonOperator(
        task_id="ssh_run_command_in_dir",
        python_callable=ssh_execute_command,
        provide_context=True,
    )
