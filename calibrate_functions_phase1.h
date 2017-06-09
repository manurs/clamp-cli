#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sched.h>
#include <sys/mman.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <getopt.h>
#include "comedi_functions.h"
#include "time_management.h"

#define ERR -1
#define OK 0
#define TRUE 1
#define FALSE 0

int ini_recibido (double *min, double *min_abs, double *max, double *period_signal, Comedi_session session, int chan, int period, int freq, char* filename);

int signal_convolution (double * lectura, int size_l, double * result, int size_r);

int signal_average(double * lectura, int size_l, double * result, int size_r);

double signal_period(int seg_observacion, double * signal, int size, double th);

void array_to_file(double * array, int size, char * filename_date, char * tittle);

void calcula_escala (double min_virtual, double max_virtual, double min_viva, double max_viva, double *scale_virtual_to_real, double *scale_real_to_virtual, double *offset_virtual_to_real, double *offset_real_to_virtual);