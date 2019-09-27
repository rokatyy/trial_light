#!/usr/bin/env python3

import os, sys
import argparse
import pandas as pd
from base64 import b64encode, b64decode
from io import StringIO


class TrialManager:
    def __init__(self, username):
        self.file = '/tmp/trial_light/info.csv'
        self.current_data = None
        self.user = username
        self.ACCESS_COUNT_LIMIT = 5
        self.ACCESS_TIME = 300

    def update_data_at_trial_file(self):
        self.read_trial_data()
        if self.user not in self.current_data:
            self.__add_data_to_trial_file()
        else:
            self.__check_user_accessibility()
        self.write_trial_data()

    def read_trial_data(self):
        data = ''.join(open(self.file, 'r').read().splitlines())
        decoded_data = (b64decode(data)).decode('utf-8')
        self.current_data = self.__parse(str(decoded_data))

    def write_trial_data(self):
        self.__make_ready_for_write()
        file = open(self.file, 'wb')
        decoded_data = b64encode(self.current_data.encode('utf-8'))
        file.write(decoded_data)

    def __add_data_to_trial_file(self):
        self.current_data[self.user] = self.ACCESS_COUNT_LIMIT

    def __parse(self, data):
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
        string = ''
        for user in self.current_data:
            string += '{username},{access_count}\n'.format(username=user, access_count=self.current_data[user])
        self.current_data = string

    def __check_user_accessibility(self):
        if self.current_data[self.user] < 1:
            print("Intruder!!!")
            exit(0)
        else:
            self.current_data[self.user] -= 1


class User:
    def __init__(self, name):
        self.name = name
        self.clear_name()

    def clear_name(self):
        """
        Name change protection by spaces
        """
        self.name = ' '.join(name.split())

    def check_db(self):
        sql_query = 'select * from {table} where name = {name}'.format(table=TABLE_NAME, name=self.name)

    def create_new_user(self):
        sql_query = 'insert into {table} values(\'name\', 5'.format(table=TABLE_NAME, name=self.name,
                                                                    access_count=ACCESS_COUNT_LIMIT)

    @staticmethod
    def authorization():
        pass


class Manager:
    def __init__(self, action, secret_flag=None):
        self.flag = secret_flag
        if action == 'unistall':
            self.__unistall()
        elif action == 'install':
            self.__install()

    def __install(self):
        pass

    def __unistall(self):
        if self.flag is not None:
            self.__full_uninstall()

    def __full_uninstall():
        pass


if __name__ == "__main__":
    # name = input("Print your name: ")
    name = 'Anna'
    trial = TrialManager(name)
    trial.update_data_at_trial_file()
