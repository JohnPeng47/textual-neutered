import json

def from_coverage_file(coverage_json: dict):
    counter = 0
    true_count = 0
    false_count = 0
    # # add exception catcher here for missing json
    for filename, data in coverage_json["files"].items():
        missing_lines = data["missing_lines"]
        executed_lines = data["executed_lines"]
        excluded_lines = data["excluded_lines"]
            
        total_stmts = data["summary"]["num_statements"]
        
        missing_check = len(missing_lines) + len(executed_lines) + len(excluded_lines) == total_stmts

        print(f"FIlename: [{filename}]")
        print(f"Missing check: [{missing_check}]")

        counter += -1 if missing_check else 1
        true_count += 1 if missing_check else 0
        false_count += 1 if not missing_check else 0
        
    print("True count: ", true_count, true_count/len(coverage_json["files"])) 
    print("False count: ", false_count, false_count/len(coverage_json["files"]))

from_coverage_file(json.load(open("coverage.json")))