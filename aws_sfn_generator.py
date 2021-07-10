from utils.logger import log
import pandas as pd
import sys


def replace_job_holders(data: str, job_name: str):
    """Replaces job variables with job values"""
    job_names = job_name.split(',')
    for index, job in enumerate(job_names):
        job_index = "$$JOB_NAME_" + str(index + 1)
        data = data.replace(job_index, job.strip())
    return data


def generate_multi_step_workflow(file: str, region: str, account_number: str):
    """Generate Step Functions dynamically"""
    df = pd.read_excel(file)
    for row in df.itertuples():
        wf_name = row.WF_NAME
        job_name = row.JOB_NAME
        count = row.COUNT
        ind_file_path = row.IND_FILE_PATH
        file_name = "./output/" + wf_name + ".json"
        file_ind = str.lower(wf_name) + ".ind"
        log.info("Generate JSON for " + str(file_name) + " has started")
        file_object = open(file_name, 'w')
        if count == 1:
            template = open("./input/one_step_glue_jobs.json")
            data = template.read()
            replace_job_holders_rslt = replace_job_holders(data, job_name)
        elif count == 2:
            template = open("./input/two_step_glue_jobs.json")
            data = template.read()
            replace_job_holders_rslt = replace_job_holders(data, job_name)
        elif count == 3:
            template = open("./input/three_step_glue_jobs.json")
            data = template.read()
            replace_job_holders_rslt = replace_job_holders(data, job_name)
        elif count == 4:
            template = open("./input/four_step_glue_jobs.json")
            data = template.read()
            replace_job_holders_rslt = replace_job_holders(data, job_name)
        else:
            log.info("Template not found")
            sys.exit(1)

        replaced_data = replace_job_holders_rslt.replace("$$WF_NAME", wf_name) \
            .replace("$$REGION", region).replace("$$JOB_NAME", job_name).replace("$$IND_FILE_PATH", ind_file_path) \
            .replace("$$ACCOUNT_NUMBER", account_number).replace("$$FILE_IND", file_ind)
        file_object.write(replaced_data)
        file_object.close()
        template.close()
        log.info("Generate JSON for " + str(file_name) + " has completed")
    return True
