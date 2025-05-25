import rosu_pattern_detector_python
import json

def parse(s : str) -> dict:
    result = {}

    for line in s[1:-1].split(','):
        key, value = line.split(':', 1)
        result[key.strip()] = float(value.strip())

    return result

def aggregate_patterns(patterns: dict) -> dict:
    result = {}

    for k, v in patterns.items():
        main_type = k.split('(')[0].lower()

        if main_type == 'none':
            continue

        if main_type not in result:
            result[main_type] = 0.0

        result[main_type] += v
    return result

def get_pattern_stats(osu_file_path:str):
    raw_string =  rosu_pattern_detector_python.get_patterns_python(osu_file_path)
    raw_dic = parse(raw_string)
    aggreated_dic = aggregate_patterns(raw_dic)
    return aggreated_dic

if __name__ == "__main__":
    print(get_pattern_stats(r"C:\Users\shw42\source\maina-skill-stats\Kurokotei - Galaxy Collapse (Mat) [Cataclysmic Hypernova].osu"))