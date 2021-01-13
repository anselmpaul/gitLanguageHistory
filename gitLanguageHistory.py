import git
import os
import subprocess
import datetime
import csv
import math

def main():
    begin_time = datetime.datetime.now()
    repo = git.Repo('.')
    commitCount = len(list(repo.iter_commits()))
    commits = []
    branch = repo.active_branch
    allLanguages = []

    print('analysing', commitCount, 'commits. This is going to take some time...')
    
    for index, commit in enumerate(list(repo.iter_commits()), start=1):        
        # need to filter out semis and linebreaks
        commitMsg = commit.message.rstrip().replace(';', ',').replace('\n', ',')
        if "Merge branch" not in commitMsg:
            commitData = {
                'commitSha': commit.hexsha,
                'commitMessage': commitMsg,
                'commitDate': commit.committed_datetime.strftime("%d-%m-%Y")
            }

            repo.git.checkout(commit.hexsha)
            languages = {}
            linguistResult = subprocess.check_output('github-linguist').decode("utf-8").split('\n')
            for language in linguistResult:
                percentAndLanguage = language.split()
                if len(percentAndLanguage) > 1:
                    languages[percentAndLanguage[1]] = percentAndLanguage[0].replace('%', '')
            commitData = commitData | languages
            usedLanguages = languages.keys()
            allLanguages = list(set(allLanguages) | set(usedLanguages))
            commits.append(commitData)

        if (index > 0 and index % 10 == 0):
            timePassed = datetime.datetime.now() - begin_time
            print('- done with', index, 'commits (', timePassed.seconds, ')s')

    repo.git.checkout(branch)
    
    result = csv.writer(open('gitLanguageHistory.csv', 'w'), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    headers = ['commitSha', 'commitMessage', 'commitDate'] + allLanguages
    result.writerow(headers)

    for commit in commits:
        row = []
        for col in headers:
            if col in commit:
                row.append(commit[col])
            else:
                row.append(0)
        result.writerow(row)

    timePassed = datetime.datetime.now() - begin_time
    print('analysed', len(commits), 'commits (100%) in ', timePassed.seconds, 's')
    print('saved results to gitLanguageHistory.csv')
if __name__ == "__main__":
    main()
