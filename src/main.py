from prefect import flow, task, get_run_logger

@flow
def main():
    print("This is First Test!!")

main()