#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
 
int main(int argc,char** argv)
{
 float chunk_size = 0;
 char* p = 0;
 int sleep_time = 0;
 
 if (argc != 3)
 {
 fprintf(stderr,"Usage: memalloc bytes_to_alloc sleep_time\n");
 exit(1);
 }
 
 chunk_size = (float)atol(argv[1])*1024*1024;
 sleep_time = atoi(argv[2]);
 
 if (!(p=(char*)malloc(chunk_size)))
 {
 fprintf(stderr,"Error allocating %.2f bytes\n", chunk_size);
 exit(1);
 }
 
 printf("Allocation successful, sleeping for %d seconds\n", sleep_time);
 sleep(sleep_time);
 printf("Initializing %.2f bytes / %.2f kilobytes / %.2f megabytes / %.2f gigabytes\n", chunk_size, chunk_size/1024, chunk_size/(1024*1024), chunk_size/(1024*1024*1024));
 memset(p,0,chunk_size);
 printf("Initialization successful, sleeping for %d seconds\n", sleep_time);
 sleep(sleep_time);
 printf("Freeing memory\n");
 free(p);
 printf("Memory freed\n");
 return 0;
}
