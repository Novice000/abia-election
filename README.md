# Abia State Election Data Analysis

This project analyzes election data from polling units in Abia State. The code identifies clusters of polling units within a 6 km radius and calculates statistics on vote distributions within each cluster to detect voting patterns and potential anomalies.

## Table of Contents
1. [Requirements](#requirements)
2. [Data](#data)
3. [How It Works](#how-it-works)
4. [Outputs](#outputs)
5. [Usage](#usage)
6. [License](#license)

## Requirements

To run this code, install the following Python libraries:
```bash
pip install pandas numpy geopy scipy
```

## Data

The `abia_data.csv` file contains election data with the following columns:
- **Location Data**: `State`, `LGA`, `Ward`, `PU-Code`, `PU-Name`
- **Voter Data**: `Accredited_Voters`, `Registered_Voters`
- **Election Results**: `APC`, `LP`, `PDP`, `NNPP`
- **Result Metadata**: `Results_Found`, `Transcription_Count`, `Result_Sheet_Stamped`, `Result_Sheet_Corrected`, `Result_Sheet_Invalid`, `Result_Sheet_Unclear`, `Result_Sheet_Unsigned`, `Results_File`
- **Geolocation**: `lat`, `long`

## How It Works

The analysis workflow follows these steps:

1. **Load and Prepare Data**: Loads the election data and cleans the polling unit names.
2. **Create Polling Unit Clusters**:
   - Uses `lat` and `long` to create clusters of polling units within a 6 km radius.
   - A `cKDTree` from the `scipy.spatial` library allows for efficient spatial querying.
   - Stores nearby polling units in a dictionary, where each polling unit has a list of its neighbors.
3. **Aggregate Vote Data by Cluster**:
   - For each polling unit, collects vote counts within its cluster for the `APC`, `LP`, `PDP`, and `NNPP` parties.
4. **Calculate Statistical Metrics**:
   - Calculates the **mean** and **standard deviation** for each party’s vote count within each cluster.
   - Computes **z-scores** for each polling unit’s vote count relative to its cluster mean to detect anomalies.
   - Stores absolute values of z-scores for easier identification of extreme values.
5. **Save Results**:
   - Saves the processed data, including calculated metrics and z-scores, to `worked_abia.csv`.

## Outputs

The final output file, `worked_abia.csv`, includes the original data plus additional columns:
- **Cluster Statistics**:
  - `mean_apc`, `mean_lp`, `mean_pdp`, `mean_nnpp`: Mean votes for each party in each cluster.
  - `stdev_apc`, `stdev_lp`, `stdev_pdp`, `stdev_nnpp`: Standard deviation of votes for each party in each cluster.
- **Z-Scores**:
  - `z_apc`, `z_lp`, `z_pdp`, `z_nnpp`: Z-scores for each party’s votes in each polling unit.
  - `abs_z_apc`, `abs_z_lp`, `abs_z_pdp`, `abs_z_nnpp`: Absolute values of the z-scores.

## Usage

1. Place `abia_data.csv` in the same directory as the code.
2. Run the script:
   ```bash
   python abia_analysis.py
   ```
3. After execution, review `worked_abia.csv` for results.

## License

This project is open-source.