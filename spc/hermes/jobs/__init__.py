from dagster import job, op


@op
def run_soda_scan():
    pass


@job()
def taco():
    run_soda_scan()


def get_jobs():
    return [taco]
