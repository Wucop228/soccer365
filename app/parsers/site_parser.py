import httpx
from lxml import html

def get_page(parse_date: str | None = None) -> str:
    url = 'https://soccer365.ru/online/'
    if parse_date:
        url += f'&date={parse_date}'
    return httpx.get(url=url).text

def get_info_match(tree: html.fromstring, match: str) -> dict | None:
    try:
        status = tree.xpath(f"{match}//div[@class='status']/span/text()")[0]
    except:
        return None
    # if status != 'Завершен': return None

    home_team = tree.xpath(f"{match}//div[@class='ht']/div[@class='name']//span/text()")[0]
    away_team = tree.xpath(f"{match}//div[@class='at']/div[@class='name']//span/text()")[0]
    score_home = tree.xpath(f"{match}//div[@class='ht']/div[@class='gls']/text()")[0]
    score_away = tree.xpath(f"{match}//div[@class='at']/div[@class='gls']/text()")[0]
    if score_home == "-" or score_away == "-": return None
    score = f"{score_home}:{score_away}"
    date = tree.xpath("//span[@class='icon16']/text()")[0]
    if not ('Завершен' in status or date[:5] in status): return None
    return {
        "home_team": home_team,
        "away_team": away_team,
        "score": score,
        "date": date,
    }

def get_matches(tree: html.fromstring, competition: str) -> list:
    results_matches = []
    cnt_matches = len(tree.xpath(f"{competition}/div")) - 1
    for match in range(cnt_matches):
        if (info_match := get_info_match(tree, f"{competition}/div[{match + 2}]")) != None:
            results_matches.append(info_match)
    return results_matches

def parse_all_competition(parse_date: str | None = None) -> dict:
    html_content = get_page(parse_date)
    results = {}
    tree = html.fromstring(html_content)
    cnt_competition = len(tree.xpath("//div[@id='result_data']/div")) - 1
    for competition in range(cnt_competition):
        xpath_cmp = f"//div[@id='result_data']/div[{competition + 1}]"
        results[tree.xpath(f"{xpath_cmp}/@id")[0]] = get_matches(tree, xpath_cmp)
    return results