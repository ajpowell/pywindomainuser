'''
    test.py

    Test the pywindomainuser class

'''

import pywindomainuser
import logging

logging.root.handlers = []
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    #datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
    #level=logging.DEBUG
    )

user = pywindomainuser.pywindomainuser()

def main():
    print('\ntest.py\n\n')

    userdetails = ''

    retcode = user.checkADUser('qozb', userdetails)

    # TODO: Missing something obvious here, but userdetails not returned
    print(userdetails)

    print('')
    print('ADFullUserName : {}'.format(userdetails.ADFullUserName))
    print('ADLastLogon    : {}'.format(userdetails['ADLastLogon']))

if __name__ == '__main__':
    main()