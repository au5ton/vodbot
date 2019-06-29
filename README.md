# vodbot
:tv: Automatically watches a provided list of Twitch vods, originally intended for OWL

## Dependencies
- Python 3 + pip
- Google Chrome installed
- Chrome webdriver installed + located

## Running an instance
- Clone repo: `git clone https://github.com/au5ton/vodbot.git`
- Install deps: `pip install -r requirements.txt`
- Rename `.env.example` to `.env` and fill out each variable with the correct information
- Run: `python vodbot.py --help`

## Ripping Overwatch League VOD data to CSV
```bash
python3 twitch_get_links.py -n overwatchleague -t highlight -s time -O owl.csv -csv
```

