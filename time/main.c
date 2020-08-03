#include <stdio.h>
#include <math.h>
#include <time.h>

int main()
{
    char strtime[20];
    
    long timestamp = 1596141304000;     //Unix Timestamp
    timestamp = timestamp / pow(10, 3); //1596141304|000
    
    time_t t = timestamp;
    strftime(strtime, sizeof strtime, "%d/%m/%Y %H:%M:%S", localtime(&t));
    
    printf("%ld\n", timestamp);
    printf("%s\n", ctime(&t));
    printf("%s\n", strtime);

    return 0;
}
