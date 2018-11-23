import os
import shutil
import glob

class DirectoryManager():

    def __init__(self, new_dir, old_dir):

        self.new_dir = new_dir
        self.old_dir = old_dir


    def create_if_not(self, path):

        if not os.path.exists(path):
            os.makedirs(path)

    def create_new_dir(self):

        self.create_if_not(self.new_dir)

    def move_user_dir(self, username, old, new=None):

        if not new:
            new = old

        src = self.old_dir + '/' + old + '/' + username
        dest = self.new_dir + '/' + username + '/' + new
        if os.path.exists(src):
            shutil.copytree(src, dest)

    def move_user_uploads(self, username):

        self.move_user_dir(username, 'upload')

    def move_user_results(self, username):

        self.move_user_dir(username, 'csv', 'result')

    def move_user_rdf(self, username):

        self.move_user_dir(username, 'rdf')
