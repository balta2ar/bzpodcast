#!/bin/sh

TITLE="My RSS entry"
LINK="http://example.com/entry4711"
DATE="`date`"
DESC="Good news"
GUID="http://example.com/entry4711" 

xmlstarlet ed -L   -a "//channel" -t elem -n item -v ""  \
     -s "//item[1]" -t elem -n title -v "$TITLE" \
     -s "//item[1]" -t elem -n link -v "$LINK" \
     -s "//item[1]" -t elem -n pubDate -v "$DATE" \
     -s "//item[1]" -t elem -n description -v "$DESC" \
     -s "//item[1]" -t elem -n guid -v "$GUID" \
     -d "//item[position()>10]" feed.xml ;
