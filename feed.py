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
from datetime import datetime
from mutagen.mp3 import MP3


BODY = '''<?xml version="1.0" encoding="utf-8"?>
 <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
 <channel>
 <atom:link href="http://192.168.1.2/feed.xml" rel="self" type="application/rss+xml" />
     <title>BZ PODCAST</title>
     <link>http://192.168.1.2</link>
     <description>BZ local feed</description>
     <lastBuildDate>{date}</lastBuildDate>
     <language>en-us</language>
     <copyright>Copyright 2010 © WHOEVER</copyright>
     <itunes:subtitle>BZ local feed</itunes:subtitle>
     <itunes:author>BZ</itunes:author>
     <itunes:summary>BZ local feed</itunes:summary>
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


if __name__ == '__main__':
    now = str(datetime.now())
    items = '\n'.join(
        ITEM.format(title=name,
                    link=HOST.format(name),
                    date=now,
                    size=os.path.getsize(name),
                    duration=int(MP3(name).info.length))
        for name in glob.glob('*.mp3'))
    feed = BODY.format(items=items, date=now)
    print(feed)
