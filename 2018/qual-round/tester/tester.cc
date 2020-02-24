#include <bits/stdc++.h>
using namespace std;

#define VERBOSE false

const string INPUT_PATH = "../input/";
const string OUTPUT_PATH = "../output//";
const string BESTOUT_PATH = "../output/best_output/";

int total;
const string INPUT_FILE_NAME[] = {
    "a.in",
    "b.in",
    "c.in",
    "d.in",
    "e.in",
};

vector<int> res;
vector<int> bon_chk;

int ride_cnt;
int b_cnt;

void init() {
    ride_cnt = 0;
    b_cnt = 0;
    res.clear();
    bon_chk.clear();
}

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

int best_score[5];

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
    
    bon_chk.resize(in.N);
    res.resize(in.N);
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
    int M;
    while (out_read >> M) {
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
    int idle_sum = 0;
    int wait_sum = 0;
    for (int num : ride) {
        int ans = 0;
        auto next = in.ride[num];
        bool bonus = false;
        // 시작 이동
        int before_T = T;
        move(T, x, y, next.a, next.b);
        idle_sum += T - before_T;


        before_T = T;
        // 기다리기
        wait(T, next.s);
        wait_sum += T - before_T;

        if (T == next.s) {
            ans += in.B;
            bonus = true;
        }

        // 도착 이동
        move(T, x, y, next.x, next.y);
        ans += diff(next.a, next.b, next.x, next.y);
        if (T > next.f) 
            continue;
        if (T > in.T) break;
        if (bonus) {
            bon_chk[num] = true;
            b_cnt++;
        }
        res[num] = 1;
        ride_cnt++;
        ret += ans;
    }

    if (VERBOSE) {
        cout << ret << "손님수: " << ride.size() << " 유휴 이동: " << idle_sum << " 기다림: " << wait_sum << '\n';
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

void revise_summary() {
    string path = BESTOUT_PATH + "summary";
    ofstream read;
    read.open(path.c_str());
    int tot = 0;
    for (int i = 0; i < 5; i++) {
        tot += best_score[i];
        read << best_score[i] << '\n';
    }
    read << tot << " <- total score";
}


void check_summary() {
    string path = BESTOUT_PATH + "summary";
    ifstream read;
    read.open(path.c_str());
    if (!read) {
        //cout << path << " does not exist\n";
        revise_summary();
    }

    for (int i = 0; i < 5; i++) {
        read >> best_score[i];
    }
}

void revise_best(score_t& score, char c, int ans) {
    if (best_score[c-'a'] > ans) return ;

    best_score[c-'a'] = ans;
    string to_path = BESTOUT_PATH + c + ".out";

    ofstream bout;
    bout.open(to_path.c_str());

    for (auto output : score.output) {
        bout << output.size();
        for (auto num : output) {
            bout << ' ' << num;
        }
        //if (output == score.output.back())
        bout << '\n';
    }
}

void run(char c) {
    if (!check_output(c)) return ;

    score_t score;
    auto& in = score.input;
    read_input(in, c);
    read_output(score, c);

    int ans = calc_ans(score);
    revise_best(score, c, ans);

    total += ans;
    cout << c << ": " << ans;
    if (VERBOSE) {
        cout << " 총 손님: "  << in.N << " 잘 태운 손님: " << ride_cnt << " 보너스: " << b_cnt << '\n';
    }
    cout << endl;
    if (!VERBOSE) return ;
    vector<int> dist;
    for (int i = 0; i < in.N; i++)
    {
        if (res[i] == 0)
        {
            auto r = in.ride[i];
            dist.push_back(diff(r.a, r.b, r.x, r.y));
        }
    }
    sort(dist.begin(), dist.end());
    int cnt = 0;
    reverse(dist.begin(), dist.end());
    for (int d : dist)
    {
        cout << d << '\n';
        cnt++;
        if (cnt == 100)
            break;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    check_summary();
    for (char i = 'a'; i <= 'e'; i++) {
        init();
        run(i);
    }
    cout << "total: " << total << '\n';
    revise_summary();

    return 0;
}
