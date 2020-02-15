#include <bits/stdc++.h>
using namespace std;

const string INPUT_PATH = "../input/";
const string OUTPUT_PATH = "../output/tester/";


int total;
const string INPUT_FILE_NAME[] = {
    "a.in",
    "b.in",
    "c.in",
    "d.in",
    "e.in",
};

struct ride_t {
    int a; // start row
    int b; // start column
    int x; // finish row
    int y; // finish column
    int s; // earliest start
    int f; // latest column
};

struct input_t {
    int R; // Row
    int C; // Column 
    int F; // Number of Vehicles in the Fleet
    int N; // Number of Rides
    int B; // Bonus
    int T; // Number of Steps
    vector<ride_t> ride;
};

// 하나의 파일 채점
struct score_t {
    input_t input;
    vector<vector<int> > output;
};

bool check_output(char c) {
    string path = OUTPUT_PATH + c + ".out";
    ifstream out_read;
    out_read.open(path.c_str());

    if (!out_read) {
        cout << path << " does not exist\n";
        return false;
    }

    return true;
}

void read_input(input_t& in, char c) {
    string path = INPUT_PATH + c + ".in";
    ifstream in_read;
    
    in_read.open(path.c_str());

    if (!in_read) {
        cout << path << " does not exist\n";
        return ;
    }

    in_read >> in.R >> in.C >> in.F >> in.N >> in.B >> in.T;
    
    for (int i = 0; i < in.N; i++) {
        int a, b, x, y, s, f;
        in_read >> a >> b >> x >> y >> s >> f;
        in.ride.push_back({a, b, x, y, s, f});
    }
}

void read_output(score_t& score, char c) {
    string path = OUTPUT_PATH + c + ".out";
    ifstream out_read;
    out_read.open(path.c_str());

    vector<bool> check(score.input.N, false);

    int line_cnt = 0;
    while (!out_read.eof()) {
        int M; out_read >> M;
        vector<int> v;
        while (M--) {
            int R; 
            out_read >> R;
            assert(0 <= R && R < score.input.N);
            assert(!check[R] || "승객은 한번씩만 태워야 함");
            check[R] = true;
            v.push_back(R);
        }
        score.output.push_back(v);
        line_cnt++;
    }
    assert(line_cnt == score.input.F);
}

int diff(int x, int y, int nx, int ny) {
    return abs(nx - x) + abs(ny - y);
}
void move(int& T, int& x, int& y, int nx, int ny) {
    int d = diff(x, y, nx, ny);
    T += d;
    x = nx;
    y = ny;
}

void wait(int& T, int w) {
    if (T >= w) return;
    T = w;
}
int calc_vehicle(input_t& in, vector<int> ride) {
    int T = 0;
    int x = 0;
    int y = 0;

    int ret = 0;
    for (int num : ride) {
        int ans = 0;
        auto next = in.ride[num];
        // 시작 이동
        move(T, x, y, next.a, next.b);
        // 기다리기
        wait(T, next.s);
        if (T == next.s)
            ans += in.B;

        // 도착 이동
        move(T, x, y, next.x, next.y);
        ans += diff(next.a, next.b, next.x, next.y);
        if (T > next.f) continue;
        if (T > in.T) break;
        ret += ans;
    }
    return ret;
}

int calc_ans(score_t& score) {
    int ret = 0;

    auto& in = score.input;
    auto& out = score.output;

    for (auto ride : out) {
        ret += calc_vehicle(in, ride);
    }
    return ret;
}

void run(char c) {
    if (!check_output(c)) return ;

    score_t score;
    read_input(score.input, c);
    read_output(score, c);

    int ans = calc_ans(score);
    total += ans;
    cout << c << ": " << ans << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    for (char i = 'a'; i <= 'e'; i++) {
        run(i);
    }
    cout << "total: " << total << '\n';
    return 0;
}