import os
import csv
import json
import random
from collections import defaultdict

class CSVConfig:
    _csv_filename = "cat_hat.csv"
    _config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt_sets", "_csv_config.json")

    @classmethod
    def load_config(cls):
        if os.path.isfile(cls._config_path):
            with open(cls._config_path, "r") as file:
                config = json.load(file)
                cls._csv_filename = config.get("csv_file", cls._csv_filename)
        else:
            cls._csv_filename = cls.get_first_csv_file()
            cls.save_config()

        # Check if the CSV file exists; if not, use the first CSV file in the directory
        csv_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt_sets")
        file_path = os.path.join(csv_directory, cls._csv_filename)
        if not os.path.isfile(file_path):
            cls._csv_filename = cls.get_first_csv_file()
            cls.save_config()

    @classmethod
    def save_config(cls):
        with open(cls._config_path, "w") as file:
            json.dump({"csv_file": cls._csv_filename}, file)

    @classmethod
    def get_csv_filename(cls):
        cls.load_config()
        return cls._csv_filename

    @classmethod
    def set_csv_filename(cls, filename):
        cls._csv_filename = filename
        cls.save_config()

    @classmethod
    def get_first_csv_file(cls):
        csv_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt_sets")
        csv_files = sorted([f for f in os.listdir(csv_directory) if f.endswith('.csv')])
        return csv_files[0] if csv_files else "cat_hat.csv"

class BuildPromptFromCSV:
    cycle_indices = defaultdict(int)
    cached_categories = {}

    @classmethod
    def get_categories(cls, file_path):
        if file_path in cls.cached_categories:
            return cls.cached_categories[file_path]

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' cannot be found. Please make sure the CSV file exists in the 'prompt_sets' folder and restart ComfyUI.")

        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension != ".csv":
            raise ValueError("Unsupported file type. Please provide a .csv file.")

        categories = defaultdict(list)
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip the first row containing category titles
            for row in reader:
                for i, value in enumerate(row):
                    if value.strip():
                        categories[headers[i]].append(value.strip())

        if not all(categories.values()):
            raise ValueError("One or more categories in the CSV file are empty.")

        cls.cached_categories[file_path] = (categories, headers)
        return categories, headers

    @classmethod
    def INPUT_TYPES(cls):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        csv_directory = os.path.join(script_directory, "prompt_sets")
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
        csv_filename = CSVConfig.get_csv_filename()
        file_path = os.path.join(csv_directory, csv_filename)
        print(f"Looking for CSV file at: {file_path}")

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' cannot be found. Please make sure the CSV file exists in the 'prompt_sets' folder and restart ComfyUI.")

        categories, headers = cls.get_categories(file_path)

        inputs = {
            "required": {
                "csv_file": (csv_files, {"default": csv_filename}),
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**32 - 1}),
            }
        }

        for i, header in enumerate(headers):
            category_options = ["None"] + categories[header]
            default_mode = "Fixed"
            if i == 0:
                default_mode = "Cycle"
            elif i == 1:
                default_mode = "Randomize"
            
            inputs["required"][f"{header}_mode"] = (["Fixed", "Randomize", "Cycle"], {"default": default_mode})
            inputs["required"][f"{header}_val"] = (category_options, {"label": header})
            inputs["required"][f"{header}_weight"] = ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01, "precision": 2})
            if i < len(headers) - 1:
                next_header = headers[i + 1]
                inputs["required"][f"{header}_to_{next_header}"] = ("STRING", {"default": ", "})

        return inputs

    RETURN_TYPES = ("STRING",)
    FUNCTION = "build_prompt"

    CATEGORY = "Prompt Nodes"

    def build_prompt(self, csv_file, seed, **kwargs):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        csv_directory = os.path.join(script_directory, "prompt_sets")
        current_csv_file = CSVConfig.get_csv_filename()
        
        if csv_file != current_csv_file:
            CSVConfig.set_csv_filename(csv_file)
            raise RuntimeError("CSV file has been changed. Please restart ComfyUI to apply the changes.")

        random.seed(seed)  # Set the random seed for reproducibility
        file_path = os.path.join(csv_directory, csv_file)
        categories, headers = self.get_categories(file_path)

        prompt_parts = []
        for i, header in enumerate(headers):
            mode = kwargs.get(f"{header}_mode", "Fixed")
            weight = kwargs.get(f"{header}_weight", 1.0)
            choice = None

            if mode == "Randomize":
                choice = random.choice(categories[header])
            elif mode == "Cycle":
                if header not in self.cycle_indices:
                    selected_value = kwargs.get(f"{header}_val", "None")
                    start_index = categories[header].index(selected_value) if selected_value in categories[header] else 0
                    self.cycle_indices[header] = start_index
                choice = categories[header][self.cycle_indices[header]]
                self.cycle_indices[header] = (self.cycle_indices[header] + 1) % len(categories[header])
            else:  # Fixed
                choice = kwargs.get(f"{header}_val", "None")
                if choice == "None":
                    continue

            if weight == 1.0:
                prompt_parts.append(choice)
            else:
                prompt_parts.append(f"({choice}:{weight:.2f})")

            if i < len(headers) - 1:
                next_header = headers[i + 1]
                separator = kwargs.get(f"{header}_to_{next_header}", ", ")
                prompt_parts.append(separator)

        prompt = "".join(prompt_parts)
        return (prompt,)

NODE_CLASS_MAPPINGS = {
    "BuildPromptFromCSV": BuildPromptFromCSV,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BuildPromptFromCSV": "Build Prompt From CSV",
}

__all__ = ['BuildPromptFromCSV']
