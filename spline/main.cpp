#include <fstream>
#include <iostream>
#include <vector>

#include "smath.h"
#include "spline.h"

using namespace std;

int main(int argc, char *argv[]) {
    vector<FUNCTION *> splines;
    ifstream fileIn(argv[0]);

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

    for (int i = 0; i < (int)splines.size() - 1; ++i) {
        pair<real, real> fSpln_ = takeMinMaxSplineX(splines[i]);
        vector<POINT> splineData =
                buildSplineData(fSpln_.first, fSpln_.second, splines[i]);
        writeSplineInfoFile("name", splineData);

        for (int j = i + 1; j < (int)splines.size(); ++j) {
            pair<real, real> sSpln_ = takeMinMaxSplineX(splines[i]);
            real ROOT = checkRoots(
                    fSpln_.first >= sSpln_.first ? fSpln_.first : sSpln_.first,
                    fSpln_.second <= sSpln_.second ? fSpln_.second : sSpln_.second,
                    splines[i], splines[j]);
            if (ROOT != nothingRoots) {
                vector<POINT> point = {{ROOT, splines[i]->getY(ROOT)}};
                writeSplineInfoFile("name", point);
            } else {
                cout << "Nothing roots, min distance: "
                     << calcMinDistance(0, 10, splines[i], splines[j]);
            }
        }
    }

    return 0;
}