'''
    test.py

    Test the pywindomainuser class

'''

import pywindomainuser

user = pywindomainuser.pywindomainuser()

def main():
    print('\ntest.py\n\n')

    output = ''

    retcode = user.checkADUser('qozb', output)

    print(output)

if __name__ == '__main__':
    main()