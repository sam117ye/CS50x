#include "helpers.h"
#include "math.h"

#define RED_COLOR 0
#define GREEN_COLOR 1
#define BLUE_COLOR 2
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for( int row = 0; row < width; row++)
    {
        for( int column = 0; column < height; column++)
        {
            int rgbtgray =round((image[column][row].rgbtBlue + image[column][row].rgbtGreen + image[column][row].rgbtRed) / 3.0);

            image[column][row].rgbtBlue = rgbtgray;
            image[column][row].rgbtGreen = rgbtgray;
            image[column][row].rgbtRed = rgbtgray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for( int row = 0; row < width; row++)
    {
        for( int column = 0; column < height; column++)
        {
            int Blue = round(.272 * image[column][row].rgbtRed + .534 * image[column][row].rgbtGreen + .131 * image[column][row].rgbtBlue);
            int Green = round(.349 * image[column][row].rgbtRed + .686 * image[column][row].rgbtGreen + .168 * image[column][row].rgbtBlue);
            int Red = round(.393 * image[column][row].rgbtRed + .769 * image[column][row].rgbtGreen + .189 * image[column][row].rgbtBlue);

            image[column][row].rgbtBlue = fmin(255,Blue);
            image[column][row].rgbtGreen = fmin(255,Green);
            image[column][row].rgbtRed = fmin(255,Red);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reflectblue;
    for( int row = 0; row < height; row++)
    {
        for( int column = 0; column < width / 2; column++)
        {
            reflectblue = image[row][column];
            image[row][column] = image[row][width - column - 1];
            image[row][width - column - 1] = reflectblue;
        }
    }
    return;
}

int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position)
{
    float count = 0;
    int sum = 0;
    for (int row = i - 1; row <= (i + 1); row++)
    {
        for(int column = j - 1; column <= (j + 1); column++)
        {
            if( row < 0 || row >= height || column < 0  || column >= width)
            {
                continue;
            }
            if(color_position == RED_COLOR)
            {
                sum += image[row][column].rgbtRed;
            }
            else if (color_position == GREEN_COLOR)
            {
                sum += image[row][column].rgbtGreen;
            }
            else if (color_position == BLUE_COLOR)
            {
                sum += image[row][column].rgbtBlue;
            }
            count++;
        }
    }
    return round(sum/count);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE second[height][width];
    for( int row = 0; row < height; row++)
    {
        for( int column = 0; column < width; column++)
        {
            second[row][column] = image[row][column];
        }
    }

    for( int row = 0; row < height; row++)
    {
        for( int column = 0; column < width; column++)
        {
            image[row][column].rgbtRed = getBlur(row, column, height, width, second, RED_COLOR);
            image[row][column].rgbtGreen = getBlur(row, column, height, width, second, GREEN_COLOR);
            image[row][column].rgbtBlue = getBlur(row, column, height, width, second, BLUE_COLOR);
        }
    return;
    }
}
