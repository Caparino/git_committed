#!/usr/bin/env python3

import subprocess
from datetime import datetime, timedelta
import random

START_DATE = datetime(2024, 12, 1)

def calculate_days_between(start_date):
    """
    Calculate the number of days between the start date and today.

    :param start_date: The starting date
    :return: Number of days
    """
    today = datetime.now()
    return (today - start_date).days


def create_commits(start_date, file_name, commit_message):
    """
    Create 2-3 sequential commits per day from the start date to today.

    :param start_date: Starting date for commits
    :param file_name: File to modify for creating changes
    :param commit_message: Base commit message
    """
    # Calculate the total number of days
    num_days = calculate_days_between(start_date)

    print(f"Total days to commit: {num_days}")

    for day in range(num_days + 1):  # Include today
        current_date = start_date + timedelta(days=day)

        # Randomly decide the number of commits for the day (1-3)
        num_commits = random.randint(1, 3)

        # Generate random times for commits within the day
        commit_times = []
        for _ in range(num_commits):
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            commit_time = current_date.replace(hour=random_hour, minute=random_minute, second=random_second)
            commit_times.append(commit_time)

        # Sort commit times to ensure they are sequential
        commit_times.sort()

        # Create commits
        for i, commit_time in enumerate(commit_times):
            commit_date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")

            # Modify the file to create changes
            with open(file_name, "a") as f:
                f.write(f"Commit on {commit_date_str} (Commit {i + 1} of {num_commits} for the day)\n")

            # Stage the changes
            subprocess.run(["git", "add", file_name])

            # Create the commit with the backdated timestamp
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"{commit_message} - {i + 1} on {commit_date_str}",
                ],
                env={
                    **subprocess.os.environ,
                    "GIT_AUTHOR_DATE": commit_date_str,
                    "GIT_COMMITTER_DATE": commit_date_str,
                },
            )

            print(f"Created commit on {commit_date_str}")


def main():
    # Start date
    start_date = START_DATE

    # File to modify
    file_name = "changes.txt"

    # Commit message base
    commit_message = "Sequential backdated commit"

    # Create commits
    create_commits(start_date, file_name, commit_message)


if __name__ == "__main__":
    main()
