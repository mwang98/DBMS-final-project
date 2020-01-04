python3 parser.py -h
python3 parser.py Define -h
python3 parser.py Execute -h
python3 parser.py Stop -h
python3 parser.py Delete -h
python3 parser.py Modify -h
python3 parser.py List -h

python3 parser.py List task
python3 parser.py List test
python3 parser.py Define -task T -test ttest -d D -m M -f F -s 3000
python3 parser.py Execute -task T
python3 parser.py Stop -task T
python3 parser.py Modify -task T -test fft
python3 parser.py Execute -task T
python3 parser.py Delete -task T
python3 parser.py List task
