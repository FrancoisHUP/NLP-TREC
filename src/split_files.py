def split_file_by_first_number(input_file):
    current_file = None
    current_number = None

    with open(input_file, 'r') as f:
        for line in f:
            number = line.split()[0]

            if number != current_number:
                if current_file:
                    current_file.close()

                current_number = number
                current_file = open(f'TREC AP 88-90/TREC AP 88-90/trec_qrels/qrel_{current_number}.txt', 'w')

            current_file.write(line)

    if current_file:
        current_file.close()

# Replace 'input.txt' with the path to your file
split_file_by_first_number('TREC AP 88-90/TREC AP 88-90/jugements de pertinence/qrels.101-150.AP8890.txt')