import csv
from CbioPortal_Data import get_studies, get_molecular_info, get_mutations


def create_cancer_data_file(file_name, List_of_Data, fields):
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        writer.writeheader()
        writer.writerows(List_of_Data)

def tcga_cancer_data():
    field_names = ["cancerType", "studyId", "uniqueSampleKey", "uniquePatientKey",
                   "molecularProfileId",
                   "sampleId", "patientId", "mutationStatus", "referenceAllele",
                   "proteinChange", "mutationType", "chr"]
    List_Mutations_All = []

    tcga_studies = get_studies()
    for study in tcga_studies:
        study_Id = study['studyId']
        cancerType_property = study["cancerType"]
        cancerType = study["name"]

        molecularprof_ids = get_molecular_info(study_Id)

        get_mutations(molecularprof_ids, cancerType,List_Mutations_All)

    create_cancer_data_file("venv/BCRA1_Data4.csv", List_Mutations_All, field_names)
