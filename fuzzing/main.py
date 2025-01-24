import argparse
import os
import sys
import shutil

def arguments():
    parser = argparse.ArgumentParser(
        description="Fuzzing list builder"
    )
    parser.add_argument("input", help="Path that you want to build")
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output folder (default:false)")
    return parser.parse_args()

def get_files_paths(directory_path):
    files = []
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and file_path.endswith('.md'):
                files.append(file_path)
    except Exception as e:
        print(f"Error: {e}")
    return files

def create_output_folder(folder_path, overwrite):
    if os.path.exists(folder_path):
        if not overwrite:
            print(f"Output folder already exists, run with --overwrite if you want to overwrite the existing folder: {folder_path}")
            sys.exit(1)
        else:
            print(f"Output folder already exists, overwritting: {folder_path}")
            shutil.rmtree(folder_path)  
    os.makedirs(folder_path)
    print(f"Output folder created: {folder_path}")



def merge_list(input_list):
    if not input_list or len(input_list) < 2:
        return [] 

    merged_list = input_list[0]

    for sublist in input_list[1:]:
        merged_list = [prefix + suffix for prefix in merged_list for suffix in sublist]

    return merged_list

def parse_file(path):
    prefixes = {}
    suffixes = {}
    payloads = {}
    full_payloads = []
    with open(path, 'r') as file:
        mode = 'global'
        part = ''
        merge_prefix = []
        merge_suffix = []

        for line in file:
            strip_line = line.rstrip('\n')
            if strip_line == '':
                strip_line = '\n'
            # Handle mode and part changes
            if strip_line.startswith('# '):
                strip_line = strip_line.strip()
                mode = strip_line.split('# ')[1]
                prefixes[mode] = []
                suffixes[mode] = []
                payloads[mode] = []
                merge_prefix = []
                merge_suffix = []
                print(f'Mode: {mode}')
                continue
            elif strip_line.startswith('## '):
                strip_line = strip_line.strip()
                previous_part = part
                part = strip_line.split('## ')[1]
                if 'Prefix ' in previous_part and not 'Prefix ' in part:
                    prefixes[mode].extend(merge_list(merge_prefix))
                elif 'Suffix ' in previous_part and not 'Suffix ' in part:
                    suffixes[mode].extend(merge_list(merge_suffix))
                continue
            # Handle data
            if 'Prefix ' in part:
                index = int(part.split('Prefix ')[1])
                if len(merge_prefix) == index:
                    merge_prefix.append([])
                merge_prefix[index].append(strip_line)
            elif part == 'Full Prefix':
                prefixes[mode].append(strip_line)
            elif part == 'Payload':
                payloads[mode].append(strip_line)
            elif part == 'Full Payload':
                full_payloads.append(strip_line)
            elif 'Suffix ' in part:
                index = int(part.split('Suffix ')[1])
                if len(merge_suffix) == index:
                    merge_suffix.append([])
                merge_suffix[index].append(strip_line)
            elif part == 'Full Suffix':
                suffixes[mode].append(strip_line)
            else:
                print(f'Error, bad part: {part}')            
                sys.exit(1)
    return {'prefixes':prefixes, 'payloads':payloads, 'suffixes': suffixes, 'full_payloads': full_payloads}

def main():
    args = arguments()
    create_output_folder(args.output, args.overwrite)
    
    paths = get_files_paths(args.input)
    for path in paths:
        data = parse_file(path)
        with open(os.path.join(args.output,(path.split(os.sep)[-1])),'a') as fout:
            for full_payload in data['full_payloads']:
                fout.write(full_payload+'\n')
            for mode in data['prefixes'].keys():
                if mode == 'Global':
                    continue
                mode_prefixes = data['prefixes']['Global'] + data['prefixes'][mode]
                mode_payloads = data['payloads']['Global'] + data['payloads'][mode]
                mode_suffixes = data['suffixes']['Global'] + data['suffixes'][mode]
                for prefix in mode_prefixes:
                    for payload in mode_payloads:
                        for suffix in mode_suffixes:
                            fout.write(f'{prefix}{payload}{suffix}\n')
    return

main()