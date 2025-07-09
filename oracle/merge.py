import os.path
import pandas as pd

from modules.utils.logger import get_logger
logger = get_logger(__name__)

class Merger:
    def __init__(self, column_name, oracle_path):
        self.column_name = column_name
        self.oracle_path = oracle_path

    def calc_performance_metrics(self, df):
        if df is None or df.empty:
            raise ValueError("[ERROR] Il DataFrame è vuoto o None.")

        tp = self.calc_true_positives(df, self.column_name)
        fp = self.calc_false_positives(df, self.column_name)
        tn = self.calc_true_negatives(df, self.column_name)
        fn = self.calc_false_negatives(df, self.column_name)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0

        return precision, recall, f1, accuracy

    def join(self, df_oracle, df_produced):
        df_oracle = pd.read_csv(df_oracle)
        df_produced = pd.read_csv(df_produced)
        df_produced.rename(columns={f'Is ML {self.column_name}': f'Is_ML_{self.column_name}'}, inplace=True)
        df_produced.drop_duplicates(subset=['ProjectName'], keep='first', inplace=True)
        df_produced = df_produced[['ProjectName', f'Is_ML_{self.column_name}']]
        df_joint = pd.merge(df_oracle, df_produced, on='ProjectName', how='left', validate='one_to_one')

        # replace nan values with 'No'
        df_joint[f'Is_ML_{self.column_name}'] = df_joint[f'Is_ML_{self.column_name}'].fillna('No')
        result_path = os.path.join(self.oracle_path, f'verifying/{self.column_name}_verification.csv')
        df_joint.to_csv(result_path, index=False)
        return df_joint

    def reporting(self, base_output_path, dir_result, file_name):
        result_path = os.path.join(base_output_path, self.column_name, dir_result, file_name)
        df_joint = self.join(os.path.join(self.oracle_path, f"oracle_{self.column_name}.csv"), result_path)
        precision, recall, f1, accuracy = self.calc_performance_metrics(df_joint)
        df_debug = self.get_false_positives(df_joint, self.column_name)
        df_debug.to_csv(os.path.join(self.oracle_path, f'verifying/{self.column_name}_false_positives.csv'),
                        index=False)
        df_debug = self.get_false_negatives(df_joint, self.column_name)
        df_debug.to_csv(os.path.join(self.oracle_path, f'verifying/{self.column_name}_false_negatives.csv'),
                        index=False)
        logger.info(f"Analysis done for {self.column_name}. Results saved in {self.column_name}_verification.csv")
        logger.info("Results:")
        logger.info(f"Precision: {precision}, Recall: {recall}, F1: {f1}, Accuracy: {accuracy}")

    @staticmethod
    def get_false_positives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'Yes')]

    @staticmethod
    def get_false_negatives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'No')]

    @staticmethod
    def calc_true_positives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'Yes')].shape[0]

    @staticmethod
    def calc_false_positives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'Yes')].shape[0]

    @staticmethod
    def calc_true_negatives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'No') & (df[f'Is_ML_{column_name}'] == 'No')].shape[0]

    @staticmethod
    def calc_false_negatives(df, column_name):
        return df[(df[f'Is_Real_ML_{column_name}'] == 'Yes') & (df[f'Is_ML_{column_name}'] == 'No')].shape[0]
