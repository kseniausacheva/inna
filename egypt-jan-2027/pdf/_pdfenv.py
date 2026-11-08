"""Импортируй это первым: убирает из sys.path системные dist-packages Python 3.13,
которые ломают cryptography и, через неё, pypdf в нашем Python 3.11."""
import sys
sys.path[:] = [p for p in sys.path if 'python3/dist-packages' not in p]
