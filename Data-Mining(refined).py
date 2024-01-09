
import requests
import json
import csv

entrezGeneId = 672

#response = requests.get("https://www.cbioportal.org/api/cancer-types?direction=ASC&pageNumber=0&pageSize=10000000&projection=SUMMARY")
#print(response.json())

tcga_studies = requests.get("https://www.cbioportal.org/api/studies?direction=ASC&keyword=TCGA&pageNumber=0&pageSize=2&projection=DETAILED")
#print(tcga_studies.json())
field_names = ["cancerType", "studyId", "uniqueSampleKey", "uniquePatientKey",
                                  "molecularProfileId",
                                  "sampleId", "patientId", "mutationStatus", "referenceAllele",
                                  "proteinChange", "mutationType", "chr"]
List_BRCA1_Data = []
for study in tcga_studies.json():
    study_Id = study['studyId']
    cancerType_property = study["cancerType"]
    cancerType = study["name"]
    #print(canceType)
    #print("processing study id: " + study_Id)

    molecular_prof = requests.get("https://www.cbioportal.org/api/studies/"+study_Id+"/molecular-profiles?direction=ASC&pageNumber=0&pageSize=10000000&projection=SUMMARY")
    molecular_list = molecular_prof.json()

    array_profileid = []
    for profile in molecular_list:
        profile_id = profile["molecularProfileId"]
        array_profileid.append(profile_id)

    molecular_input = {"molecularProfileIds": array_profileid}
    #print(molecular_input)
    mutations = requests.post("https://www.cbioportal.org/api/mutations/fetch?direction=ASC&pageNumber=0&pageSize=10000000&projection=DETAILED", json = molecular_input)
    if mutations.status_code == 200:
            #print("processing mutations for sample list:  " + samplelist_id + " and profile id: " + profile_id)
        mutations_list = mutations.json()
        for mutation in mutations_list:
            BRCA1_Data = {"cancerType": [], "studyId": [], "uniqueSampleKey": [], "uniquePatientKey": [],
                              "molecularProfileId": [],
                              "sampleId": [], "patientId": [], "mutationStatus": [], "referenceAllele": [],
                              "proteinChange": [], "mutationType": [], "chr": []}
            BRCA1_Data["cancerType"].append(cancerType)
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
            BRCA1_Data["chr"].append(mutation["chr"])

                #print(BRCA1_Data)

            List_BRCA1_Data.append(BRCA1_Data)


with open("venv/BRCA1_Data4.csv", 'w') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames = field_names )
    writer.writeheader()
    writer.writerows(List_BRCA1_Data)

