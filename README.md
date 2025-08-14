# YouTube Views Counter

A Python script that extracts view counts from YouTube videos without using the YouTube API. The script can process multiple YouTube URLs from a text file and export the results to a CSV file.

## ⚠️ IMPORTANT DISCLAIMER
This tool is for educational and research purposes only. 
- YouTube's Terms of Service may prohibit automated data extraction
- Use at your own risk and responsibility
- Consider using YouTube's official API for production use
- Ensure compliance with applicable laws and terms of service

## Features

- **No API Required**: Scrapes view counts directly from YouTube pages without needing API keys
- **Batch Processing**: Process multiple YouTube URLs from a text file
- **Multiple URL Formats**: Supports various YouTube URL formats (`youtube.com/watch?v=`, `youtu.be/`, etc.)
- **CSV Export**: Save results to a CSV file with view counts and summary statistics
- **Error Handling**: Continues processing even if some URLs fail, with detailed error reporting
- **Rate Limiting**: Built-in delays to avoid being blocked by YouTube
- **Robust Parsing**: Uses multiple regex patterns and BeautifulSoup fallback for reliable extraction

## Requirements

- Python 3.6+
- Required packages:
  ```bash
  pip install requests beautifulsoup4
  ```

## Usage

### Command Line
```bash
python3 search.py input_file.txt [output_file.csv]
```

### Examples
```bash
# Basic usage - print results to console
python3 search.py urls.txt

# Save results to CSV file
python3 search.py urls.txt results.csv
```

### Input File Format
Create a text file with one YouTube URL per line:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/jNQXAC9IVRw
https://youtube.com/watch?v=9bZkp7q19f0
```

### Output Format
The script generates a CSV file with the following structure:
```
URL,Views
https://www.youtube.com/watch?v=dQw4w9WgXcQ,1234567890
https://youtu.be/jNQXAC9IVRw,987654321
https://youtube.com/watch?v=9bZkp7q19f0,Error: Invalid YouTube URL

Summary
Total Views,2222222211
Successful URLs,2
Failed URLs,1
```

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- URLs with additional parameters (e.g., `&t=30s`)

## Limitations

- **No API Guarantees**: Since this scrapes YouTube directly, it may break if YouTube changes their page structure
- **Rate Limiting**: Includes delays to avoid being blocked, making large batches slow
- **Accuracy**: View counts are approximate and may not match official API results

## Example Output
```
Processing 3 URLs...

Processing URL 1/3: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Views: 1,234,567,890

Processing URL 2/3: https://youtu.be/jNQXAC9IVRw
Views: 987,654,321

Processing URL 3/3: https://youtube.com/watch?v=invalid
Error: Invalid YouTube URL

Summary:
========================================
Total Views: 2,222,222,211
Successfully Processed URLs: 2
Failed URLs: 1
========================================

Results saved to results.csv
```
