#include <ctype.h>
#include <stdio.h>
#include <string.h>


static char CARDS[14] = { '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A' };
static char CARD_TYPES[4] = { 'h', 'd', 's', 'c' };

int check_card(char value, char type)
{
    char *pVal = strchr(CARDS, value);
    char *pType = strchr(CARD_TYPES, type);

    if (pVal == NULL || pType == NULL) {
        return 0;
    }
    return 1;
}

int used_card(char player1[8][2], char player2[8][2], char value, char type)
{
    for (int i = 0; i < 7; i++) {
        if ((player1[i][0] == value && player1[i][1] == type) || (player2[i][0] == value && player2[i][1] == type)) {
            return 0;
        }
    }
    return 1;
}

int count_occurences(char arr[8][2], char key, int valOrType)
{
    int res = 0;

    for (int i = 0; i < 7; i++) {
        if (arr[i][valOrType] == key) {
            res++;
        }
    }
    return res;
}

int card_in_array(char key, const char arr[5])
{
    for (int i = 0; i < 4; i++) {
        if (arr[i] == key) {
            return 1;
        }
    }
    return 0;
}

int convert_card(char card)
{
    switch (card) {
    case '2':
        return 2;
    case '3':
        return 3;
    case '4':
        return 4;
    case '5':
        return 5;
    case '6':
        return 6;
    case '7':
        return 7;
    case '8':
        return 8;
    case '9':
        return 9;
    case 'T':
        return 10;
    case 'J':
        return 11;
    case 'Q':
        return 12;
    case 'K':
        return 13;
    case 'A':
        return 14;
    default:
        return 0;
    }
}


int highest_card_apart_from(char arr[8][2], char apartArr[5])
{
    char highest = '2';

    for (int i = 0; i < 7; i++) {
        if (convert_card(arr[i][0]) > convert_card(highest) && (!card_in_array(arr[i][0], apartArr))) {
            highest = arr[i][0];
        }
    }
    return convert_card(highest);
}

int highest_card_type(char cards[8][2], char apart_arr[5], char type)
{
    char highest = '2';

    for (int i = 0; i < 7; i++) {
        if (convert_card(cards[i][0]) > convert_card(highest) && (!card_in_array(cards[i][0], apart_arr)) &&
                cards[i][1] == type) {
            highest = cards[i][0];
        }
    }
    return convert_card(highest);
}

void compare_score(int score1, int score2, int *whoWon)
{
    if (score1 > score2) {
        *whoWon = 1;
    } else if (score1 < score2) {
        *whoWon = 2;
    } else if (score1 != 0) {
        *whoWon = 3;
    }
}


void card_sort(char cards[8][2])
{
    int minimum = 0;
    char tempVal;
    char tempType;

    for (int i = 0; i < 7; i++) {
        minimum = i;
        for (int j = i + 1; j < 7; j++) {
            if (convert_card(cards[j][0]) < convert_card(cards[minimum][0])) {
                minimum = j;
            }
        }
        tempVal = cards[i][0];
        tempType = cards[i][1];
        cards[i][0] = cards[minimum][0];
        cards[i][1] = cards[minimum][1];
        cards[minimum][0] = tempVal;
        cards[minimum][1] = tempType;
    }
}

int key_in_array(const char arr[7], char key)
{
    for (int i = 0; i < 7; i++) {
        if (arr[i] == key) {
            return 1;
        }
    }
    return 0;
}

