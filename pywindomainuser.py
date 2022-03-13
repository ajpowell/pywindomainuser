'''
    pywindomainuser.py

    python class to call 'net user <userid> /DOMAIN' to check if the
    supplied user is a member of the domain - if they are, then various 
    details are returned.

'''

import subprocess
import logging
import os
import platform
import sys

class pywindomainuser:
    # Constructor
    def __init__(self):
        # Check that this is a Windows system
        __platform = platform.system()

        logging.info('>>> Platform       : {}'.format(__platform))
        if(__platform.lower() != 'windows'):
            print('ERROR: pywindomainuser will only work on Windows systems')
            print('       Platform identified as {}'.format(__platform))
            sys.exit(-1)

        # Check that net.exe exists 
        __net_filename = 'net.exe'
        __windows_directory = os.getenv('windir')
        logging.info('>>> Windir         : {}'.format(__windows_directory))

        __net_filepath = os.path.join(os.path.join(__windows_directory, 'System32'), __net_filename)
        logging.info('>>> net.exe path   : {}'.format(__net_filepath))

        if not os.path.exists(__net_filepath):
            print('ERROR: net.exe not found on this system')
            sys.exit(-1)

        self.__include_lines = (
                'User name',
                'Full Name',
                'Account active',
                'Last logon',
                'Password last set',
                'Password expires'
                )

    def __format_output(self,command_output, processed_output, include_lines):
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


    def __run_command(self, command, include_lines, output):
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
        self.__format_output(raw_output, output, include_lines)
        
        return return_code  

    def __getFieldData(self, output, field):
        fielddata = ''
        for line in output:
            #print('  {}: {}'.format(line,line.find(field)))
            if line and (line.find(field)>=0):
                #print('Found field!')
                fielddata = line[len(field):].lstrip()
                #print(fielddata)
        
        return fielddata

    def checkADUser(self, username, output):
        __user = username.upper()

        command = ['net', 'user', __user, '/DOMAIN']

        __output = []

        retcode = self.__run_command(command, self.__include_lines, __output)

        # Get fields
        __ADUserName = self.__getFieldData(__output,'User name')
        __ADFullUserName = self.__getFieldData(__output,'Full Name')
        __ADAccountActive = self.__getFieldData(__output,'Account active')
        __ADLastLogon = self.__getFieldData(__output,'Last logon')
        __ADPasswordLastSet = self.__getFieldData(__output,'Password last set')
        __ADPasswordExpires = self.__getFieldData(__output,'Password expires')

        #print('@Username:   {}'.format(ADUserName))
        #print('@Fullname:   {}'.format(ADFullUserName))
        #print('@Active:     {}'.format(ADAccountActive))
        #print('@Last Logon: {}'.format(ADLastLogon))

        #print('{},{},{},\"{}\",{},{},{},{}'.format(user, retcode, ADUserName, 
        #    ADFullUserName, ADAccountActive, ADLastLogon,
        #    ADPasswordLastSet,ADPasswordExpires))

        output = { 
            'ADUserName': __ADUserName,
            'ADFullUserName': __ADFullUserName,
            'ADAccountActive': __ADAccountActive,
            'ADLastLogon': __ADLastLogon,
            'ADPasswordLastSet': __ADPasswordLastSet,
            'ADPasswordExpires': __ADPasswordExpires
        }

        print(output)

        return retcode

if __name__ == '__main__':
    pass
