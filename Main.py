#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    print ('Hello world!')
    with open('/Users/timotheeaupetit/Music/iTunes/iTunes Music Library.xml', 'r') as f:
        print (f.read())


if __name__ == '__main__':
    main()
