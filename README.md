[README.md](https://github.com/user-attachments/files/32858612/README.md)
# Python Mini Projects

Two small, beginner-friendly Python projects:

1. **Speech-to-Text Transcription** – convert audio recordings into text
2. **Weather Data Analysis and Prediction** – analyze temperature history and forecast trends

```
.
├── transcribe.py          # Project 1: speech-to-text CLI
├── weather_analysis.py    # Project 2: analysis + forecasting
├── sample.wav             # Example audio (synthetic voice)
├── transcript.txt         # Example transcription output
├── forecast.csv           # Example forecast output
└── weather_report.png     # Example plot output
```

---

## 1. Speech-to-Text Transcription

A command-line tool that converts audio files into text using the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library.

### Features
- Reads WAV, AIFF and FLAC directly; converts MP3, M4A, OGG and others automatically
- Background-noise calibration
- Splits long recordings into chunks (default 30 s) to stay within API limits
- Prints timestamped text as each chunk finishes
- Two engines: **Google** (online, more accurate, default) and **PocketSphinx** (offline, English only)
- Optional save to a `.txt` file

### Install
```bash
pip install SpeechRecognition

# Optional: MP3/M4A/OGG support
pip install pydub          # also install ffmpeg: https://ffmpeg.org/download.html

# Optional: offline engine
pip install pocketsphinx
```

### Usage
```bash
python transcribe.py recording.wav
python transcribe.py meeting.mp3 -o transcript.txt
python transcribe.py interview.wav --language es-ES --chunk 30
python transcribe.py recording.wav --engine sphinx      # offline
```

| Option | Description | Default |
|---|---|---|
| `audio` | Path to the audio file | required |
| `-o, --output` | Save transcript to a text file | none |
| `-l, --language` | Language code (e.g. `en-US`, `es-ES`, `fr-FR`) | `en-US` |
| `-c, --chunk` | Chunk length in seconds | `30` |
| `-e, --engine` | `google` or `sphinx` | `google` |

### Example output
```
[   0.0s] oh it is a estimates the zoo and three to whether to sunny and warm

=== Full transcript ===
oh it is a estimates the zoo and three to whether to sunny and warm

Saved to transcript.txt
```

> **Note on accuracy:** the example above was produced by the small offline engine on a robotic synthetic voice, so it is garbled. The Google engine on a clear human voice is much more accurate.

### Notes and limitations
- The Google engine needs an internet connection and is intended for short clips.
- Clear audio with little background noise gives the best results.
- Ideas to extend: live microphone input, subtitle (`.srt`) export, speaker labels, a simple GUI.

---

## 2. Weather Data Analysis and Prediction

Analyzes historical daily temperature data, measures long-term trends, and forecasts future temperatures with regression.

### Features
- Loads a CSV (any date column + daily temperature column) or uses built-in synthetic demo data
- Cleaning: sorts, removes duplicate dates, fills short gaps by interpolation
- Analysis: summary statistics, hottest/coldest day, monthly averages, warming trend per decade
- Model: linear regression with a time trend plus yearly seasonality (sine/cosine terms)
- Honest evaluation: trains on the earlier 80% of the data, tests on the final 20% (no shuffling), and compares against two baselines using MAE, RMSE and R²
- Forecast with a 95% range, saved as `forecast.csv`
- Three-panel plot saved as `weather_report.png`

### Install
```bash
pip install pandas numpy scikit-learn matplotlib
```

### Usage
```bash
python weather_analysis.py                       # demo with synthetic data
python weather_analysis.py --csv data.csv --date-col DATE --temp-col TAVG --days 365
```

| Option | Description | Default |
|---|---|---|
| `--csv` | Path to your CSV file | demo data |
| `--date-col` | Name of the date column | `date` |
| `--temp-col` | Name of the temperature column | `temp` |
| `--days` | Number of days to forecast | `365` |
| `--out` | Output plot filename | `weather_report.png` |

Free real-world data: [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/), [Meteostat](https://meteostat.net/), or weather datasets on Kaggle.

### Example results (synthetic demo data)

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Baseline (mean) | 7.38 | 8.45 | -0.005 |
| Baseline (day-of-year average) | 2.56 | 3.18 | 0.858 |
| Linear + 1 harmonic | 2.37 | 2.96 | 0.877 |
| Linear + 2 harmonics | 2.37 | 2.95 | 0.877 |

The fitted trend was +0.93 °C per decade against a true value of +0.8 in the synthetic data.

### Notes and limitations
- A model built only from date and season predicts the *typical* temperature for a day, not tomorrow's actual weather. Day-to-day variation is mostly noise.
- The 95% range covers individual days and does not include uncertainty in the trend, so long-range forecasts are less certain than the band suggests.
- Ideas to extend: lag features (recent temperatures), Random Forest, SARIMA or Prophet, extra variables such as humidity and pressure, and `TimeSeriesSplit` cross-validation.

---

## Requirements
- Python 3.9+
- Project 1: `SpeechRecognition` (optional: `pydub` + ffmpeg, `pocketsphinx`)
- Project 2: `pandas`, `numpy`, `scikit-learn`, `matplotlib`
