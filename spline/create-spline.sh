info="""
  ----------------------------------------------------

  Build your splines from file with points
  and find theirs intersection points.

  Pass a file with points, where the number
  of points is indicated first, and then the points in
  XY a space-separated format.

  > create-spline input.txt

  Example, where one point with coordinates = (2, 3).
  1
  2 3

  ----------------------------------------------------
"""

echo "$info"

if [ ${#1} -eq 0 ]; then
  echo "create-spline: empty data!"
  exit
fi

path=$(readlink -f "$1")

python3 validator.py "$path"
if [ $? -eq 255 ]; then
  echo "create-spline: invalid data!"
  exit
fi

./spline "$path"
if [ $? -ne 0 ]; then
  echo "create-spline: fatal spline build!"
  exit
fi

graphics=$(ls | grep -P -o ".*\.spline")

python3 graph.py "$graphics"

for graphic in $graphics; do rm "$graphic"; done
