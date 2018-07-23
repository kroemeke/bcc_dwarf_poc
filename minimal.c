#include <stdio.h>

struct dupa_s {
  int a;
  int b;
  char buf[90];
  int c;
};

typedef struct dupa_s dupa_t;

int Shee3yie(dupa_t *y) { 
 printf("%d\n",y->c);
 sleep(1);
 return 0;
};

int main() {
  int i = 0;
  for (i=0;i<100;i++) {
    dupa_t *x;
    sprintf(x->buf,"TEST nr : ");
    x->c=i;
    Shee3yie(x);
  }
  return 0;
}
