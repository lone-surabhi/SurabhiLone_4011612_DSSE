from pydriller import Repository

def analyze_camel_aggregate(github_url, issue_ids):
    repo = Repository(github_url)
    
    all_found_commit_hashes = set()
    all_unique_file_paths = set()
    total_cumulative_dmm = 0.0

    print(f"Scanning {github_url} for issues: {issue_ids}...\n")

    for commit in repo.traverse_commits():
        if any(issue.upper() in commit.msg.upper() for issue in issue_ids):
            
            if commit.hash not in all_found_commit_hashes:
                all_found_commit_hashes.add(commit.hash)
                
                for m_file in commit.modified_files:
                    path = m_file.new_path or m_file.old_path
                    if path:
                        all_unique_file_paths.add(path)
                
                metrics = [
                    commit.dmm_unit_size,
                    commit.dmm_unit_complexity,
                    commit.dmm_unit_interfacing
                ]
                valid_metrics = [m for m in metrics if m is not None]
                if valid_metrics:
                    commit_dmm_score = sum(valid_metrics) / len(valid_metrics)
                    total_cumulative_dmm += commit_dmm_score

    total_commits = len(all_found_commit_hashes)
    
    if total_commits > 0:
        avg_files_changed = len(all_unique_file_paths) / total_commits

        avg_dmm_metric = total_cumulative_dmm / total_commits
    else:
        avg_files_changed = 0.0
        avg_dmm_metric = 0.0

    print("=" * 45)
    print("FINAL AGGREGATE RESULTS")
    print("=" * 45)
    print(f"Total Commits Analyzed:         {total_commits}")
    print(f"Average Number of Files Changed: {avg_files_changed:.2f}")
    print(f"Average DMM Metric:             {avg_dmm_metric:.4f}")
    print("=" * 45)

CAMEL_URL = "https://github.com/apache/camel.git"
TARGET_ISSUES = ['CAMEL-180', 'CAMEL-321', 'CAMEL-1818', 'CAMEL-3214', 'CAMEL-18065']

if __name__ == "__main__":
    analyze_camel_aggregate(CAMEL_URL, TARGET_ISSUES)