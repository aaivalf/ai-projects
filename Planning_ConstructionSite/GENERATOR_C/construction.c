#include <stdlib.h>
#include <stdio.h>
#include <sys/timeb.h>

typedef unsigned char Bool;
#define TRUE 1
#define FALSE 0

/* helpers */
void create_random_positions(void);
void print_open_barriered(void);
void print_tool_positions(void);
void print_tool_goal_positions(void);

/* command line */
void usage(void);
Bool process_command_line(int argc, char *argv[]);
Bool setup_tool_numbers(int vec);
Bool setup_barrier_numbers(int vec);

/* globals */
/* command line params */
int gx, gy, gnum_tooltypes, gtool_vec, *gtool_number, gbarrier_vec, *gbarrier_number, gp_goal;

/* random values */
int gx_pos, gy_pos, **gx_tool_pos, **gy_tool_pos, **gx_barrier_pos, **gy_barrier_pos;
int **gx_tool_goal_pos, **gy_tool_goal_pos;

/* helper */
Bool **gbarrier;

int main(int argc, char *argv[]) {
    int x, y, i, j;

    /* seed the random() function */
    struct timeb tp;
    ftime(&tp);
    srandom(tp.millitm);

    /* command line treatment, first preset values */
    gx = -1;
    gy = -1;
    gnum_tooltypes = -1;
    gtool_vec = -1;
    gbarrier_vec = -1;
    gp_goal = 100;

    if (argc == 1 || (argc == 2 && *++argv[0] == '?')) {
        usage();
        exit(1);
    }
    if (!process_command_line(argc, argv)) {
        usage();
        exit(1);
    }

    create_random_positions();

    /* now output problem in PDDL syntax */
    printf("\n\n\n");

    /* header */
    printf("(define (problem construction-x%d-y%d-t%d-k%d-l%d-p%d)",
           gx, gy, gnum_tooltypes, gtool_vec, gbarrier_vec, gp_goal);
    printf("\n(:domain construction-site)");

    printf("\n(:objects ");
    for (y = 0; y < gy; y++) {
        printf("\n        ");
        for (x = 0; x < gx; x++) {
            printf("f%d-%df ", x, y);
        }
    }
    printf("\n        ");
    for (i = 0; i < gnum_tooltypes; i++) {
        printf("type%d ", i);
    }
    for (i = 0; i < gnum_tooltypes; i++) {
        if (gtool_number[i] == 0)
            continue;
        printf("\n        ");
        for (j = 0; j < gtool_number[i]; j++) {
            printf("tool%d-%d ", i, j);
        }
    }
    printf("\n)");

    printf("\n(:init");
    printf("\n(free)");
    for (y = 0; y < gy; y++) {
        for (x = 0; x < gx; x++) {
            printf("\n(location f%d-%df)", x, y);
        }
    }
    for (i = 0; i < gnum_tooltypes; i++) {
        printf("\n(type type%d)", i);
    }
    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gtool_number[i]; j++) {
            printf("\n(tool tool%d-%d)", i, j);
            printf("\n(tool-type tool%d-%d type%d)", i, j, i);
        }
    }
    for (y = 0; y < gy; y++) {
        for (x = 0; x < gx - 1; x++) {
            printf("\n(connected f%d-%df f%d-%df)", x, y, x + 1, y);
        }
    }
    for (y = 0; y < gy - 1; y++) {
        for (x = 0; x < gx; x++) {
            printf("\n(connected f%d-%df f%d-%df)", x, y, x, y + 1);
        }
    }
    for (y = 0; y < gy; y++) {
        for (x = 1; x < gx; x++) {
            printf("\n(connected f%d-%df f%d-%df)", x, y, x - 1, y);
        }
    }
    for (y = 1; y < gy; y++) {
        for (x = 0; x < gx; x++) {
            printf("\n(connected f%d-%df f%d-%df)", x, y, x, y - 1);
        }
    }
    print_open_barriered();
    print_tool_positions();
    printf("\n(at-worker f%d-%df)", gx_pos, gy_pos);
    printf("\n)");

    printf("\n(:goal");
    printf("\n(and");
    print_tool_goal_positions();
    printf("\n)");
    printf("\n)");

    printf("\n)");

    printf("\n\n\n");

    exit(0);
}

/* random problem generation functions */

void create_random_positions(void) {
    int MAX;
    int i, j, rx, ry, r;

    MAX = -1;
    for (i = 0; i < gnum_tooltypes; i++) {
        if (MAX == -1 || gtool_number[i] > MAX) {
            MAX = gtool_number[i];
        }
        if (gbarrier_number[i] > MAX) {
            MAX = gbarrier_number[i];
        }
    }
    gx_tool_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    gy_tool_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    gx_barrier_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    gy_barrier_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    gx_tool_goal_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    gy_tool_goal_pos = (int **)calloc(gnum_tooltypes, sizeof(int *));
    for (i = 0; i < gnum_tooltypes; i++) {
        gx_tool_pos[i] = (int *)calloc(MAX, sizeof(int));
        gy_tool_pos[i] = (int *)calloc(MAX, sizeof(int));
        gx_barrier_pos[i] = (int *)calloc(MAX, sizeof(int));
        gy_barrier_pos[i] = (int *)calloc(MAX, sizeof(int));
        gx_tool_goal_pos[i] = (int *)calloc(MAX, sizeof(int));
        gy_tool_goal_pos[i] = (int *)calloc(MAX, sizeof(int));
    }
    gbarrier = (Bool **)calloc(gx, sizeof(Bool *));
    for (i = 0; i < gx; i++) {
        gbarrier[i] = (Bool *)calloc(gy, sizeof(Bool));
        for (j = 0; j < gy; j++) {
            gbarrier[i][j] = FALSE;
        }
    }

    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gbarrier_number[i]; j++) {
            while (TRUE) {
                rx = random() % gx;
                ry = random() % gy;
                if (!gbarrier[rx][ry])
                    break;
            }
            gbarrier[rx][ry] = TRUE;
            gx_barrier_pos[i][j] = rx;
            gy_barrier_pos[i][j] = ry;
        }
    }
    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gtool_number[i]; j++) {
            rx = random() % gx;
            ry = random() % gy;
            gx_tool_pos[i][j] = rx;
            gy_tool_pos[i][j] = ry;
        }
    }
    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gtool_number[i]; j++) {
            r = random() % 100;
            if (r >= gp_goal) {
                gx_tool_goal_pos[i][j] = -1;
                gy_tool_goal_pos[i][j] = -1;
                continue;
            }
            rx = random() % gx;
            ry = random() % gy;
            gx_tool_goal_pos[i][j] = rx;
            gy_tool_goal_pos[i][j] = ry;
        }
    }
    while (TRUE) {
        rx = random() % gx;
        ry = random() % gy;
        if (!gbarrier[rx][ry])
            break;
    }
    gx_pos = rx;
    gy_pos = ry;
}

