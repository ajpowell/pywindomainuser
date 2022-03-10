'''
adcheck.py

Python code to check if users have Active Directory account.

Uses 'net user <user> /DOMAIN' as I was unable to install ldap libraries

'''

import subprocess
import logging

logging.root.handlers = []
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    #datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
    #level=logging.DEBUG
    )

ignore_lines = ()
include_lines = (
                'User name',
                'Full Name',
                'Account active',
                'Last logon',
                'Password last set',
                'Password expires'
                )

def format_output(command_output, processed_output, include_lines):
    #print(command_output)
    for line in command_output:
        #logging.debug(line)
        if line and any(s in line for s in include_lines):
            # deduplicate as we go...
            #if line not in processed_output:
            #    logging.debug('>>> {}'.format(line))
            #    processed_output.append(line)
            logging.debug('>>> {}'.format(line))
            processed_output.append(line)


def run_command(command, include_lines, output):
    process = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    raw_output = []
    logging.debug('--------------------')
    logging.debug('{} - {}'.format(command[0], command[1]))

    # Loop until command finished...
    while True:
        output_lines = process.stdout.readline()
        line = output_lines.strip()
        if line:
            logging.debug('> ' + line)
            raw_output.append(line)

        # Check for a return code i.e. command complete
        return_code = process.poll()
        if return_code is not None:
            logging.debug('>> RETURN CODE: {}'.format(return_code))
            break
    
    # process the output
    format_output(raw_output, output, include_lines)
    
    return return_code  


def checkADUser(username, output):
    command = ['net', 'user', username, '/DOMAIN']

    retcode = run_command(command, include_lines, output)

    return retcode

def getFieldData(output, field):
    fielddata = ''
    for line in output:
        #print('  {}: {}'.format(line,line.find(field)))
        if line and (line.find(field)>=0):
            #print('Found field!')
            fielddata = line[len(field):].lstrip()
            #print(fielddata)
    
    return fielddata

def main():

    users = [
'AAGT',
'AZMI',
'BBLV',
'BEOX',
'BHTI',
'BMAL',
'BSPY',
'BUNF',
'CAJD',
'CHVD',
'CVDE',
'DADO',
'DOGM',
'DOUL',
'DOXC',
'GADM',
'GDCU',
'GEGF',
'GHBH',
'GUNM',
'JAAO',
'JOTQ',
'KKIO',
'KPBT',
'KRDR',
'KRKS',
'KUHI',
'KXCN',
'KXCR',
'KXCS',
'LAHH',
'MASK',
'MICL',
'MKKN',
'MOFK',
'MOSR',
'MQCF',
'MRNG',
'MUUD',
'NAGR',
'NAKR',
'OKAA',
'QDBT',
'qipy',
'QJDR',
'QOSZ',
'QOZB',
'RAKP',
'RAMR',
'RAVB',
'RDAW',
'RMFV',
'RMGJ',
'RRJG',
'RSEX',
'SAPV',
'SCJZ',
'SEIE',
'SHEM',
'SHQD',
'SIIV',
'SJJH',
'STFH',
'STQU',
'SUDA',
'SUHL',
'SURV',
'THOO',
'VAJU',
'VAMZ',
'vihd',
'VINI',
'VRAD',
'WIGN',
'WMEN'
    ]

    for user in users:
        output = []
        retcode = checkADUser(user.upper(), output)

        #print(output)
        #print('\nretcode = {}\n'.format(retcode))

        # Get fields
        ADUserName = getFieldData(output,'User name')
        ADFullUserName = getFieldData(output,'Full Name')
        ADAccountActive = getFieldData(output,'Account active')
        ADLastLogon = getFieldData(output,'Last logon')
        ADPasswordLastSet = getFieldData(output,'Password last set')
        ADPasswordExpires = getFieldData(output,'Password expires')

        #print('@Username:   {}'.format(ADUserName))
        #print('@Fullname:   {}'.format(ADFullUserName))
        #print('@Active:     {}'.format(ADAccountActive))
        #print('@Last Logon: {}'.format(ADLastLogon))

        print('{},{},{},\"{}\",{},{},{},{}'.format(user, retcode, ADUserName, 
            ADFullUserName, ADAccountActive, ADLastLogon,
            ADPasswordLastSet,ADPasswordExpires))

if __name__ == '__main__':
    main()