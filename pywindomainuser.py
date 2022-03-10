'''
    pywindomainuser.py

    python class to call 'net user <userid> /DOMAIN' to check if the
    supplied user is a member of the domain - if they are, then various 
    details are returned
'''

import subprocess
import logging

class pywindomainuser:
    # Constructor
    def __init__(self):
        # TODO: Check that this is a Windows system
        # TODO: Check that net exists 
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
        user = username.upper()

        command = ['net', 'user', user, '/DOMAIN']

        __output = []
        retcode = self.__run_command(command, self.__include_lines, __output)

        # Get fields
        ADUserName = self.getFieldData(__output,'User name')
        ADFullUserName = self.getFieldData(__output,'Full Name')
        ADAccountActive = self.getFieldData(__output,'Account active')
        ADLastLogon = self.getFieldData(__output,'Last logon')
        ADPasswordLastSet = self.getFieldData(__output,'Password last set')
        ADPasswordExpires = self.getFieldData(__output,'Password expires')

        #print('@Username:   {}'.format(ADUserName))
        #print('@Fullname:   {}'.format(ADFullUserName))
        #print('@Active:     {}'.format(ADAccountActive))
        #print('@Last Logon: {}'.format(ADLastLogon))

        #print('{},{},{},\"{}\",{},{},{},{}'.format(user, retcode, ADUserName, 
        #    ADFullUserName, ADAccountActive, ADLastLogon,
        #    ADPasswordLastSet,ADPasswordExpires))

        output = { 
            'ADUserName': ADUserName,
            'ADFullUserName': ADFullUserName,
            'ADAccountActive': ADAccountActive,
            'ADLastLogon': ADLastLogon,
            'ADPasswordLastSet': ADPasswordLastSet,
            'ADPasswordExpires': ADPasswordExpires
        }

        return retcode