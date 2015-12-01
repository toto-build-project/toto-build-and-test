//
//  main.cpp
//  ceng test
//

#include <iostream>
#include <stdio.h>
#include <stdlib.h>


#define SECRET1 0x44
#define SECRET2 0x55

int main(int argc, char *argv[])
{
    char user_input[100];
    int *secret;
    int int_input;
    int a, b, c, d;
    
    /* allocating size for a */
    a = (int *) malloc(20000*sizeof(int));
    secret = (int *) malloc(2*sizeof(int));
    
    /* getting the secret */
    secret[0] = SECRET1; secret[1] = SECRET2;
    

  while (1) {
    printf("The variable secret's address is 0x%8x|%d (on stack)\n", &secret), &secret;
    printf("The variable secret's value is 0x%8x|%d (on heap)\n", secret, secret);
    printf("secret[0]'s address is 0x%8x|%d  (on heap)\n", &secret[0], &secret[0]);
    printf("secret[1]'s address is 0x%8x|%d  (on heap)\n", &secret[1], &secret[1]);
    printf("The user_input address is 0x%8x|%d  (on stack) \n", &user_input, &user_input);
    printf("The int_input address is 0x%8x|%d (on stack)\n", &int_input, &int_input);

    printf("Please enter a decimal integer\n");
    scanf("%d", &int_input);  

    printf("Please enter a string\n");
    scanf("%s", user_input); /* getting a string from user */
    
    /* Vulnerable place */
    printf(user_input);
    printf("\n");
    
    /* Verify whether your attack is successful */
    printf("The original secrets: 0x%x -- 0x%x\n", SECRET1, SECRET2);
    printf("The new secrets:      0x%x -- 0x%x\n", secret[0], secret[1]);

  }
  return 0;
}
