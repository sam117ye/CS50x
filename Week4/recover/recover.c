#include <stdio.h>
#include <stdlib.h>

#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // correct usage
    if (argc != 2)
    {
        printf("Usage: :/recover IMAGE\n");
        return 1;
    }

    // open file
    FILE *input_file = fopen(argv[1], "r");

    // check if the file is not NULL
    if (input_file == NULL)
    {
        printf("File cannot be opened\n");
        return 2;
    }

    //read file
    unsigned char  buffer[512];

    // look for JPEG beginnings
    int count_image = 0;

    // output image
    FILE *Out_image = NULL;

    // Make a new JPEG
    char *outptr = malloc(8 * sizeof(char));

    while (fread(buffer, sizeof(char), 512, input_file))
    {
        if (buffer[0] == 0xff &&  buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            sprintf (outptr, "%03i.jpg", count_image);

            Out_image = fopen(outptr,"w");

            count_image++;
        }

        if (Out_image != NULL)
        {
            fwrite(buffer, sizeof(char), 512, Out_image);
        }
    }

    //close infile and outfile and free malloc
    free(outptr);

    fclose(Out_image);

    fclose(input_file);

    return 0;
}
