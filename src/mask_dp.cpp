#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>

// No generating-function identities: each clause is skipped or included once.
// Counts are <= C(60,13), so uint64_t suffices for all n<=6 and m<=13.
using Poly=std::array<uint64_t,14>;
struct Hash {
    size_t operator()(uint64_t x) const {
        x+=0x9e3779b97f4a7c15ULL;
        x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;
        x=(x^(x>>27))*0x94d049bb133111ebULL;
        return x^(x>>31);
    }
};
using Map=std::unordered_map<uint64_t,Poly,Hash>;
int main(int argc,char** argv){
    const int n=argc>1?std::stoi(argv[1]):6;
    const int mmax=argc>2?std::stoi(argv[2]):13;
    const size_t cap=argc>3?std::stoull(argv[3]):40000000;
    if(n<1||n>6||mmax<0||mmax>13)throw std::runtime_error("n<=6, m<=13 required");
    const int assignments=1<<n;
    const uint64_t all=n==6?~uint64_t(0):((uint64_t(1)<<assignments)-1);
    std::vector<uint64_t> clauses;
    for(int j=1;j<n;j++)for(int i=0;i<j;i++)for(int a=0;a<2;a++)for(int b=0;b<2;b++){
        uint64_t mask=0;
        for(int s=0;s<assignments;s++)
            if(((s>>i)&1)==a||((s>>j)&1)==b)mask|=uint64_t(1)<<s;
        clauses.push_back(mask);
    }
    Map dp;dp.max_load_factor(0.8);dp[all][0]=1;
    const auto start=std::chrono::steady_clock::now();
    uint64_t rolling_hash=0;
    for(size_t c=0;c<clauses.size();c++){
        // Intersection strictly decreases popcount unless it fixes a mask.
        // Process original states in increasing popcount. All proper-subset
        // destinations have already been processed (or are new); the source
        // polynomial is therefore still its value before this clause.
        // unordered_map node references survive insertion and rehashing.
        std::array<std::vector<Map::value_type*>,65> buckets;
        for(auto& entry:dp)buckets[__builtin_popcountll(entry.first)].push_back(&entry);
        for(auto& bucket:buckets)for(auto* entry:bucket){
            const auto mask=entry->first;
            Poly& p=entry->second;
            const auto dest=mask&clauses[c];
            if(dest==mask){
                for(int k=mmax;k>=1;k--)p[k]+=p[k-1];
            }else if(dest){
                bool nonzero=false;
                for(int k=0;k<mmax;k++)nonzero|=p[k]!=0;
                if(nonzero){
                    Poly& take=dp[dest];
                    for(int k=0;k<mmax;k++)take[k+1]+=p[k];
                }
            }
            if(dp.size()>cap){std::cerr<<"STATE CAP reached at step "<<c+1<<"\n";return 2;}
        }
        uint64_t h=0;
        for(const auto& [mask,p]:dp){
            uint64_t term=Hash{}(mask);
            for(int k=0;k<=mmax;k++)term=Hash{}(term^Hash{}(p[k]+uint64_t(k)));
            h+=term;
        }
        rolling_hash=Hash{}(rolling_hash^h);
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cerr<<"step "<<c+1<<" states "<<dp.size()<<" hash "<<h<<" seconds "<<sec<<"\n";
    }
    Poly total{};
    for(const auto& [mask,p]:dp)for(int k=0;k<=mmax;k++)total[k]+=p[k];
    std::cout<<"{\"n\":"<<n<<",\"m_max\":"<<mmax<<",\"states\":"<<dp.size()<<",\"rolling_hash_u64\":\""<<rolling_hash<<"\",\"counts\":[";
    for(int k=0;k<=mmax;k++){if(k)std::cout<<',';std::cout<<total[k];}
    std::cout<<"]}\n";
}
