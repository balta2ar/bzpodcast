"""
<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
  <channel>
    <title>My RSS Feed</title>
    <description>This is my RSS Feed</description>
  </channel>
  <item>
    <title>My RSS entry</title>
    <link>http://example.com/entry4711</link>
    <pubDate>Tue Dec  9 01:27:53 MSK 2014</pubDate>
    <description>Good news</description>
    <guid>http://example.com/entry4711</guid>
  </item>
  <item>
    <title>My RSS entry</title>
    <link>http://example.com/entry4711</link>
    <pubDate>Tue Dec  9 01:27:21 MSK 2014</pubDate>
    <description>Good news</description>
    <guid>http://example.com/entry4711</guid>
  </item>
</rss>
"""


import os
import glob
import argparse
import logging
from datetime import datetime
from datetime import tzinfo
from email.utils import formatdate
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4StreamInfoError

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


BODY = '''<?xml version="1.0" encoding="utf-8"?>
 <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
 <channel>
 <atom:link href="http://192.168.1.2/feed.xml" rel="self" type="application/rss+xml" />
     <title>{podcast_title}</title>
     <link>http://192.168.1.2</link>
     <description>{podcast_description}</description>
     <lastBuildDate>{date}</lastBuildDate>
     <language>en-us</language>
     <copyright>Copyright 2010 © WHOEVER</copyright>
     <itunes:subtitle>BZ local feed</itunes:subtitle>
     <itunes:author>BZ</itunes:author>
     <itunes:summary>{podcast_description}</itunes:summary>
     <itunes:owner>
         <itunes:name>BZ</itunes:name>
         <itunes:email>maintainer@email.com</itunes:email>
     </itunes:owner>
     <itunes:image href="http://192.168.1.2/logo.jpg" />
     <itunes:category text="Category1" />
     <itunes:category text="Category2">
            <itunes:category text="Subcategory" />
     </itunes:category>
  {items}
     <itunes:explicit>no</itunes:explicit>
 </channel>
 </rss>
'''

ITEM = '''
<item>
    <title>{title}</title>
    <link>{link}</link>
    <itunes:author>Item Author</itunes:author>
    <description>{title}</description>
    <itunes:summary>{title}</itunes:summary>
    <enclosure url="{link}" length="{size}" type="audio/mpeg"/>
    <guid>{link}</guid>
    <pubDate>{date}</pubDate>
    <itunes:duration>{duration}</itunes:duration>
    <itunes:keywords>Keywords</itunes:keywords>
    <category>Podcasts</category>
    <itunes:explicit>no</itunes:explicit>
</item>
'''


HOST = 'http://192.168.1.2/{0}'


def get_pubDate(name):
    date = datetime.fromtimestamp(os.path.getmtime(name))
    return formatdate(float(date.strftime('%s')), tzinfo())


def get_length(name):
    logging.info('get_length: "%s"', name)
    encoder = None
    if name.endswith('.mp3'):
        encoder = MP3
    elif name.endswith('.mp4'):
        encoder = MP4
    else:
        raise ValueError('Unknown media type: "%s"' % name)
    try:
        return int(encoder(name).info.length)
    except MP4StreamInfoError:
        logging.info('Failed to get length for "%s"', name)
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate podcast feed from files')
    parser.add_argument('--files', type=str, default='*.mp3',
                        help='Input files glob')
    parser.add_argument('--podcast-title', type=str, default='BZ PODCAST',
                        help='Podcast title')
    parser.add_argument('--podcast-description', type=str, default='BZ local feed',
                        help='Podcast title')
    args = parser.parse_args()

    now = str(datetime.now())
    items = '\n'.join(
        ITEM.format(title=name,
                    link=HOST.format(name),
                    #date=now,
                    date=get_pubDate(name),
                    size=os.path.getsize(name),
                    duration=get_length(name))
        for name in glob.glob(args.files)
        if get_length(name) != 0)
    feed = BODY.format(items=items, date=now,
                       podcast_title=args.podcast_title,
                       podcast_description=args.podcast_description)
    print(feed)