/* printing functions */

void print_open_barriered(void) {
    int x, y, i, j;

    for (y = 0; y < gy; y++) {
        for (x = 0; x < gx; x++) {
            if (!gbarrier[x][y]) {
                printf("\n(open f%d-%df)", x, y);
            }
        }
    }

    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gbarrier_number[i]; j++) {
            printf("\n(barrier f%d-%df)",
                   gx_barrier_pos[i][j], gy_barrier_pos[i][j]);
            printf("\n(barrier-type f%d-%df type%d)",
                   gx_barrier_pos[i][j], gy_barrier_pos[i][j], i);
        }
    }
}

void print_tool_positions(void) {
    int i, j;

    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gtool_number[i]; j++) {
            printf("\n(at tool%d-%d f%d-%df)", i, j,
                   gx_tool_pos[i][j], gy_tool_pos[i][j]);
        }
    }
}

void print_tool_goal_positions(void) {
    int i, j;

    for (i = 0; i < gnum_tooltypes; i++) {
        for (j = 0; j < gtool_number[i]; j++) {
            if (gx_tool_goal_pos[i][j] == -1)
                continue;
            printf("\n(at tool%d-%d f%d-%df)", i, j,
                   gx_tool_goal_pos[i][j], gy_tool_goal_pos[i][j]);
        }
    }
}

/* command line functions */

void usage(void) {
    printf("\nusage:\n");

    printf("\nOPTIONS   DESCRIPTIONS\n\n");
    printf("-x <num>    x scale (minimal 1)\n");
    printf("-y <num>    y scale (minimal 1)\n\n");
    printf("-t <num>    num different tool+barrier types (minimal 1)\n\n");
    printf("-k <num>    number tools vector (decimal)\n");
    printf("-l <num>    number barriers vector (decimal)\n\n");
    printf("-p <num>    probability of any tool being mentioned in the goal (preset: %d)\n\n",
           gp_goal);
}

Bool process_command_line(int argc, char *argv[]) {
    char option;

    while (--argc && ++argv) {
        if (*argv[0] != '-' || strlen(*argv) != 2) {
            return FALSE;
        }
        option = *++argv[0];
        switch (option) {
        default:
            if (--argc && ++argv) {
                switch (option) {
                case 'x':
                    sscanf(*argv, "%d", &gx);
                    break;
                case 'y':
                    sscanf(*argv, "%d", &gy);
                    break;
                case 't':
                    sscanf(*argv, "%d", &gnum_tooltypes);
                    break;
                case 'p':
                    sscanf(*argv, "%d", &gp_goal);
                    break;
                case 'k':
                    sscanf(*argv, "%d", &gtool_vec);
                    if (gnum_tooltypes == -1) {
                        break;
                    } else {
                        if (setup_tool_numbers(gtool_vec)) {
                            break;
                        } else {
                            printf("\n\ncannot interpret tool number vector.\n\n");
                            exit(1);
                        }
                    }
                    break;
                case 'l':
                    sscanf(*argv, "%d", &gbarrier_vec);
                    if (gnum_tooltypes == -1) {
                        break;
                    } else {
                        if (setup_barrier_numbers(gbarrier_vec)) {
                            break;
                        } else {
                            printf("\n\ncannot interpret barrier number vector.\n\n");
                            exit(1);
                        }
                    }
                    break;
                default:
                    printf("\n\nunknown option: %c entered\n\n", option);
                    return FALSE;
                }
            } else {
                return FALSE;
            }
        }
    }

    if (gx < 1 || gy < 1 || gnum_tooltypes < 1) {
        return FALSE;
    }

    return TRUE;
}

Bool setup_tool_numbers(int vec) {
    int current, i;

    if (gnum_tooltypes < 1)
        return FALSE;

    gtool_number = (int *)calloc(gnum_tooltypes, sizeof(int));

    current = vec;

    for (i = gnum_tooltypes - 1; i >= 0; i--) {
        gtool_number[i] = (int)(current % 10);
        if (gtool_number[i] < 0)
            return FALSE;
        current = (int)(current / 10);
    }

    return TRUE;
}

Bool setup_barrier_numbers(int vec) {
    int current, i;

    if (gnum_tooltypes < 1)
        return FALSE;

    gbarrier_number = (int *)calloc(gnum_tooltypes, sizeof(int));

    current = vec;

    for (i = gnum_tooltypes - 1; i >= 0; i--) {
        gbarrier_number[i] = (int)(current % 10);
        if (gbarrier_number[i] < 0)
            return FALSE;
        current = (int)(current / 10);
    }

    return TRUE;
}

