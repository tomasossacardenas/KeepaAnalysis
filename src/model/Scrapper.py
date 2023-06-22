class Scrapper:
    def __init__(self, name: str, columns: list, column_upc: str, exe_path: str, results_analysis: str, base_files_analysis: str):
        self._name = name
        self._columns = columns
        self._column_upc = column_upc
        self._exe_path = exe_path
        self._results_analysis = results_analysis
        self._base_files_analysis = base_files_analysis