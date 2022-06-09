./create-spline

graphics=$(ls | grep -P -o ".*\.spline")

python3 graph.py "$graphics"

for graphic in $graphics; do rm "$graphic"; done
