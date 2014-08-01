// @file: src/realtype.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Contributors:
//   Korepwx              <public@korepwx.com>
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// This file is distributed under two-clause BSD license.

#include <time.h>
#include "realtype.h"

#define NN 312
#define MM 156
#define MATRIX_A 0xB5026F5AA96619E9ULL
#define UM 0xFFFFFFFF80000000ULL /* Most significant 33 bits */
#define LM 0x7FFFFFFFULL /* Least significant 31 bits */


struct RandomGenerator::Private
{
  /* The array for the state vector */
  unsigned long long mt[NN];
  int mti;

  // Constructor & Destructor
  Private() : mti(NN+1)
  {
  }
  
  // Construct the random generator by a given seed
  Private(unsigned long long seed) : mti(NN+1)
  {
    init_genrand64(seed);
  }
  
  /* initializes mt[NN] with a seed */
  void init_genrand64(unsigned long long seed)
  {
    mt[0] = seed;
    for (mti=1; mti<NN; mti++)
      mt[mti] =  (6364136223846793005ULL * (mt[mti-1] ^ (mt[mti-1] >> 62)) + mti);
  }
  
  /* generates a random number on [0, 2^64-1]-interval */
  unsigned long long genrand64_int64(void)
  {
    int i;
    unsigned long long x;
    static unsigned long long mag01[2]={0ULL, MATRIX_A};
    
    if (mti >= NN) { /* generate NN words at one time */
      
      /* if init_genrand64() has not been called, */
      /* a default initial seed is used     */
      if (mti == NN+1)
        init_genrand64(5489ULL);
      
      for (i=0;i<NN-MM;i++) {
        x = (mt[i]&UM)|(mt[i+1]&LM);
        mt[i] = mt[i+MM] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
      }
      for (;i<NN-1;i++) {
        x = (mt[i]&UM)|(mt[i+1]&LM);
        mt[i] = mt[i+(MM-NN)] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
      }
      x = (mt[NN-1]&UM)|(mt[0]&LM);
      mt[NN-1] = mt[MM-1] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
      
      mti = 0;
    }
    
    x = mt[mti++];
    
    x ^= (x >> 29) & 0x5555555555555555ULL;
    x ^= (x << 17) & 0x71D67FFFEDA60000ULL;
    x ^= (x << 37) & 0xFFF7EEE000000000ULL;
    x ^= (x >> 43);
    
    return x;
  }
  
  /* generates a random number on [0, 2^63-1]-interval */
  long long genrand64_int63(void)
  {
    return (long long)(genrand64_int64() >> 1);
  }
  
  /* generates a random number on [0,1]-real-interval */
  double genrand64_real1(void)
  {
    return (genrand64_int64() >> 11) * (1.0/9007199254740991.0);
  }
  
  /* generates a random number on [0,1)-real-interval */
  double genrand64_real2(void)
  {
    return (genrand64_int64() >> 11) * (1.0/9007199254740992.0);
  }
  
  /* generates a random number on (0,1)-real-interval */
  double genrand64_real3(void)
  {
    return ((genrand64_int64() >> 12) + 0.5) * (1.0/4503599627370496.0);
  }
};

RandomGenerator::RandomGenerator()
: d_(new Private())
{
}

RandomGenerator::RandomGenerator(unsigned long long seed)
: d_(new Private(seed))
{
}

RandomGenerator::~RandomGenerator()
{
  delete d_;
}

Real RandomGenerator::operator()() {
  return d_->genrand64_real2();
}
