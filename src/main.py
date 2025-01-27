import os
import pandas as pd
from shared.application import Preprocessor as prep
from shared.application import HelperTools as ht
from charging.application.services.app import Application as app
from config import pdict

# ---------------------------------------------------------------------------
class DataLoader:
    """Handles loading and preprocessing of datasets"""

    def __init__(self, config):
        self.config = config

    def load_geodata(self):
        """Load geospatial data for Berlin PLZ"""
        return pd.read_csv(self.config["file_geodat_plz"], delimiter=";")

    def load_charging_stations(self):
        """Load electric charging stations dataset"""
        return pd.read_csv(self.config["file_lstations"], delimiter=";", encoding='utf-8')

    def preprocess_charging_stations(self, df_charging_stations, df_geodata):
        """Preprocess charging stations data"""
        df_preprocessed = prep.preprop_lstat(df_charging_stations, df_geodata, self.config)
        return prep.count_plz_occurrences(df_preprocessed)

    def load_residents_data(self):
        """Load population data by PLZ"""
        return pd.read_csv(self.config["file_residents"])

    def preprocess_residents_data(self, df_residents, df_geodata):
        """Preprocess population data"""
        return prep.preprop_resid(df_residents, df_geodata, self.config)


# ---------------------------------------------------------------------------
class DirectoryManager:
    """Handles directory setup and management"""

    @staticmethod
    def set_working_directory():
        """Set the current working directory to the script's location"""
        current_working_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_working_directory)
        print("Current working directory\n" + os.getcwd())


# ---------------------------------------------------------------------------
class ApplicationManager:
    """Manages the main application workflow"""

    def __init__(self, config):
        self.config = config
        self.data_loader = DataLoader(config)

    @ht.timer
    def run(self):
        """Run the main application"""
        DirectoryManager.set_working_directory()

        # Load and preprocess data
        print("Loading datasets...")
        df_geodata = self.data_loader.load_geodata()
        print("Geodata for Berlin loaded.")

        df_charging_stations = self.data_loader.load_charging_stations()
        print("Charging stations dataset loaded.")
        print(df_charging_stations.columns)

        gdf_charging_stations = self.data_loader.preprocess_charging_stations(
            df_charging_stations, df_geodata
        )
        print("Charging stations preprocessed.")

        df_residents = self.data_loader.load_residents_data()
        gdf_residents = self.data_loader.preprocess_residents_data(df_residents, df_geodata)
        print("Population data processed.")

        # Launch the Streamlit app
        print("Launching Streamlit app...")
        app_instance = app(gdf_charging_stations, gdf_residents)
        app_instance.run()
        print("Streamlit app running.")


# ---------------------------------------------------------------------------
# Entry point for the application
if __name__ == "__main__":
    app_manager = ApplicationManager(pdict)
    app_manager.run()
