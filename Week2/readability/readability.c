#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Declare function
int calc_letter(string text);
int calc_index(int letter, int word, int sentence);

int main(void)
{
    // Promt user for text

    string text = get_string(" Text: ");

    // initialization

    int sentence = 0;
    int word = 1;
    int letter = calc_letter(text);

    // calculate sentence and word

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '?' || text[i] == '.' || text[i] == '!')
        {
            sentence++;
        }
        else if (text[i] == ' ')
        {
            word++;
        }
    }

    int result = calc_index(letter, word, sentence);

    // Print grade level
    if (result < 1)
    {
        printf("Before Grade 1\n");
    }
    if (result >= 1 && result <= 16)
    {
        printf("Grade %d\n", result);
    }
    else if (result > 16)
    {
        printf("Grade 16+\n");
    }
}

// Define function
int calc_letter(string text)
{
    // calculate number of letter
    int letter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {

        if (isalpha(text[i]))
        {
            letter++;
        }
    }
    return letter;
}

int calc_index(int letter, int word, int sentence)
{
    float L = (float) letter / word * 100;
    float S = (float) sentence / word * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    return index;
}
