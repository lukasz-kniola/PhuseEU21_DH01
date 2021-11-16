library(httr)
library(jsonlite)

# Send and retrieve HTTP (REST) request
res <- GET("https://clinicaltrials.gov/api/query/study_fields?expr=AREA[LeadSponsorName]Biogen&fields=NCTId,OrgStudyId,Acronym,SecondaryId&min_rnk=1&max_rnk=1000&fmt=json")

# Extract contents of request, store as list
data <- fromJSON(rawToChar(res$content))

# Drill to StudyFields and store as Dataframe
studyFields <- as.data.frame(data$StudyFieldsResponse$StudyFields)

# Optionally, remove records where Acronym is empty
acronyms <- studyFields[which(studyFields$Acronym != quote(character(0))),]

View(acronyms)
