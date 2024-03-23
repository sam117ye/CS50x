// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

 // declare functions from load
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    hash_value = hash(word);
    node *cursor = table[hash_value];

    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0 )
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *infile = fopen (dictionary, "r");

    if(infile == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }

    char word[LENGTH+1];

    while (fscanf(infile, "%s", word) != EOF)
    {
         node *n = malloc(sizeof(node));

           if (n == NULL)
           {
              return false;
           }
           // copy string
           strcpy(n->word, word);

           // make a link chain
           hash_value = hash(word);
           n->next = table[hash_value];
           table[hash_value] = n;
           word_count++;
    }
    fclose(infile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if(word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while(cursor)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
