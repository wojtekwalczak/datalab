#!/usr/bin/env python
# -*- encoding: utf-8

"""Plot view counts for YouTube playlists."""

__author__ = 'Wojciech Walczak'
__email__ = 'ww(at)tosh.pl'

import os
import sys
import pafy # see: https://github.com/np1/pafy
import matplotlib.pyplot as plt


def cr_results_path():
   results_path = os.path.join('results', sys.argv[0].split('.')[0])
   if not os.path.exists(results_path):
      os.makedirs(results_path)
   return results_path


def get_playlist(playlist_id):
   return pafy.get_playlist(playlist_id)


def get_viewcount(playlist):
   for entry in playlist.get('items', []):
      yield entry['pafy'].viewcount


def get_vid_titles(playlist):
   for entry in playlist.get('items', []):
      yield entry['pafy'].title


def make_plot(save_path, plot_title, viewcounts, xtick_labels):
   fig = plt.figure()
   fig.subplots_adjust(bottom=0.2)
   ax = fig.add_subplot(111)
   ax.plot(viewcounts, linewidth=2.5, marker='D')
   ax.grid(True)
   ax.set_xticks(range(0, len(viewcounts)))
   ax.set_xticklabels(xtick_labels, fontsize=7, rotation=45, ha='right')
   ax.set_title(plot_title)
   ax.set_ylabel(u'Views count')
   plt.savefig(save_path, bbox_inches='tight')


def main(playlist_id):
   print 'Downloading playlist %s...' % (playlist_id)
   pl = get_playlist(playlist_id)
   title = pl.get('title', '')
   author = pl.get('author', '')
   atitle = '%s by %s' % (title, author)
   print 'Got: ', atitle

   save_path = os.path.join(cr_results_path(), '%s.png' % (playlist_id))
   print 'Saving plot to:', save_path
   viewcount = list(get_viewcount(pl))
   xtick_labels = list(get_vid_titles(pl))
   make_plot(save_path, atitle, viewcount, xtick_labels)


if __name__ == '__main__':
   if len(sys.argv) > 1:
      main(sys.argv[1])
   else:
      print 'USAGE: %s <playlist_id>' % (sys.argv[0])
      print 'E.g.: %s PL84A56BC7F4A1F852' % (sys.argv[0])
