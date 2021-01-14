import git
import os
import subprocess
import datetime
import csv
import math
import argparse

def main():
    begin_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Create a history of the programming languages used in your git repo.')
    parser.add_argument('--path', nargs='?', default='.',
                        help='path to your git repo, defaults to the current directory')

    args = parser.parse_args()

    repo = git.Repo(args.path)
    commitCount = len(list(repo.iter_commits()))
    branch = repo.active_branch
    writtenLines = 0

    print('analysing', commitCount, 'commits. This is going to take some time...')

    result = csv.writer(open('gitLanguageHistory.csv', 'w'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    headers = ['commitSha', 'commitMessage', 'commitDate', 'language', 'percent']# + allLanguages
    result.writerow(headers)
    
    for index, commit in enumerate(list(repo.iter_commits()), start=1):        
        # need to filter out semis and linebreaks
        commitMsg = commit.message.rstrip().replace(';', ',').replace('\n', ',')
        if "Merge branch" not in commitMsg:
            repo.git.checkout(commit.hexsha)
            linguistResult = subprocess.check_output('github-linguist', cwd=args.path.encode('utf-8')).decode("utf-8").split('\n')
            for language in linguistResult:
                row = [commit.hexsha, commitMsg, commit.committed_datetime.strftime("%d.%m.%Y"), "", ""]
                percentAndLanguage = language.split()
                if len(percentAndLanguage) > 1:
                    row[3] = percentAndLanguage[1]
                    row[4] = percentAndLanguage[0].replace('%', '')
                    result.writerow(row)
                    writtenLines = writtenLines + 1

        if (index > 0 and index % 10 == 0):
            timePassed = datetime.datetime.now() - begin_time
            print('- done with', index, 'commits (', timePassed.seconds, ')s, wrote', writtenLines, 'lines')

    repo.git.checkout(branch)        

    timePassed = datetime.datetime.now() - begin_time
    print('analysed', commitCount, 'commits (100%) in ', timePassed.seconds, 's')
    print('saved', writtenLines, 'lines to gitLanguageHistory.csv')
if __name__ == "__main__":
    main()
