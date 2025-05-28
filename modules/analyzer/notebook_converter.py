import os


class NotebookConverter:
    def __init__(self, jupyter_command="jupyter"):
        self.jupyter_command = jupyter_command

    def convert_notebook_to_code(self, file_path: str) -> str:
        os.system(f"{self.jupyter_command} nbconvert --to script \"{file_path}\"")
        return file_path.replace(".ipynb", ".py")

    def convert_and_check(self, file_path: str) -> bool:
        file_py = self.convert_notebook_to_code(file_path)
        return os.path.exists(file_py)

    def convert_all_notebooks(self, folder_path: str) -> list:
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder {folder_path} does not exist.")

        converted_files = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.ipynb'):
                    full_path = os.path.join(root, file)
                    try:
                        converted_file = self.convert_notebook_to_code(full_path)
                        converted_files.append(converted_file)
                        print(f"Converted: {full_path} -> {converted_file}")
                    except Exception as e:
                        print(f"Error converting {full_path}: {e}")

        return converted_files
