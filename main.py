from logger import log
from aws_sfn_generator import generate_multi_step_workflow

file = "./input/metadata.xlsx"
region = "us-west-1"
account_number = "1234567890"

if __name__ == '__main__':
    log.info("Generating Workflows started")
    generate_multi_step_workflow(file, region, account_number)
    log.info("Generating Workflows completed")