void straight_flush(char player1[8][2], char player2[8][2], int *whoWon)
{
    char flushCards1[7] = { 0 };
    char flushCards2[7] = { 0 };
    int posNew1 = 6;
    int posNew2 = 6;
    int diff1 = 0;
    int diff2 = 0;
    int straightCount1 = 0;
    int straightCount2 = 0;
    int highestStraight1 = 0;
    int highestStraight2 = 0;


    card_sort(player1);
    card_sort(player2);

    for (int i = 0; i < 4; i++) {
        if (count_occurences(player1, CARD_TYPES[i], 1) > 4) {
            for (int j = 6; j >= 0; j--) {
                if (player1[j][1] == CARD_TYPES[i]) {
                    flushCards1[posNew1] = player1[j][0];
                    posNew1--;
                }
            }
        }
        if (count_occurences(player2, CARD_TYPES[i], 1) > 4) {
            for (int j = 6; j >= 0; j--) {
                if (player2[j][1] == CARD_TYPES[i]) {
                    flushCards2[posNew2] = player2[j][0];
                    posNew2--;
                }
            }
        }
    }

    for (int i = 6; i > 0; i--) {
        diff1 = convert_card(flushCards1[i]) - convert_card(flushCards1[i - 1]);

        if (diff1 == 1) {
            if (!highestStraight1) {
                highestStraight1 = convert_card(flushCards1[i]);
            }
            straightCount1++;
        } else if (diff1 > 1 && straightCount1 < 4 && flushCards1[i - 1] != 0) {
            straightCount1 = 0;
            highestStraight1 = 0;
        }
        diff2 = convert_card(flushCards2[i]) - convert_card(flushCards2[i - 1]);
        if (diff2 == 1) {
            if (!highestStraight2) {
                highestStraight2 = convert_card(flushCards2[i]);
            }
            straightCount2++;
        } else if (diff2 > 1 && straightCount2 < 4 && flushCards2[i - 1] != 0) {
            straightCount2 = 0;
            highestStraight2 = 0;
        }
    }

    if (highestStraight1 == 5 && key_in_array(flushCards1, 'A')) {
        straightCount1++;
    }

    if (highestStraight2 == 5 && key_in_array(flushCards2, 'A')) {
        straightCount2++;
    }

    if (straightCount1 < 4) {
        highestStraight1 = 0;
    }
    if (straightCount2 < 4) {
        highestStraight2 = 0;
    }

    compare_score(highestStraight1, highestStraight2, whoWon);

}

void four_kind(char player1[8][2], char player2[8][2], int *whoWon)
{
    int score1 = 0;
    int score2 = 0;
    char apartArr[5] = { '0', '0', '0', '0', '0' };

    if (*whoWon != 0) {
        return;
    }
    for (int i = 0; i < 13; i++) {
        if (score1 == 0 && count_occurences(player1, CARDS[i], 0) == 4) {
            apartArr[0] = CARDS[i];
            score1 = (i + 2) * 100 + highest_card_apart_from(player1, apartArr);

        }
        if (score2 == 0 && count_occurences(player2, CARDS[i], 0) == 4) {
            apartArr[0] = CARDS[i];
            score2 = (i + 2) * 100 + highest_card_apart_from(player2, apartArr);
        }
    }
    compare_score(score1, score2, whoWon);
}

void full_house(char player1[8][2], char player2[8][2], int *whoWon)
{
    int three1 = 0;
    int two1 = 0;
    int three2 = 0;
    int two2 = 0;
    int occurences = 0;
    int score1 = 0;
    int score2 = 0;


    if (*whoWon != 0) {
        return;
    }
    for (int i = 12; i >= 0; i--) {
        if (three1 == 0 || two1 == 0) {
            occurences = count_occurences(player1, CARDS[i], 0);
            if (occurences == 3 && three1 == 0) {
                three1 = 100 * (i + 2);
            } else if (occurences >= 2 && two1 == 0) {
                two1 = i + 2;
            }
        }
        if (three2 == 0 || two2 == 0) {
            occurences = count_occurences(player2, CARDS[i], 0);
            if (occurences == 3 && three2 == 0) {
                three2 = 100 * (i + 2);
            } else if (occurences >= 2 && two2 == 0) {
                two2 = i + 2;
            }
        }
    }
    if (three1 != 0 && two1 != 0) {
        score1 = three1 + two1;
    }
    if (three2 != 0 && two2 != 0) {
        score2 = three2 + two2;
    }
    compare_score(score1, score2, whoWon);
}


void flush(char player1[8][2], char player2[8][2], int *whoWon)
{
    char flushCard = 0;
    int score1 = 0;
    int score2 = 0;
    int highest1 = 0;
    int highest2 = 0;
    char arrCards[5] = { '0' };

    if (*whoWon != 0) {
        return;
    }

    for (int i = 0; i < 4; i++) {
        if (!score1 && count_occurences(player1, CARD_TYPES[i], 1) > 4) {
            flushCard = CARD_TYPES[i];
            score1 = 1;
        }
        if (!score2 && count_occurences(player2, CARD_TYPES[i], 1) > 4) {
            flushCard = CARD_TYPES[i];
            score2 = 1;
        }
    }

    if (score1 && score2) {
        int i = 0;
        while (i < 5 && score1 == score2) {
            highest1 = highest_card_type(player1, arrCards, flushCard);
            highest2 = highest_card_type(player2, arrCards, flushCard);
            score1 += highest1;
            score2 += highest2;
            arrCards[i] = CARDS[highest1 - 2];
            i++;
        }
    }
    compare_score(score1, score2, whoWon);
}

