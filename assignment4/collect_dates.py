import re
from typing import Tuple
from operator import itemgetter

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months


month_dict = {
            'january':'01', 'jan':'01',
            'february':'02', 'feb':'02',
            'march':'03', 'mar':'03',
            'april':'04', 'apr':'04',
            'may':'05',
            'june':'06', 'jun':'06',
            'july':'07', 'jul':'07',
            'august':'08', 'aug':'08',
            'september':'09', 'sep':'09',
            'october':'10', 'oct':'10',
            'november':'11', 'nov':'11',
            'december':'12', 'dec':'12'

}


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]il(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    oct = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"
    # Regex to capture days, months and years with numbers '(?P<area>\d{3})-(?P<extension>\d{4})'
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>\b(?:1\d{3}|20[0-2]\d\b))"
    # month should accept month names or month numbers
    month_iso = r"(?P<month_iso>\b(?:0\d|1[0-2])\b)"
    month = rf"(?P<month>(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec}))"
    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>\b(?:0\d|1\d|2\d|3[0-1])\b|\b(?:\d|1\d|2\d|3[0-1])\b)"

    # I return the month_isp separatly so it is easier to use.
    return year, month, month_iso, day



def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    if s.lower() in month_dict.keys():
        return month_dict[s]
    


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if len(n)==1:
        return str('0' + n)
    elif len(n)<1 or len(n)>2:
        raise ValueError("Incorrect day format")
    else:
        return n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, month_iso, day = get_date_patterns()
    
    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}-{month_iso}-{day}"

    # Date on format DD/MM/YYYY
    DMY = rf"{day}\s{month}\s{year}"

    # Date on format MM/DD/YYYY
    MDY = rf"{month}\s{day},\s{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\s{month}\s{day}"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []
    

    # find all dates in any format in text date_matches = re.findall(rf"{format}", html_string)
    for f in formats:
        match_dates = re.findall(rf"{f}", text)
        for match in match_dates:
            if not f == ISO: # because only ISO format does not support month name
                if f == DMY:
                    # get month number and fixing the day format: jan -> 01 and day: 1 -> 01
                    new_month = convert_month(str(match[1]).lower())
                    new_day = zero_pad(str(match[0]))
                    dates.append(str(match[2])+"/"+str(new_month)+"/"+str(new_day))
                    #match = re.sub(rf"({day})\s({month})\s({year})", r"\3/\2/\1", match)
                elif f == MDY:
                    new_month = convert_month(str(match[0]).lower())
                    new_day = zero_pad(str(match[1]))
                    dates.append(str(match[2])+"/"+str(new_month)+"/"+str(new_day))
                    #match = re.sub(rf"({month})\s({day})\s({year})", r"\3/\1/\2", match)
                elif f == YMD:
                    new_month = convert_month(str(match[1]).lower())
                    new_day = zero_pad(str(match[2]))
                    dates.append(str(match[0])+"/"+str(new_month)+"/"+str(new_day))
                    #match = re.sub(rf"({year})\s({month})\s({day})", r"\1/\2/\3", match)


            else: # ISO format
                dates.append(str(match[0])+"/"+str(match[1])+"/"+str(match[2]))
            
    #for data in dates:
        
    sorted_dates = sorted(dates)

                    
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        f = open(output, "w")
        for i in sorted_dates:
            f.write(str(i))
            f.write('\n')
        f.close()

    return sorted_dates
