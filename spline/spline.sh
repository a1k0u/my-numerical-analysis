

graphics=$(ls | grep -P -o ".*\.spline")
python3 graph.py "$graphics"