void straight(char player1[8][2], char player2[8][2], int *whoWon)
{
    int highestStraight1 = 0;
    int highestStraight2 = 0;
    int straightCount1 = 0;
    int straightCount2 = 0;
    int diff1 = 0;
    int diff2 = 0;


    if (*whoWon != 0) {
        return;
    }

    card_sort(player1);
    card_sort(player2);

    for (int i = 6; i > 0; i--) {
        diff1 = convert_card(player1[i][0]) - convert_card(player1[i - 1][0]);
        if (diff1 == 1) {
            if (!highestStraight1) {
                highestStraight1 = convert_card(player1[i][0]);
            }
            straightCount1++;
        } else if (diff1 > 1 && straightCount1 < 4) {
            straightCount1 = 0;
            highestStraight1 = 0;
        }
        diff2 = convert_card(player2[i][0]) - convert_card(player2[i - 1][0]);
        if (diff2 == 1) {
            if (!highestStraight2) {
                highestStraight2 = convert_card(player2[i][0]);
            }
            straightCount2++;
        } else if (diff2 > 1 && straightCount2 < 4) {
            straightCount2 = 0;
            highestStraight2 = 0;
        }
    }

    if (highestStraight1 == 5 && player1[0][0] == '2' && player1[6][0] == 'A') {
        straightCount1++;
    }

    if (highestStraight2 == 5 && player2[0][0] == '2' && player2[6][0] == 'A') {
        straightCount2++;
    }

    if (straightCount1 < 4) {
        highestStraight1 = 0;
    }
    if (straightCount2 < 4) {
        highestStraight2 = 0;
    }
    compare_score(highestStraight1, highestStraight2, whoWon);
}

void three_kind(char player1[8][2], char player2[8][2], int *whoWon)
{
    int score1 = 0;
    int score2 = 0;
    char apartArr[5] = { '0', '0', '0', '0', '0' };
    int highest1 = 0;
    int highest2 = 0;

    if (*whoWon != 0) {
        return;
    }
    for (int i = 12; i >= 0; i--) {
        if (score1 == 0 && count_occurences(player1, CARDS[i], 0) == 3) {
            score1 = (i + 2) * 100;
            apartArr[0] = CARDS[i];
        }
        if (score2 == 0 && count_occurences(player2, CARDS[i], 0) == 3) {
            score2 = (i + 2) * 100;
        }
    }
    int i = 0;
    while (i < 2 && score1 == score2 && score1 != 0) {
        highest1 = highest_card_apart_from(player1, apartArr);
        highest2 = highest_card_apart_from(player2, apartArr);
        if (highest1 == highest2) {
            apartArr[i + 1] = CARDS[highest1 - 2];
        }
        score1 += highest1;
        score2 += highest2;
        i++;
    }
    compare_score(score1, score2, whoWon);
}

void two_pairs(char player1[8][2], char player2[8][2], int *whoWon)
{
    int highPair1 = 0;
    int lowPair1 = 0;
    int highPair2 = 0;
    int lowPair2 = 0;
    int score1 = 0;
    int score2 = 0;
    char apartArr[5] = { '0', '0', '0', '0', '0' };

    if (*whoWon != 0) {
        return;
    }

    for (int i = 12; i >= 0; i--) {
        if ((highPair1 == 0 || lowPair1 == 0) && count_occurences(player1, CARDS[i], 0) == 2) {
            if (highPair1 == 0) {
                highPair1 = i + 2;
                apartArr[0] = CARDS[i];
            } else if (lowPair1 == 0) {
                lowPair1 = i + 2;
                apartArr[1] = CARDS[i];
            }

        }
        if ((highPair2 == 0 || lowPair2 == 0) && count_occurences(player2, CARDS[i], 0) == 2) {
            if (highPair2 == 0) {
                highPair2 = i + 2;
            } else if (lowPair2 == 0) {
                lowPair2 = i + 2;
            }
        }
    }
    if (lowPair1 != 0) {
        score1 = highPair1 * 10000 + lowPair1 * 100;
    }
    if (lowPair2 != 0) {
        score2 = highPair2 * 10000 + lowPair2 * 100;
    }
    if (score1 != 0 && score2 != 0 && score1 == score2) {
        score1 += highest_card_apart_from(player1, apartArr);
        score2 += highest_card_apart_from(player2, apartArr);
    }
    compare_score(score1, score2, whoWon);
}

