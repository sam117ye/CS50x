#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt the user for the pyramid's height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8 );

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n -i - 1; j++)  
        {
            printf(" ");
        }
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}

