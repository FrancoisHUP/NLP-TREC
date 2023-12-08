import json

def write_run_file(results, file_path):
    with open(file_path, 'w') as f:
        for result in results:
            f.write(" ".join(map(str, result)) + "\n")

def write_result(result, file_path):
    # with open(file_path, 'w') as file:
    #     json.dump(overall_result, file, indent=4)
    with open(file_path, 'w') as f:
        for key, value in result.items():
            f.write(f"{key}: {value}\n")

