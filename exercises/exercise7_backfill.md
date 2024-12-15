# Exercise 7 - Backfill

- Use a previously created DAG and use backfill to trigger runs before the start date
- Backfilling is possible using:
1. Run `docker compose ps` and find the name of the scheduler
2. Get into the scheduler using: 
    ```sh
    docker exec -it <scheduler name> /bin/bash
    ```
3. Run:
   ```sh
   airflow dags backfill -s <start date> -e <end date> <dag_name>
   ```
   (start date and end date can be formatted as "yyyy-mm-dd")
4. Check the DAG