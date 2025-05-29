import os

from modules.analyzer.ml_consumer_analyzer import MLConsumerAnalyzer
from modules.analyzer.ml_producer_analyzer import MLProducerAnalyzer

def analyze_producers(input_path, output_path, analyzer_path):
    output_folder = os.path.join(output_path, "producer")
    print(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    count = len(os.listdir(output_folder))
    result_name = f"producer_{count + 1}"
    output_folder = os.path.join(output_folder, result_name)
    os.makedirs(output_folder, exist_ok=True)
    producer_dict_path = os.path.join(analyzer_path, "library_dictionary", "library_dict_producers_2.csv")
    input_folder = input_path

    if not os.path.exists(producer_dict_path):
        print(f"Error Producer: The library dictionary '{producer_dict_path}' does not exist.")
        exit(1)
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        exit(1)

    analyzer = MLProducerAnalyzer(output_folder=output_folder)
    print(f"Analyzing producers with dictionary: {producer_dict_path}")
    print(f"Results will be saved in: {output_folder}")
    analyzer.analyze_projects_set(input_folder, producer_dict_path)
    return result_name

def analyze_consumers(input_path, output_path, analyzer_path, rules_3 = True, rules_4 = True):
    output_folder = os.path.join(output_path, "consumer")
    os.makedirs(output_folder, exist_ok=True)
    count = len(os.listdir(output_folder))
    result_name = f"consumer_{count + 1}"
    output_folder = os.path.join(output_folder, result_name)
    os.makedirs(output_folder, exist_ok=True)
    consumer_dict_path = os.path.join(analyzer_path, "library_dictionary", "library_dict_consumers_2.csv")
    producer_dict_path = os.path.join(analyzer_path, "library_dictionary", "library_dict_producers_2.csv")
    input_folder = input_path


    if not os.path.exists(consumer_dict_path):
        print(f"Error Consumer: The library dictionary '{consumer_dict_path}' does not exist.")
        exit(1)
    if not os.path.exists(producer_dict_path):
        print(f"Error Producer: The library dictionary '{producer_dict_path}' does not exist.")
        exit(1)
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        exit(1)

    analyzer = MLConsumerAnalyzer(output_folder=output_folder)
    print(f"Analyzing consumers with dictionary: {consumer_dict_path}")
    print(f"Results will be saved in: {output_folder}")
    print(f"Rules_3 is set to: {rules_3}")
    print(f"Rules_4 is set to: {rules_4}")
    analyzer.analyze_projects_set(input_folder, consumer_dict_path, producer_dict_path, rules_3, rules_4)
    return result_name
