import os

class NotebookConverter:

    @staticmethod
    def convert_notebook_to_code(file_path: str) -> str:
        os.system(f'jupyter nbconvert --to script "{file_path}"')
        return file_path.replace(".ipynb", ".py")

    @staticmethod
    def convert_and_check(file_path: str) -> bool:
        file_py = NotebookConverter.convert_notebook_to_code(file_path)
        return os.path.exists(file_py)

    @staticmethod
    def convert_all_notebooks(folder_path: str) -> list:
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder {folder_path} does not exist.")

        converted_files = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.ipynb'):
                    full_path = os.path.join(root, file)
                    try:
                        converted_file = NotebookConverter.convert_notebook_to_code(full_path)
                        converted_files.append(converted_file)
                        print(f"Converted: {full_path} -> {converted_file}")
                    except Exception as e:
                        print(f"Error converting {full_path}: {e}")

        return converted_files
