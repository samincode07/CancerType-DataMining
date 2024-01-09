#from cbio_py import cbio_mod as cb
import requests
import json
import csv


response = requests.get("https://www.cbioportal.org/api/cancer-types?direction=ASC&pageNumber=0&pageSize=10000000&projection=SUMMARY")
#print(response.json())

tcga_studies = requests.get("https://www.cbioportal.org/api/studies?direction=ASC&keyword=TCGA&pageNumber=0&pageSize=2&projection=DETAILED")
#print(tcga_studies.json())
field_names = ["cancerType", "studyId", "uniqueSampleKey", "uniquePatientKey",
                                  "molecularProfileId",
                                  "sampleId", "patientId", "mutationStatus", "referenceAllele",
                                  "proteinChange", "mutationType"]
List_BRCA1_Data = []
for study in tcga_studies.json():
    study_Id = study['studyId']
    cancerType_property = study["cancerType"]
    cancerType = study["name"]
    print(cancerType)
    #print("processing study id: " + study_Id)

    molecular_prof = requests.get("https://www.cbioportal.org/api/studies/"+study_Id+"/molecular-profiles?direction=ASC&pageNumber=0&pageSize=10000000&projection=SUMMARY")
    molecular_list = molecular_prof.json()

    samples = requests.get("https://www.cbioportal.org/api/studies/"+study_Id+"/sample-lists?direction=ASC&pageNumber=0&pageSize=10000000&projection=SUMMARY")
    sample_list = samples.json()


    for profile in molecular_list:
        profile_id = profile["molecularProfileId"]
        for sample in sample_list:
            samplelist_id = sample["sampleListId"]
            mutations = requests.get("https://www.cbioportal.org/api/molecular-profiles/"+profile_id+"/mutations?direction=ASC&entrezGeneId=672&pageNumber=0&pageSize=10000000&projection=SUMMARY&sampleListId="+samplelist_id)
            if mutations.status_code == 200:
                #print("processing mutations for sample list:  " + samplelist_id + " and profile id: " + profile_id)
                mutations_list = mutations.json()
                for mutation in mutations_list:
                    BRCA1_Data = {"cancerType": [], "studyId": [], "uniqueSampleKey": [], "uniquePatientKey": [],
                                  "molecularProfileId": [],
                                  "sampleId": [], "patientId": [], "mutationStatus": [], "referenceAllele": [],
                                  "proteinChange": [], "mutationType": []}
                    #BRCA1_Data["cancerType"].append(response)
                    BRCA1_Data["referenceAllele"].append(mutation["referenceAllele"])
                    BRCA1_Data["studyId"].append(mutation["studyId"])
                    BRCA1_Data["uniqueSampleKey"].append(mutation["uniqueSampleKey"])
                    BRCA1_Data["uniquePatientKey"].append(mutation["uniquePatientKey"])
                    BRCA1_Data["molecularProfileId"].append(mutation["molecularProfileId"])
                    BRCA1_Data["sampleId"].append(mutation["sampleId"])
                    BRCA1_Data["patientId"].append(mutation["patientId"])
                    BRCA1_Data["mutationStatus"].append(mutation["mutationStatus"])
                    BRCA1_Data["proteinChange"].append(mutation["proteinChange"])
                    BRCA1_Data["mutationType"].append(mutation["mutationType"])

                    #print(BRCA1_Data)

                    List_BRCA1_Data.append(BRCA1_Data)


with open("BRCA1_Data.csv", 'w') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames = field_names )
    writer.writeheader()
    writer.writerows(List_BRCA1_Data)

