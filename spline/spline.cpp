#include <cmath>
#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include "spline.h"

using namespace std;

long double getH_(vector<POINT>& staticPoints, int index) {
    if (!index)
        index++;
    return staticPoints[index].x - staticPoints[index - 1].x;
}

CONTAINER getRatios_(vector<POINT>& staticPoints, int index) {
    CONTAINER container{};
    container.F = (staticPoints[index + 1].y - staticPoints[index].y) /
                  getH_(staticPoints, index + 1) -
                  staticPoints[index].y / getH_(staticPoints, index);

    if (index > 0)
        container.F +=
                (staticPoints.at(index - 1).y) / getH_(staticPoints, index);

    container.A = getH_(staticPoints, index) / 6;
    container.B =
            (getH_(staticPoints, index) + getH_(staticPoints, index + 1)) / 3;
    container.C = getH_(staticPoints, index + 1) / 6;
    return container;
}

long double getAlpha_(vector<POINT>& staticPoints, int index) {
    CONTAINER container{};
    container = getRatios_(staticPoints, index - 1);

    if (index == 1)
        return (-container.C) / container.B;

    return (-container.C) /
           (container.A * getAlpha_(staticPoints, index - 1) + container.B);
}

long double getBeta_(vector<POINT>& staticPoints, int index) {
    CONTAINER container{};
    container = getRatios_(staticPoints, index - 1);

    if (index == 1)
        return container.F / container.B;

    return (container.F - container.A * getBeta_(staticPoints, index - 1)) /
           (container.A * getAlpha_(staticPoints, index - 1) + container.B);
}

long double getGamma_(vector<POINT>& staticPoints,
                      vector<long double>& gammas,
                      int index) {
    if (!index || index == staticPoints.size() - 1)
        return 0;

    if (index == 1 || index == staticPoints.size() - 2) {
        CONTAINER container = getRatios_(staticPoints, index);

        return (container.F - container.A * getBeta_(staticPoints, index)) /
               (container.A * getAlpha_(staticPoints, index) + container.B);
    }

    long double nextGamma;
    if (gammas[index + 1] != GARBAGE)
        nextGamma = gammas[index + 1];
    else
        nextGamma = getGamma_(staticPoints, gammas, index + 1);

    long double value = getAlpha_(staticPoints, index + 1) * nextGamma +
                        getBeta_(staticPoints, index + 1);

    gammas[index] = value;

    return value;
}

void getGammaValues(vector<POINT>& staticPoints, vector<long double>& gammas) {
    for (int i = 0; i < (int)gammas.size(); ++i)
        if (gammas[i] == GARBAGE)
            gammas[i] = getGamma_(staticPoints, gammas, i);
}

POINT getSplinePoint(vector<POINT>& staticPoints,
                     vector<long double>& gammas,
                     long double x) {
    int index = -1;
    for (int i = 0; i < (int)staticPoints.size() - 1; ++i) {
        if (staticPoints[i].x <= x && x <= staticPoints[i + 1].x) {
            index = i;
            break;
        }
    }

    if (index == -1)
        return POINT {GARBAGE, GARBAGE};

    long double A, B, C, D, X_i_1, X_i, H;

    X_i_1 = staticPoints[index + 1].x;
    X_i   = staticPoints[index].x;
    H     = getH_(staticPoints, index + 1);

    A = (X_i_1 - x) / H;
    B = (x - X_i) / H;
    C = (powl(X_i_1 - x, 3) - powl(H, 2) * (X_i_1 - x)) / (6 * H);
    D = (powl(x - X_i, 3) - powl(H, 2) * (x - X_i)) / (6 * H);

    long double Y_i_1, Y_i, G_i_1, G_i;

    Y_i_1 = staticPoints[index + 1].y;
    Y_i   = staticPoints[index].y;
    G_i_1 = gammas[index + 1];
    G_i   = gammas[index];

    POINT result = {0, 0};
    result.x = x;
    result.y = Y_i * A + Y_i_1 * B + G_i * C + G_i_1 * D;

    return result;
}

bool pointCompare_(const POINT& one, const POINT& two) {
    return one.x < two.x;
}

FUNCTION* createFunction(vector<POINT>& staticPoints) {
    auto* func = new FUNCTION;

    int n = (int)staticPoints.size();
    func->staticPoints.resize(n);
    func->gammas.resize(n, GARBAGE);

    for (int i = 0; i < n; ++i)
        func->staticPoints[i] = staticPoints[i];
    sort(func->staticPoints.begin(), func->staticPoints.end(), &pointCompare_);
    getGammaValues(func->staticPoints, func->gammas);

    return func;
}

pair<long double, long double> takeMinMaxSplineX(FUNCTION* function) {
    return {function->staticPoints[0].x, function->staticPoints.back().x};
}

vector<POINT> buildSplineData(long double start, long double stop, FUNCTION* function) {
    vector<POINT> functionPoints;
    double step = 0.5;
    while (start != stop) {
        functionPoints.push_back(
                {start, function->getY(start)}
        );
        start += step;
    }

    return functionPoints;
}

void writeSplineInfoFile(const string& name, vector<POINT>& points) {
    string fileName = name + ".spline";
    ofstream fileOut;
    fileOut.open(fileName);
    for (POINT point : points)
        fileOut << point.x << " " << point.y << endl;
    fileOut.close();
}
