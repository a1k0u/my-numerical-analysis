#include <iostream>
#include <vector>

#include "spline.h"

using namespace std;

int main() {
    vector<POINT> st = {{0, 1}, {2, 10}, {4, -5}, {6, 0}, {8, 11}, {10, 3}};

    FUNCTION* func1 = createFunction(st);
    double start = 0, stop = 10, step = 0.5;
    while (start != stop) {
        cout << "x=" << start << ", y=" << func1->getY(start) << endl;
        start += step;
    }

    return 0;
}