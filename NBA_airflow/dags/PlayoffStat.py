import requests
from bs4 import BeautifulSoup
import pymysql
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.models import Variable


def parser_stat(**kwargs):
    url = Variable.get("nba_stats_url")
    # 建立連線
    conn = pymysql.connect(
        host="host.docker.internal",
        user="root",
        password="jason871226",
        database="NBA",
        charset="utf8mb4",
    )

    cursor = conn.cursor()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
    }
    response = requests.get(url, headers=headers)
    # 2. 解析 HTML
    print(response.json()["resultSets"][0]["rowSet"])
    # 3. 抓想要的資料，例如所有 <h1> 標題

    for x in response.json()["resultSets"][0]["rowSet"]:
        sql = """
        INSERT IGNORE INTO player_stats_playoff (
            player_id, player_name, nickname, team_id, team_abbreviation, age, gp, w, l, w_pct,
            min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct,
            oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd,
            pts, plus_minus, nba_fantasy_pts, dd2, td3, wnba_fantasy_pts,
            gp_rank, w_rank, l_rank, w_pct_rank, min_rank, fgm_rank, fga_rank, fg_pct_rank,
            fg3m_rank, fg3a_rank, fg3_pct_rank, ftm_rank, fta_rank, ft_pct_rank,
            oreb_rank, dreb_rank, reb_rank, ast_rank, tov_rank, stl_rank, blk_rank,
            blka_rank, pf_rank, pfd_rank, pts_rank, plus_minus_rank,
            nba_fantasy_pts_rank, dd2_rank, td3_rank, wnba_fantasy_pts_rank
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
        )
        """

        cursor.execute(sql, x)
        conn.commit()


# DAG設定
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 4, 26),
    "retries": 1,
}

with DAG(
    dag_id="nba_player_stats_playoff_dag",
    default_args=default_args,
    schedule_interval=None,  # 手動執行，或你可以改成每天跑一次 '0 6 * * *'
    catchup=False,
    tags=["nba", "crawler"],
) as dag:

    crawl_and_insert_task = PythonOperator(
        task_id="crawl_nba_stats_and_insert_db",
        python_callable=parser_stat,
    )
