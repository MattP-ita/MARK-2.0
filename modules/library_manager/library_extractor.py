from modules.utils.logger import get_logger
logger = get_logger(__name__)

class LibraryExtractor:

    @staticmethod
    def get_libraries_from_file(file_path: str) -> list:
        libraries = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="ISO-8859-1") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                logger.error(f"Error reading file {file_path}")
                return libraries
        except FileNotFoundError:
            logger.error(f"Error finding file {file_path}")
            return libraries

            # Your analysis logic here
        for line in lines:
            # delete trailing whitespaces at start if present
            line = line.lstrip()
            if 'import ' in line:
                if "from" in line:
                    libraries.append(line.split(' ')[1])
                else:
                    libraries.append(line.split(' ')[1])
        return libraries

    @staticmethod
    def check_ml_library_usage(file_path: str, library_dict):
        file_libraries = LibraryExtractor.get_libraries_from_file(file_path)
        for i in range(len(file_libraries)):
            if "." in file_libraries[i]:
                file_libraries[i] = file_libraries[i].split(".")[0]
        # filter dict libraries from file libraries
        dict_libraries = library_dict[library_dict['library'].isin(file_libraries)]

        return dict_libraries
