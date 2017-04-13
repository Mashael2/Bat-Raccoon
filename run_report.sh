#!/bin/bash -
#===============================================================================
#
#          FILE: run_report.sh
#
#         USAGE: ./run_report.sh
#
#   DESCRIPTION:
#
#       Bash script is a wrapper that takes in terminal input parameters and options.
#
#       Options are validated to be correct and sets user, pass, email, begin,
#       and end variables to parameters passed.
#
#       The parameters are checked to validate that they are not null or empty.
#
#       Then call create_report.py to generate a report into sqlite3 DB:
#           create_report.py has it's exit codes evaluated and this script will 
#           email the customer an email corresponding to the return code
#           If create report returns a 2:
#               the user is emailed that there are no transactions between
#               specified dates
#           If create report returns a 1:
#               the user is emailed that the input parameters for the
#               dates was an incorrect formT
#           If create report retruns a 0:
#               the program compresses the report into a zip file
#               the zip file uses ftp binary transfer to send the zip to the
#               server @ var ftpAddr declared as a global at the top
#
#               IF the ftp transfer completes successfully with the users name
#               and password:
#                   an email is sent to the user that the transfer was successfully
#               Else
#                   a message is displayed that ftp transfer failed,
#                   and the user is emailed that it failed due to user/password
#
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: DAVID MARILUCH (), davidmariluch@mail.weber.edu
#  ORGANIZATION: WSU
#       CREATED: 04/11/2017 20:58
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error


ftpAddr="137.190.19.99"     # create ftpAddr

# How script is used
usage()
{
    echo "Usage: hw8.sh -u <FTPuser> -p <FTPpw> -e <email> -f <begDate> -t <endDate>"
}



# Check for options and parameters
while getopts ":u:p:e:f:t:" opt
    do
        case $opt in
            u) user=$OPTARG   # username to ssh
                ;;
            p) pass=$OPTARG   # password to ssh
                ;;
            e) email=$OPTARG  # email to send verification email
                ;;
            f) begin=$OPTARG  # begin date to query range from date in python
                ;;
            t) end=$OPTARG    # end date to query range from date in python
                ;;
            \?) usage
                ;;
    esac
done

# Test if parameters are set. -z checks to see if the value is null
if [[ -z $user ]]
then
    echo "The user name must be specified"
    usage
    exit 1
fi

if [[ -z $pass ]]
then
    echo "The password must be specified"
    usage
    exit 1
fi

if [[ -z $email ]]
then
    echo "The email must be specified"
    usage
    exit 1
fi

if [[ -z $begin ]]
then
    echo "The begin date must be specified"
    usage
    exit 1
fi

if [[ -z $end ]]
then
    echo "The end date must be specified"
    usage
    exit 1
fi

# function for compressing and transfering file over ftp
# Returns compress and ftp return code
compressAndTransfer()
{
    file="company_trans_$begin"_"$end.dat"
    zipName="company_trans_$begin"_"$end.zip"

    # echo "File: $file"
    # echo "ZipName: $zipName"

    zip $zipName $file
    ftplog=$PWD/ftp.log

    # ftp into ftpAddr
    ftp -nv $ftpAddr <<EOF > $ftplog
    quote user $user
    quote pass $pass
    binary
    put $zipName
    bye
EOF

    grep "230 Login successful" $ftplog
    grep "226 Transfer complete" $ftplog
    rcode=$?
    # echo "FTP return code: $rcode"
    if [[ $rcode -eq 0 ]]
    then
        echo "Your output file is $zipName"
        # echo "Successful FTP"
        `rm $ftplog`
    fi

    return "$rcode"
}


# Call create_report.py and check return codes
echo "Getting transactions from $begin to $end"
./create_report.py $begin $end
rc=$?     # rc is the return code that we get from calling create report 
# echo "Create report return code: $rc"

# check the return code
if [[ rc -eq 0 ]]
then
    compressAndTransfer
    code=$?
    # echo "Compress and Transfer code: $code"
    echo "Emailing report to $email"

    if [[ $code -eq 0 ]]
    then
        ` mail -s "Successfully transfer file ($ftpAddr)" $email <<< "Succesfully created a transaction report from BegDate:$begin to EndDate:$end"`
    else
        echo "Ftp transfer failed"
        ` mail -s "Ftp transfer failed ($ftpAddr)" $email <<< "Username: $user / Password: $pass is incorrect to ftp to Address: $ftpAddr"`
        exit 3
    fi
elif [[ rc -eq 1 ]]
then
    ` mail -s "The create_report program exited with code 1" $email <<< "Bad input parameters BegDate:$begin & EndDate:$end"`
    exit 1
elif [[ rc -eq 2 ]]
then
    ` mail -s "The create_report program exited with code 2" $email <<< "No transactions available from BegDate:$begin toEndDate:$end"`
    exit 2
else
    echo "Something went horribly wrong"
    echo "Create report failed"
    exit 4
fi


exit 0

