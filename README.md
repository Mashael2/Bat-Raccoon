# Bat-Raccoon


create_report.py Modules:
    
convertEndDateertBegDate() - 
  Change the start date format from YYYYMMDD to YYYY-MM-DD hh:mm
  
convertEndDate() - 
  Change the start date format from YYYYMMDD to YYYY-MM-DD hh:mm
  
createRepo() - 
  Create report of transactions
  
main() - 
  Test function
  
  
run_report.sh Function:

Bash script is a wrapper that takes in terminal input parameters
and options. They are validated to be correct and used to 
call create_report.py to generate a report into sqlite3 database.

Script create_report.py then has it's exit codes evaluated and run_report.sh 
will email the customer an email corresponding to the return code.






