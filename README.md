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



################### Run Report (run_report.sh) #####################

Bash script is a wrapper that takes in terminal input parameters and options.

Options are validated to be correct and sets user, pass, email, begin, and end 
variables to parameters passed.

The parameters are checked to validate that they are not null or empty

Then call create_report.py to generate a report into sqlite3 DB:
    create_report.py has it's exit codes evaluated and this script will
    email the customer an email corresponding to the return code

    If create report returns a 2:
        The user is emailed that there are no transactions between specified dates
    If create report returns a 1:
        The user is emailed that the input parameters for the dates was an incorrect form
    If create report retruns a 0:
        The program compresses the report into a zip file
        The zip file uses ftp binary transfer to send the zip to the server
        at var ftpAddr declared as a global at the top

        IF the ftp transfer completes successfully with the users name and password:
            An email is sent to the user that the transfer was successfully
        Else
            A message is displayed that ftp transfer failed,
            and the user is emailed that it failed due to user/password
