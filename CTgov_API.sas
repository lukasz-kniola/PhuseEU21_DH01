filename request HTTP 'https://clinicaltrials.gov/api/query/field_values?expr=AREA[LocationCountry]Poland%20AND%20AREA[Condition]Multiple%20Sclerosis&field=LeadSponsorName&fmt=csv' debug;

proc import datafile=request 
    out=ct(rename=(VAR1=n VAR2=ValuesFound VAR3=StudiesFound VAR4=Sponsor)) 
    dbms=csv replace;
    getnames=no;
    datarow=14;
run;

proc sort data=ct;
    by descending StudiesFound;
    where StudiesFound ge 5;
run;
