#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "smath.h"
#include "spline.h"

using namespace std;

int main(int argc, char *argv[]) {
    vector<FUNCTION *> splines;
    ifstream fileIn("input.txt");

    if (!fileIn.is_open()) return -1;

    while (!fileIn.eof()) {
        int n;
        real x, y;
        vector<POINT> points;

        fileIn >> n;
        for (int i = 0; i < n; i++) {
            fileIn >> x >> y;
            points.push_back({x, y});
        }

        splines.push_back(createFunction(points));
    }
    fileIn.close();

    for (int i = 0; i < (int)splines.size(); ++i) {
        pair<real, real> fSpln_ = takeMinMaxSplineX(splines[i]);
        vector<POINT> splineData =
                buildSplineData(fSpln_.first, fSpln_.second, splines[i]);
        writeSplineInfoFile("func" + to_string(i), splineData);

        if (i != (int)splines.size() - 1) {
            for (int j = i + 1; j < (int)splines.size(); ++j) {
                pair<real, real> sSpln_ = takeMinMaxSplineX(splines[j]);

                real a = fSpln_.first >= sSpln_.first ? fSpln_.first + 0.01
                                                      : sSpln_.first + 0.01;
                real b = fSpln_.second <= sSpln_.second ? fSpln_.second - 0.01
                                                        : sSpln_.second - 0.01;

                real ROOT = checkRoots(a, b, splines[i], splines[j]);
                if (ROOT != nothingRoots) {
                    vector<POINT> point = {{ROOT, splines[i]->getY(ROOT)}};
                    writeSplineInfoFile("point_" + to_string(i) + to_string(j),
                                        point);
                }
                else {
                    cout << "Distance between " + to_string(i) + " and " +
                            to_string(j) + " splines : "
                         << calcMinDistance(0, 10, splines[i], splines[j])
                         << endl;
                }
            }
        }
    }

    return 0;
}