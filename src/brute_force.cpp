#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

// Enumerate every one of the 2^24 clause subsets on four labeled variables.
// Array index is the clause subset, value its exact set of satisfying assignments.
int main(int argc,char**argv){
    int n=argc>1?std::stoi(argv[1]):4;
    if(n<1||n>4)throw std::runtime_error("n must be 1..4");
    std::vector<uint16_t> cm;
    for(int j=1;j<n;j++)for(int i=0;i<j;i++)for(int a=0;a<2;a++)for(int b=0;b<2;b++){
        uint16_t mask=0;
        for(int s=0;s<(1<<n);s++)if(((s>>i)&1)==a||((s>>j)&1)==b)mask|=uint16_t(1)<<s;
        cm.push_back(mask);
    }
    uint32_t total=uint32_t(1)<<cm.size();
    std::vector<uint16_t> sat(total);
    sat[0]=n==4?uint16_t(65535):uint16_t((uint32_t(1)<<(1<<n))-1);
    std::vector<uint64_t> counts(cm.size()+1);counts[0]=1;
    for(uint32_t f=1;f<total;f++){
        sat[f]=sat[f&(f-1)]&cm[__builtin_ctz(f)];
        if(sat[f])++counts[__builtin_popcount(f)];
    }
    std::cout<<"{\"n\":"<<n<<",\"subsets_examined\":"<<total<<",\"counts\":[";
    for(size_t m=0;m<counts.size();m++){if(m)std::cout<<',';std::cout<<counts[m];}
    std::cout<<"]}\n";
}
