import os

from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper

tool = GoogleTrendsQueryRun(api_wrapper=GoogleTrendsAPIWrapper())