#include <bits/stdc++.h>
using namespace std;

const string INPUT_PATH = "../input/";
const string OUTPUT_PATH = "../output/queued/";
const string BESTOUT_PATH = "../output/best_output/";
const string INPUT_FILE_NAME[] = {
    "a.in",
    "b.in",
    "c.in",
    "d.in",
    "e.in",
    "f.in",
};

int total;
int best_score[6];

struct input_t
{
    // number of book;
    int B;
    // number of libraries
    int L;
    // number of days
    int D;
    // score of books
    vector<int> scores;
    struct lib_t
    {
        // number of books in library
        int N;
        // sign up preocess
        int T;
        // per day
        int M;
        // books in the library
        vector<int> ids;
    };
    vector<lib_t> libs;
};

struct output_t
{
    int A;
    struct lib_t
    {
        int Y;
        int K;
        vector<int> ids;
    };
    vector<lib_t> libs;
};

void init()
{
    total = 0;
}

bool check_output(char c)
{
    string path = OUTPUT_PATH + c + ".out";
    ifstream out_read;
    out_read.open(path.c_str());

    if (!out_read)
    {
        cout << path << " does not exist\n";
        return false;
    }

    return true;
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

    in_read >> in.B >> in.L >> in.D;

    in.scores.resize(in.B);
    in.libs.resize(in.L);
    for (int i = 0; i < in.B; i++)
    {
        in_read >> in.scores[i];
    }

    for (int i = 0; i < in.L; i++)
    {
        auto &lib = in.libs[i];
        in_read >> lib.N >> lib.T >> lib.M;
        lib.ids.resize(lib.N);

        for (int j = 0; j < lib.N; j++)
        {
            in_read >> lib.ids[j];
        }
    }
}

void read_output(output_t &out, char c)
{
    string path = OUTPUT_PATH + c + ".out";
    ifstream out_read;
    out_read.open(path.c_str());

    out_read >> out.A;
    out.libs.resize(out.A);
    for (int i = 0; i < out.A; i++)
    {
        auto &lib = out.libs[i];
        out_read >> lib.Y >> lib.K;
        //cout << lib.Y << ' ' << lib.K << '\n';
        lib.ids.resize(lib.K);
        for (int j = 0; j < lib.K; j++)
        {
            out_read >> lib.ids[j];
        }
    }
}

int calc_ans(input_t &in, output_t &out)
{
    int A = out.A;
    int base_T = 0;
    int ret = 0;
    int cnt = 0;
    int cnt2 = 0;
    vector<bool> check(in.B, false);
    for (int a = 0; a < A; a++)
    {
        auto olib = out.libs[a];
        int Y = olib.Y;
        int K = olib.K;

        auto ilib = in.libs[Y];
        base_T += ilib.T;
        int now_T = base_T;
        for (int k = 0; k < K; k++)
        {
            if (k % ilib.M == 0)
            {
                if (++now_T > in.D)
                    break;
            }
            if (!check[olib.ids[k]])
                check[olib.ids[k]] = true;
            else
                cnt++;
        }
    }
    for (int i = 0; i < in.B; i++)
    {
        if (check[i])
        {
            ret += in.scores[i];
        }
        else
        {
            cnt2++;
        }
    }
    return ret;
}

void revise_best(output_t &out, char c, int ans)
{
    if (best_score[c - 'a'] > ans)
        return;

    best_score[c - 'a'] = ans;
    string to_path = BESTOUT_PATH + c + ".out";

    ofstream bout;
    bout.open(to_path.c_str());

    // output 출력
    bout << out.A << '\n';
    for (auto lib : out.libs)
    {
        bout << lib.Y << ' ' << lib.K << '\n';
        for (auto i : lib.ids)
        {
            bout << i << ' ';
        }
        bout << '\n';
    }
}

void revise_summary()
{
    string path = BESTOUT_PATH + "summary";
    ofstream read;
    read.open(path.c_str());
    int tot = 0;
    for (int i = 0; i < 6; i++)
    {
        tot += best_score[i];
        read << best_score[i] << '\n';
    }
    read << tot << " <- total score";
    cout << "best_sum: " << tot << '\n';
}

void check_summary()
{
    string path = BESTOUT_PATH + "summary";
    ifstream read;
    read.open(path.c_str());
    if (!read)
    {
        //cout << path << " does not exist\n";
        revise_summary();
    }

    for (int i = 0; i < 6; i++)
    {
        read >> best_score[i];
    }
}

void run(char c)
{
    if (!check_output(c))
        return;

    input_t in;
    output_t out;
    read_input(in, c);
    read_output(out, c);

    int mx_iter = 1000;
    while (t--) {
    
    }
    int ans = calc_ans(in, out);
    
    revise_best(out, c, ans);

    total += ans;
    cout << c << ": " << ans << '\n';
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    check_summary();
    for (char i = 'a'; i <= 'f'; i++)
    {
        init();
        run(i);
    }
    revise_summary();

    return 0;
}
