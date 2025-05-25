import rosu_pattern_detector_python

def get_pattern_stats(osu_file_path:str):
    return rosu_pattern_detector_python.get_patterns_python(osu_file_path)


if __name__ == "__main__":
    print(get_pattern_stats(r"C:\Users\shw42\source\maina-skill-stats\Kurokotei - Galaxy Collapse (Mat) [Cataclysmic Hypernova].osu"))