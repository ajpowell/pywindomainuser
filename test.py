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
    print('')
    logging.info('test.py')
    print('')

    userdetails = user.checkADUser('qozb')

    logging.info(userdetails)

    print('')

    logging.info('ADFullUserName : {}'.format(userdetails['ADFullUserName']))
    logging.info('ADLastLogon    : {}'.format(userdetails['ADLastLogon']))

    print('')
    logging.info('Done.')


if __name__ == '__main__':
    main()
