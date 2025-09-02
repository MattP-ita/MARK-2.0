# MARK 2.0: Architectural Refactoring of a Classification Tool for Machine Learning Projects

**MARK 2.0** is an engineering refactoring of MARK: the tool automatically classifies Machine Learning (ML) projects 
based on their behavior with respect to model production and/or use, using heuristic rules and static analysis of source code.
The goal of this release is to improve readability, maintainability, and extensibility without altering the classification logic.

## CONTENT
**/modules**  All the modules that make up the tool:
- **analyzer**: contains all the classification logic, from classifier selection to its construction and use
- **cloner**: for cloning projects from Git
- **keyword_extractor**: contains the keyword extraction logic (Strategy Pattern)
- **library_manager**: contains all the scripts needed for managing libraries
- **scanner**: a tool that filters the files to be analyzed
- **utils**: contains the logger
- **oracle**: Tools for comparing results with oracle files.

## INSTALLATION
Install the required dependencies:
```sh
    pip install -r requirements.txt
```

Optional development tools (to replicate the quantitative evaluation):
```sh
    pip install -r dev-requirements.txt
```
After installation, create the JSON files for calculating the metrics:
```sh
   radon mi -s -j .\modules | Out-File -Encoding utf8 mi.json
   radon cc -s -j .\modules | Out-File -Encoding utf8 cc.json
```
Run the script to get the results:
```sh
   python calcola_voto.py
```

## CONFIGURATION
- **AnalyzerRole**: Select the analysis role (producer/consumer).
- **LibraryDictType**: Select the library dictionary for the role.
- **FileFilters**: Include/exclude files (e.g., exclude tests/examples for consumer rule 4).
- **KeywordExtractionStrategy**: Keyword extraction strategy (default: regex).
- **Input/output path**: Passed as parameters (not hard-coded).

The AnalyzerBuilder centralizes these choices and produces a ready-to-use analyzer.

## USAGE 
The configurations are in main.py.
1. **Repository Cloning**: The RepoCloner receives an integer N and clones the first N repositories from the configured source.
2. **Analysis (Classification)**: The Facade instantiates the correct analyzer based on the role (AnalyzerRole) and configuration (LibraryDictType), via Factory → Builder.
3. **Aggregation and Reporting**: Concludes with Merger and ResultAnalysis.

**Supported roles**: PRODUCER, CONSUMER

```sh
    python main.py
```
**Note**: In MARK 2.0, phases are modular and parameterizable; partially starting a single phase may require a minor modification to main.py (e.g., enabling/disabling steps).

## OUTPUT
- CSV/JSON with projects classified by role.
- Merger reports with metrics (accuracy, precision, recall, F1) compared to the oracle.
- Persistent logs in logs/ for each execution.

