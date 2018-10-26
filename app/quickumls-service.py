#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

'''
quickumls_service.py
~~~~~~~~~~~~~~~~~~~~

App wraps quickumls as a tcp service.

'''

import os
import sys
import warnings

import json
from quickumls import QuickUMLS
import constants

if (os.environ.get('GRPC','false')=='true'):
    from springcloudstream.grpc.stream import Processor
else:
    from springcloudstream.tcp.stream import Processor

warnings.filterwarnings("ignore")

quickumls_fp = os.environ.get('QUICKUMUMLS_FP', "/data/quickumlsdb")
overlapping_criteria = os.environ.get('OVERLAPPING_CRITERIA', "score")
threshold = os.environ.get('THRESHOLD', 0.7)
similarity_name = os.environ.get('SIMILARITY_NAME', "jaccard")
window = os.environ.get('WINDOW', 5)
min_match_length = os.environ.get('MIN_MATCH_LENGTH', 3)
verbose = os.environ.get('VERBOSE', False)

accepted_semtypes = os.environ.get('ACCEPTED_SEMTYPES', constants.ACCEPTED_SEMTYPES)

print("quickumls_fp={}, overlapping_criteria={}, threshold={}, similarity_name={}, window={}, accepted_semtypes={}"
      .format(quickumls_fp, overlapping_criteria, threshold, similarity_name, window, accepted_semtypes))

matcher = QuickUMLS(quickumls_fp, overlapping_criteria, threshold, window, similarity_name, min_match_length, accepted_semtypes, verbose)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def process(data):
    dto = json.loads(str(data))
    text = dto['text']
    matches = matcher.match(text, best_match=True, ignore_syntax=True)
    return json.dumps(matches, cls=SetEncoder) + '\r\n'


Processor(process, sys.argv).start()