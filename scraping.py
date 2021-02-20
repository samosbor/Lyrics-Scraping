import requests
from bs4 import BeautifulSoup
import re
from bad_words import get_bw

def produce_url():
    #this function accepts input for an artist and a song and then outputs a url that will go
    #into the az = requests.get(url)

    #accept input
    artist = input("What is the artist of the song? ")
    song = input("What is the song title? ")

    #make sure to get rid of any spaces between names (Kanye West)

    def no_spaces(name):
        name = name.split(' ')
        new_name = ''
        for i in name:
            new_name += i.lower()
        return new_name

    artist = no_spaces(artist)
    song = no_spaces(song)

    #further considerations:
    # apostrophes
    # ampersands
    # misspellings

    return f'https://www.azlyrics.com/lyrics/{artist}/{song}.html'

def fetch_url(link):
    try:
        az = requests.get(link)
        soup = BeautifulSoup(az.text, 'html.parser')
        return soup
    except:
        print('Couldn\'t find the song. Try again')

def clean_lyrics(soup):
    #this function gets rid of html elements and empty spaces. 
    # improvements: 1. get rid of parentheses 2. get rid of \ before apostrophe 3. lower case everything

    soup_text = str(soup)
    b4mxm = soup_text.split(' MxM banner ')
    b4mxm.pop(1)
    b4mxm = str(b4mxm)
    b4mxm = b4mxm.split('Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that.')
    b4mxm.pop(0)
    b4mxm_str = str(b4mxm)
    soup_b4mxm = BeautifulSoup(b4mxm_str, 'html.parser')

    
    #print(soup_b4mxm.prettify())

    ### IM GOING TO USE REGULAR EXPRESSIONS HERE WE GOOOOOOOOOOO

    def clean_text(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    cleantext_1 = clean_text(b4mxm_str)
    #print(cleantext_1)
    text_list = cleantext_1.split('\\\\n')
    text_list.pop(0)
    text_list.pop(-1)
    lyrics_string = ''
    for i in text_list:
        lyrics_string += (' '+i)

    lyrics_string = lyrics_string.split(' ')
    #print(lyrics_string)

    final_list = []
    for i in lyrics_string:
        if i != '':
            final_list.append(i)

    #IMPROVEMENTS:
    #lowercase every word
    #get rid of parentheses
    #get rid of apostrophe problem with \\

    # This is the final list of lyrics
    return final_list

#print(clean_lyrics(url))

def find_bw(list_lyrics):
    badwordlist = get_bw()
    all_bw = []
    for i in list_lyrics:
        if i in badwordlist:
            all_bw.append(i)
    return all_bw

def score_bw(bw_list):
    #this function scores each bad word on a scale of 1-10 for how offensive it is
    #probably just going to list the worst 10 swear words and give it a score of 10 and leave 
    #all the other swear words at a one
    really_bw = ['fuck', 'cunt', 'pussy', 'bitch', 'dick', 'fucker', 
    'ass', 'ballsack', 'whore', 'nigga', 'nigger'
    ]
    count = 0
    for i in bw_list:
        if i in really_bw:
            count += 10
        else:
            count += 1
    return count

def main():
    try:
        #this produces the url based on inputs and saves
        lyric_url = produce_url()

        #this fetches the url just produced and saves as soup
        soup = fetch_url(lyric_url)

        #this cleans the lyrics and saves as a list
        lyric_list = clean_lyrics(soup)

        #this finds the bad words in the song and saves as a list
        list_bw = find_bw(lyric_list)

        print(f"The number of words in this song is {len(lyric_list)}")
        print(f'The number of bad words in this song is {len(list_bw)}')
        print(f'Thus, this song scores a {score_bw(list_bw)}')
        print(list_bw)
    
    except:
        print('Couldn\'t find the song you wanted. Try again?')

main()