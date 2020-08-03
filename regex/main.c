#include <stdio.h>
#include <regex.h>

#define MAX_MATCHES 1

void match(regex_t *pexp, char *sz)
{
    regmatch_t matches[MAX_MATCHES]; //A list of the matches in the string (a list of 1)
    //Compare the string to the expression
    //regexec() returns 0 on match, otherwise REG_NOMATCH
    if (regexec(pexp, sz, MAX_MATCHES, matches, 0) == 0)
    {
        printf("\"%s\" matches characters %d - %d\n", sz, matches[0].rm_so, matches[0].rm_eo);
    }
    else
    {
        printf("\"%s\" does not match\n", sz);
    }
}

int main()
{
    int rv;
    regex_t exp;
    //REG_EXTENDED is so that we can use Extended regular expressions
    rv = regcomp(&exp, "^((95|97|98|99|59|58)\[0-9]{5})$", REG_EXTENDED);
    if (rv != 0)
    {
        printf("regcomp failed with %d\n", rv);
    }
    //Run a test on it
    match(&exp, "5928127");
    match(&exp, "9912349");
    match(&exp, "3503316");
    //Free it
    regfree(&exp);

    return 0;
}
