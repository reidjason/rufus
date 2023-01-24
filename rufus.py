import os
from datetime import datetime, timedelta
import sys


class DirectoryInfo:

    def __init__(self) -> None:
        self.dir = sys.argv[1]
        self.status = os.popen(f'cd {self.dir} && git status').read()
        self.commit = os.popen(f'cd {self.dir} && git log').read().split('\n')

    def get_active_branch(self, status: str) -> str:

        # status string appears as 'On branch branch_name'
        branch_name = status.split()[2]
        return branch_name

    def are_local_changes(self, status: str) -> bool:
        # Searches for Untracked files within status message
        try:
            return True if status.index("Untracked files:") > 0 else False
        except ValueError:
            return False

    def is_recent_commit(self, commit: str) -> bool:

        #Gets date from commit message and converts it.
        try:
            date = commit[2].split('Date:')[1].split('-')[0].strip()
            date = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")

            weekago = datetime.now() - timedelta(days=7)
            return True if date > weekago else False
        except IndexError:
            return False
    def should_we_blame_rufus(self, commit: str) -> bool:
        try:
            author = commit[1].split()[1]
            return True if author == 'rufus' else False
        except IndexError:
            return False

    def print_directory_info(self) -> None:
        print(f'active branch: {self.get_active_branch(self.status)}')
        print(f'local changes: {self.are_local_changes(self.status)}')
        print(f'recent commit: {self.is_recent_commit(self.commit)}')
        print(f'blame Rufus: {self.should_we_blame_rufus(self.commit)}')


DirectoryInfo().print_directory_info()