void pair(char player1[8][2], char player2[8][2], int *whoWon)
{
    int score1 = 0;
    int score2 = 0;
    char apartArr[5] = { '0', '0', '0', '0', '0' };
    int highest1 = 0;
    int highest2 = 0;

    if (*whoWon != 0) {
        return;
    }

    for (int i = 12; i >= 0; i--) {
        if (score1 == 0 && count_occurences(player1, CARDS[i], 0) == 2) {
            score1 = (i + 2) * 100;
            apartArr[0] = CARDS[i];
        }
        if (score2 == 0 && count_occurences(player2, CARDS[i], 0) == 2) {
            score2 = (i + 2) * 100;
        }
    }
    int i = 0;
    while (i < 3 && score1 == score2 && score1 != 0) {
        highest1 = highest_card_apart_from(player1, apartArr);
        highest2 = highest_card_apart_from(player2, apartArr);
        apartArr[i + 1] = CARDS[highest1 - 2];
        score1 += highest1;
        score2 += highest2;
        i++;
    }
    compare_score(score1, score2, whoWon);
}

void high_card(char player1[8][2], char player2[8][2], int *whoWon)
{
    int score1 = 0;
    int score2 = 0;
    char apartArr[5] = { '0', '0', '0', '0', '0' };
    int highest1 = 0;
    int highest2 = 0;

    if (*whoWon != 0) {
        return;
    }
    int i = 0;
    while (i < 5 && score1 == score2) {
        highest1 = highest_card_apart_from(player1, apartArr);
        highest2 = highest_card_apart_from(player2, apartArr);
        apartArr[i] = CARDS[highest1 - 2];
        score1 += highest1;
        score2 += highest2;
        i++;
    }
    compare_score(score1, score2, whoWon);
}

int check_win(char player1[8][2], char player2[8][2])
{
    int whoWon = 0;

    straight_flush(player1, player2, &whoWon);
    four_kind(player1, player2, &whoWon);
    full_house(player1, player2, &whoWon);
    flush(player1, player2, &whoWon);
    straight(player1, player2, &whoWon);
    three_kind(player1, player2, &whoWon);
    two_pairs(player1, player2, &whoWon);
    pair(player1, player2, &whoWon);
    high_card(player1, player2, &whoWon);
    return whoWon;
}

int main(void)
{
    char player1[8][2] = { { '\0' } };
    char player2[8][2] = { { '\0' } };
    char cardType;
    char cardValue;
    char temp;
    int num = 0;
    int whoWon = 0;

    while (scanf(" %c%c%c ", &cardValue, &cardType, &temp) == 3) {
        if (!check_card(cardValue, cardType)) {
            fprintf(stderr, "Invalid card");
            return 1;
        }
        if (!used_card(player1, player2, cardValue, cardType)) {
            fprintf(stderr, "Duplicate cards");
            return 1;
        }
        if (num < 2) {
            player1[num][0] = cardValue;
            player1[num][1] = cardType;
        } else if (num < 4) {
            player2[num - 2][0] = cardValue;
            player2[num - 2][1] = cardType;
        } else {
            player1[num - 2][0] = cardValue;
            player1[num - 2][1] = cardType;
            player2[num - 2][0] = cardValue;
            player2[num - 2][1] = cardType;
        }
        num++;
        if (!isspace(temp)) {
            fprintf(stderr, "Invalid format\n");
            return 1;
        }
        if ((num == 2 || num == 4 || num == 9) && temp != '\n') {
            fprintf(stderr, "Missing new line character\n");
            return 1;
        }
        if (num == 9) {
            whoWon = check_win(player1, player2);
            if (whoWon == 1) {
                putchar('W');
            } else if (whoWon == 2) {
                putchar('L');
            } else {
                putchar('D');
            }
            num = 0;
            for (int i = 0; i < 7; i++) {
                player1[i][0] = '\0';
                player1[i][1] = '\0';
                player2[i][0] = '\0';
                player2[i][1] = '\0';
            }
            printf("\n");
        }
    }
    if (num > 0) {
        fprintf(stderr, "Wrong number of cards\n");
        return 1;
    }
    return 0;
}
