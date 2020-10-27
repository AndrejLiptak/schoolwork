/**
 * @file    main.c
 * \mainpage HW04 Documentation
 *
 *
 * On the 'Files' page, there is a list of documented files with brief descriptions.
 *
*/
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "graph.h"
#include "heap.h"

/*
 * If you want to document it Doxygen, the first comment must remain as
 * it is now. The comment tells Doxygen that this file should be
 * processed
 *  */

int print_to_file(const char **argv, Node *src, Node *targ)
{
    FILE *fdWrite = fopen(argv[5], "w");
    if (fdWrite == NULL) {
        fprintf(stderr, "error creating file\n");
        return 1;
    }
    fprintf(fdWrite, "digraph {\n");

    while (node_get_previous(targ) != NULL) {
        src = node_get_previous(targ);
        fprintf(fdWrite, "\t%u -> %u [label=%u];\n", node_get_id(src), node_get_id(targ), node_get_distance(targ) - node_get_distance(src));
        targ = src;
    }
    fprintf(fdWrite, "}\n");
    fclose(fdWrite);
    return 0;
}

void print_to_stdout(Node *src, Node *targ)
{
    printf("digraph {\n");

    while (node_get_previous(targ) != NULL) {
        src = node_get_previous(targ);
        printf("\t%u -> %u [label=%u];\n", node_get_id(src), node_get_id(targ), node_get_distance(targ) - node_get_distance(src));
        targ = src;
    }
    printf("}\n");

}

int read_nodes(Graph *gr, const char **argv)
{
    FILE *fdNodes = fopen(argv[1], "r");
    if (fdNodes == NULL) {
        fprintf(stderr, "wrong nodes files\n");
        return 1;
    }
    char buffer[200] = { '\0' };
    char *token;
    int index = 1;
    unsigned int nodeID = 0;

    while (fgets(buffer, 200, fdNodes) != NULL) {
        token = strtok(buffer, ",");
        nodeID = strtol(token, NULL, 0);
        index = 1;
        if (errno == EINVAL || errno == ERANGE) {
            fprintf(stderr, "wrong input format\n");
            fclose(fdNodes);
            return 1;
        }
        while (token != NULL) {
            index++;
            token = strtok(NULL, ",");
        }
        if (index != 8) {
            fprintf(stderr, "wrong input format\n");
            fclose(fdNodes);
            return 1;
        }
        if (!graph_insert_node(gr, nodeID)) {
            fprintf(stderr, "error while inserting Node to graph\n");
            fclose(fdNodes);
            return 1;
        }
    }
    fclose(fdNodes);
    return 0;
}

int read_edges(const char **argv, Graph *gr)
{
    FILE *fdEdges = fopen(argv[2], "r");
    if (fdEdges == NULL) {
        fprintf(stderr, "wrong edges file\n");
        return 1;
    }

    char buffer[200] = { '\0' };
    char *token;

    int index = 1;
    unsigned int source = 0;
    unsigned int dest = 0;
    int mindelay = 0;
    while (fgets(buffer, 200, fdEdges) != NULL) {
        token = strtok(buffer, ",");
        index = 1;
        while (token != NULL) {
            if (index == 1) {
                source = strtol(token, NULL, 0);
                if (errno == EINVAL || errno == ERANGE) {
                    fprintf(stderr, "wrong input format\n");
                    fclose(fdEdges);
                    return 1;
                }
            }
            if (index == 2) {
                dest = strtol(token, NULL, 0);
                if (errno == EINVAL || errno == ERANGE) {
                    fprintf(stderr, "wrong input format\n");
                    fclose(fdEdges);
                    return 1;
                }
            }
            if (index == 4) {
                mindelay = strtol(token, NULL, 0);
                if (errno == EINVAL || errno == ERANGE) {
                    fprintf(stderr, "wrong input format\n");
                    fclose(fdEdges);
                    return 1;
                }
            }
            index++;
            token = strtok(NULL, ",");
        }
        if (index != 8) {
            fprintf(stderr, "wrong input formath\n");
            fclose(fdEdges);
            return 1;
        }
        if (!graph_insert_edge(gr, source, dest, mindelay)) {
            fprintf(stderr, "error while inserting edge\n");
            fclose(fdEdges);
            return 1;
        }
    }
    fclose(fdEdges);
    return 0;
}

int djikstra(Heap *hp, Node *targ)
{
    Node *min = NULL;
    Node *next = NULL;
    unsigned int alt = 0;
    struct edge *edges = NULL;

    while (!heap_is_empty(hp)) {
        min = heap_extract_min(hp);
        if (node_get_distance(min) == UINT_MAX) {
            fprintf(stderr, "target is not reachable from source\n");
            return 1;
        }
        if (min == targ)
            break;
        edges = node_get_edges(min);
        for (int i = 0; i < node_get_n_outgoing(min); i++) {
            next = edges[i].destination;
            alt = node_get_distance(min) + edges[i].mindelay;
            if (alt < node_get_distance(next)) {
                heap_decrease_distance(hp, next, alt, min);
            }
        }
    }
    return 0;
}

int main(int argc, const char **argv)
{
    if (argc != 5 && argc != 6) {
        fprintf(stderr, "Wrong number of arguments\n");
        return 1;
    }

    Graph *gr = graph_new();
    if (gr == NULL) {
        fprintf(stderr, "error creating graph\n");
        graph_free(gr);
        return 1;
    }

    if (read_nodes(gr, argv)) {
        graph_free(gr);
        return 1;
    }

    if (read_edges(argv, gr)) {
        graph_free(gr);

        return 1;
    }

    Heap *hp = heap_new_from_graph(gr);
    Node *src = graph_get_node(gr, strtol(argv[3], NULL, 0));
    if (src == NULL) {
        fprintf(stderr, "non-existing source node\n");
        goto error;
    }
    heap_decrease_distance(hp, src, 0, NULL);

    Node *targ = graph_get_node(gr, strtol(argv[4], NULL, 0));
    if (targ == NULL) {
        fprintf(stderr, "non-existing target node\n");
        goto error;
    }

    if (djikstra(hp, targ)) {
        goto error;
    }

    if (argc == 6) {
        if (print_to_file(argv, src, targ)) {
            goto error;
        }
    } else {
        print_to_stdout(src, targ);
    }

    graph_free(gr);
    heap_free(hp);
    return 0;

error:
    graph_free(gr);
    heap_free(hp);
    return 1;
}
