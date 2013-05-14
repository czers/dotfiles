"""Configuration info for files maintained by this repo is kept here"""
import argparse
import errno
import os
import shutil


class DotFile(object):
    """A configuration item for a single dotfile"""

    def __init__(self, repo_path, user_path):
        super(DotFile, self).__init__()
        self.repo_path = repo_path
        self.user_path = os.path.expanduser(user_path)

    def pull_local(self):
        """Pull a local copy of a dotfile into the repo"""
        try:
            shutil.copyfile(self.user_path, self.repo_path)
        except IOError as err:
            print "Could not pull %s from %s: (%s) %s" % (
                self.repo_path, self.user_path, err.errno, err.strerror)

    def push_repo(self):
        """Push a repo copy of a dotfile to some local location"""
        dotfile_dir = os.path.dirname(self.user_path)
        try:
            os.makedirs(dotfile_dir)
            print "Created directory for a dotfile: %s" % self.user_path
        except OSError as err:
            if err.errno == errno.EEXIST and os.path.isdir(dotfile_dir):
                pass
            else:
                raise
        shutil.copyfile(self.repo_path, self.user_path)


DOTFILES = [
    DotFile(repo_path='bashrc',
            user_path='~/.bashrc'),
    DotFile(repo_path='custom_prompt.sh',
            user_path='~/scripts/custom_prompt.sh'),
    DotFile(repo_path='natural_scroll.sh',
            user_path='~/scripts/natural_scroll.sh'),
    DotFile(repo_path='tmux.conf',
            user_path='~/.tmux.conf'),
]


def pull_local():
    """Pull all known dotfiles into the repo"""
    for dotfile in DOTFILES:
        dotfile.pull_local()


def push_repo():
    """Push all known dotfiles to local locations"""
    for dotfile in DOTFILES:
        dotfile.push_repo()


PULL_LOCAL_HELP = ("Pull the local copies of the dotfiles into the repo "
                   "(default)")
PUSH_REPO_HELP = "Push the repo copies of the dotfiles to the local locations"


def main():
    """Handle execution from command line"""
    parser = argparse.ArgumentParser(description="Manage local dotfiles.")
    parser.add_argument('-pl', '--pull_local', action='store_true',
                        default=True, dest='to_repo', help=PULL_LOCAL_HELP)
    parser.add_argument('-pr', '--push_repo', action='store_false',
                        dest='to_repo', help=PUSH_REPO_HELP)
    args = parser.parse_args()
    if args.to_repo:
        print "Pulling local dotfiles into the repo."
        pull_local()
    else:
        print "Pushing repo dotfiles into local locations."
        push_repo()


if __name__ == "__main__":
    main()
