#include <bits/stdc++.h>
using namespace std;

#define VERBOSE false

const string INPUT_PATH = "../../input/";
const string OUTPUT_PATH = "../../output/pser/";

vector<list<int>> ans;

struct ride_t
{
    int a; // start row
    int b; // start column
    int x; // finish row
    int y; // finish column
    int s; // earliest start
    int f; // latest column
    int idx; // index
};

struct input_t
{
    int R; // Row
    int C; // Column
    int F; // Number of Vehicles in the Fleet
    int N; // Number of Rides
    int B; // Bonus
    int T; // Number of Steps
    vector<ride_t> ride;
};

int diff(int x, int y, int nx, int ny)
{
    return abs(nx - x) + abs(ny - y);
}

int diff(ride_t a) {
    return diff(a.a, a.b, a.x, a.y);
}

void read_input(input_t &in, char c)
{
    string path = INPUT_PATH + c + ".in";
    ifstream in_read;

    in_read.open(path.c_str());

    if (!in_read)
    {
        cout << path << " does not exist\n";
        return;
    }

    in_read >> in.R >> in.C >> in.F >> in.N >> in.B >> in.T;
    ans.resize(in.F);
    for (int i = 0; i < in.N; i++)
    {
        int a, b, x, y, s, f;
        in_read >> a >> b >> x >> y >> s >> f;
        in.ride.push_back({a, b, x, y, s, f, i});
    }
}

void move(int &T, int &x, int &y, int nx, int ny)
{
    int d = diff(x, y, nx, ny);
    T += d;
    x = nx;
    y = ny;
}

void wait(int &T, int w)
{
    if (T >= w)
        return;
    T = w;
}

int check(const input_t& in, int x, int y, const ride_t& r, int T) {
    move(T, x, y, r.a, r.b);
    wait(T, r.s);
    move(T, x, y, r.x, r.y);
    if (T > r.f) return 0;
    return T;
}

void make_order(const input_t& in, const ride_t& r) {
    for (list<int>& l : ans) {
        int x = 0, y = 0, T = 0;

        for (auto it = l.begin(); it != l.end(); it++) {
            // 낀다음에
            int ret = check(in, x, y, r, T);
            cout << [] << '\n';
            if (ret != 0 || ret <= in.ride[*it].s - diff(r.x, r.y, in.ride[*it].a, in.ride[*it].b)) {
                l.insert(it, r.idx);
                return ;
            }
            T = check(in, x, y, in.ride[*it], T);
        }
        int ret = check(in, x, y, r, T);
        if (ret == 0 || ret > in.T) continue;
        l.push_back(r.idx);
        return ;
    }
}

void run(char c)
{
    input_t in;
    read_input(in, c);
    sort(in.ride.begin(), in.ride.end(), [](ride_t a, ride_t b) {
        return diff(a) > diff(b);
    });
    for (auto r : in.ride) {
        make_order(in, r);
    }
    
    string path = OUTPUT_PATH + c + ".out";
    ofstream out_read;
    out_read.open(path.c_str());

    for (auto l : ans) {
        out_read << l.size();
        for (int i : l) {
            out_read << ' ' << i;
        }
        out_read << '\n';
    }
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    run('d');

    return 0;
}