#!/usr/bin/env python3


import pandas as pd
from base64 import b64encode, b64decode
from io import StringIO
import signal

ACCESS_TIME = 300


class TrialManager:
    def __init__(self, username):
        self.file = '/tmp/trial_light/info.csv'
        self.current_data = None
        self.user = username
        self.ACCESS_COUNT_LIMIT = 5
        self.update_data_at_trial_file()

    def update_data_at_trial_file(self):
        """
        Updates specific user information at trial_file.
        """
        self.read_trial_data()
        if self.user not in self.current_data:
            self.__add_data_to_trial_file()
        else:
            self.__check_user_accessibility()
        self.write_trial_data()

    def read_trial_data(self):
        """
        Reads trial data file and decodes it from base64 into string.
        """
        data = ''.join(open(self.file, 'r').read().splitlines())
        decoded_data = (b64decode(data)).decode('utf-8')
        self.current_data = self.__parse(str(decoded_data))

    def write_trial_data(self):
        """
        Writes updated data at file.
        """
        self.__make_ready_for_write()
        file = open(self.file, 'wb')
        decoded_data = b64encode(self.current_data.encode('utf-8'))
        file.write(decoded_data)

    def __add_data_to_trial_file(self):
        """
        Call if user doesn't exists.
        Added user info into dictionary.
        """
        limit = self.ACCESS_COUNT_LIMIT
        self.current_data[self.user] = limit

    def __parse(self, data):
        """
        Parses current trial file.
        Parses string as csv file format and then put it into dictionary.
        Returns:
            data_dict (dict)
        """
        parse_file = StringIO(data)
        csv_file = pd.read_csv(parse_file, header=None, names=['username', 'access_count'], )
        data_dict = {}
        try:
            for username in csv_file['username']:
                for access_count in csv_file['access_count']:
                    data_dict[username] = int(access_count)
        except:
            pass
        return data_dict

    def __make_ready_for_write(self):
        """
        Converts dictionary into string format
        """
        string = ''
        for user in self.current_data:
            string += '{username},{access_count}\n'.format(username=user, access_count=self.current_data[user])
        self.current_data = string

    def __check_user_accessibility(self):
        """
        Checks if user can use app. If the user used the application the number of times equal to the limit,
        he will not able to use it anymore.
        """
        if self.current_data[self.user] < 1:
            print("Intruder!!!")
            exit(0)
        else:
            self.current_data[self.user] -= 1


def handler(signum, frame):
    raise Exception("Your time is over.")


class App:
    def __init__(self):
        try:
            print("Welcome to super secure calculator. Print your expression:")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(ACCESS_TIME)
            while True:
                self.__super_secure_function()
        except Exception as e:
            print(e)

    def __super_secure_function(self):
        """
        Name change protection by spaces
        """
        expression = input()
        if expression == 'exit':
            signal.alarm(0)
            print("Thanks for using our super secure calc :)")
            exit(0)
        try:
            result = eval(expression)
            print(result)
        except:
            print("Not valid expression. Please retry. For exit print 'exit'.")


if __name__ == "__main__":
    name = input("Print your name: ")
    trial = TrialManager(name)
    App()
