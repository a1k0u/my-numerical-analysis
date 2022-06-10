#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "src/smath.h"
#include "src/spline.h"

using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 2)
        exit(-1);

    vector<FUNCTION *> splines;
    ifstream fileIn(argv[1]);

    if (!fileIn.is_open()) exit(-1);

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

                real a = fSpln_.first >= sSpln_.first ? fSpln_.first
                                                      : sSpln_.first;
                real b = fSpln_.second <= sSpln_.second ? fSpln_.second
                                                        : sSpln_.second;

                real ROOT = checkRoots(a + 0.1, b - 0.1, splines[i], splines[j]);
                if (ROOT != nothingRoots) {
                    vector<POINT> point = {{ROOT, splines[i]->getY(ROOT)}};
                    writeSplineInfoFile("point_" + to_string(i) + to_string(j),
                                        point);
                }
                else {
                    cout << "Distance between " + to_string(i) + " and " +
                            to_string(j) + " splines : "
                         << calcMinDistance(fSpln_.first + sSpln_.first - a,
                                            fSpln_.second + sSpln_.second - b,
                                            splines[i], splines[j])
                         << endl;
                }
            }
        }
    }

    return 0;
}