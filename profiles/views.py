import requests
from bs4 import BeautifulSoup
from decouple import config
from django.shortcuts import render

URL = config("URL")

def rank(request):
    profiles = []
    profiles += get_leetcode_profiles(start=0, end=98)
    profiles += get_leetcode_profiles(start=100, end=198)
    profiles += get_leetcode_profiles(start=200, end=298)
    profiles += get_leetcode_profiles(start=300, end=398)
    profiles += get_leetcode_profiles(start=400, end=499)
    return render(request, 'rank.html', {'profiles': profiles})

def get_leetcode_profiles(url=URL, start=1, end=98):
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        profiles = []
        for index, row in enumerate(soup.find_all('tr', class_='layout_trCenter__6KUQy')):
            if end is not None and index > end:
                break

            if index + 1 < start:
                continue

            columns = row.find_all('td')

            if len(columns) >= 3:
                avatar_url = columns[0].find('img')['src']
                reputation_count = columns[1].text.strip()
                rank = columns[2].text.strip()
                username = columns[0].text.split()[-1]
                profile_info = {
                    'username': username,
                    'avatar_url': avatar_url,
                    'reputation_count': reputation_count,
                    'rank': int(rank)
                }
                profiles.append(profile_info)

        return profiles

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None